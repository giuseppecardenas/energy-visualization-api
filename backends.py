from sqlalchemy import func
from models import Plant
from exceptions import MapEntityException, InvalidMapQueryException, GisBackendException
import logging


class MapEntity(object):
    """
    Generic map entity.

    Maps info to be displayed on the map to the corresponding
    entity's fields.
    """
    ENTITIES = {
        'plant' : Plant
    }

    _entity_fields_map = {
        Plant: {
                'plant_name' :            'pname',
                'state':                  'pstatabb',
                'nameplate_capacity':     'namepcap',
                'fuel_category':          'plfuelct',
                'annual_net_generation':  'plngenan',
                'latitude':               'lat',
                'longitude':              'lon'
        }
    }

    def __init__(self, object):
        self._object = object
        if not type(self._object) in self._entity_fields_map:
            raise MapEntityException('Class [{0}] cannot be used to create a MapEntity.'
                                     .format(self._object.__class__))

        field_dict = self._entity_fields_map[type(self._object)]
        for attr in field_dict:
            value = field_dict[attr]
            setattr(self, attr, getattr(self._object, value))

    def to_json(self):
        json = {}

        # Add fields that map directly to the database
        for field in self._entity_fields_map[type(self._object)]:
            attr_name = self._entity_fields_map[type(self._object)][field]
            json[field] = getattr(self._object, attr_name, None)

        #Add computed fields
        entity_computed_fields_map = {
            Plant: {
                'state_contribution_percentage': self._object.annual_net_generation_state_percentage
            }
        }
        computed_fields_for_entity = entity_computed_fields_map[type(self._object)]
        for computed_field in computed_fields_for_entity:
            json[computed_field] = computed_fields_for_entity[computed_field]

        return json


class MapQuery(object):
    """
    Representation of a map query.

    Maps API queries to the corresponding queries
    in the SQLAlchemy ORM.

    Allows processing of queries such as these

    {
	    'entity_type': 'plant',
	    'limit': '10',
	    'sort': {
	                'field': 'annual_net_generation',
	                'order': 'desc'
	    }
    }

    This will return a list of ten 'plant' entities
    sorted in descending order by the field
    'annual_net_generation'.

    This query

    {
	    'entity_type': 'plant',
	    'limit': 'max',
	    'within_radius': {
            'point': {
                        'latitude':  '38.416272',
                        'longitude': '-82.117837'
            },
            'radius': '30'
	    }
    }

    Will return all 'plant' entities within 30
    miles of coordinate -82.117837, 38.416272.

    We can also supply coordinates that enclose a polygon
    to the GIS engine.

    For example, this set of coordinates

        -82.681891, 38.779234
        -82.599994, 38.161377
        -81.334090, 38.204311
        -81.054471, 38.767503

    encloses a polygon in West Virginia, USA.

    This query:

    {
        'entity_type': 'plant',
        'limit': 3,
        'filter': {
                    'plfuelct': 'NUCLEAR'
        },
        'sort': {
            'plngenan': 'desc'
        },
        'within_polygon': {
            'points': [
                {
                    'latitude':  '38.779234',
                    'longitude': '-82.681891'
                },
                {
                    'latitude':  '38.161377',
                    'longitude': '-82.599994'
                },
                {
                    'latitude':  '38.204311',
                    'longitude': '-81.334090'
                },
                {
                    'latitude':  '38.767503',
                    'longitude': '-81.054471'
                },
            ]
        }
    }

    Will return the three largest nuclear power plants
    in that area, sorted in descending order by annual
    net generation.
    """

    _required_fields = ['entity_type']
    _optional_fields = ['limit', 'filter', 'sort', 'within_radius', 'within_polygon']
    _individual_field_checks = {
        'within_radius': [
                            lambda x: isinstance(x, dict),
                            lambda x: 'point' in x,
                            lambda x: 'radius' in x,
                            lambda x: 'latitude' in x['point'],
                            lambda x: 'longitude' in x['point']
        ],
        'within_polygon': [
                            lambda x: isinstance(x, dict),
                            lambda x: isinstance(x['points'], list),
                            lambda x: len(x['points']) > 3
        ],
        'sort': [
            lambda x: 'field' in x and 'order' in x,
        ]
    }
    _general_checks = [
        lambda x: 'entity_type' in x,
        lambda x: x['entity_type'] in MapEntity.ENTITIES
    ]

    def __init__(self, json_query):
        self._json_query = json_query
        self._perform_validations()
        self._orm_query = self._construct_orm_query()

    def evaluate(self):
        return self._orm_query.all()

    def _construct_orm_query(self):
        """
        Query is constructed in order.

        Filters are applied first:

            'filter', 'within_radius' or 'within_polygon'

        then sort is performed, and lastly, the limit is
        taken.

        :return: An unevaluated ORM query.
        """
        from app import session
        map_entity_model = MapEntity.ENTITIES[self._json_query['entity_type']]
        query = session.query(map_entity_model)

        # Since the point of the test is to visualize annual
        # net power generation, exclude Plant records with
        # 'plngenan' set to None or 0.
        if map_entity_model == Plant:
            query = query.filter(Plant.plngenan != None).filter(Plant.plngenan != 0)

        if 'filter' in self._json_query:
            #convert to lowercase if filtering by a string attribute:
            for attribute, value in self._json_query['filter'].items():
                query = query.filter(getattr(map_entity_model, attribute.lower()) == value)

        if 'sort' in self._json_query:
            order_value = self._json_query['sort']['order']
            model_field = getattr(map_entity_model, self._json_query['sort']['field'].lower())
            if order_value == 'desc':
                query = query.order_by(model_field.desc())
            elif order_value == 'asc':
                query = query.order_by(model_field)

        if 'limit' in self._json_query:
            query = query.limit(int(self._json_query['limit']))

        if 'within_radius' in self._json_query:
            latitude = self._json_query['within_radius']['point']['latitude']
            longitude = self._json_query['within_radius']['point']['longitude']
            radius = float(self._json_query['within_radius']['radius'])

            query = query.filter(func.ST_DistanceSphere(
                getattr(map_entity_model, 'geom'),
                func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4269)) <= radius * 1609.34)

        if 'within_polygon' in self._json_query:
            points_str = '('
            points_list = self._json_query['within_polygon']['points']
            for point in points_list:
                points_str += ('{0} {1}, ').format(point['longitude'], point['latitude'])

            #Add first point at the end to close the polygon
            points_str += ('{0} {1}').format(points_list[0]['longitude'],
                                         points_list[0]['latitude'])
            points_str += ')'

            query = query.filter(func.ST_Within(
                getattr(map_entity_model, 'geom'),
                func.ST_GeomFromEWKT('SRID=4269;POLYGON({0})'.format(points_str))
            ))

        return query


    def _perform_validations(self):
        # Perform mandatory checks
        for check in self._general_checks:
            if not check(self._json_query):
                raise InvalidMapQueryException('Check [{0}] failed for query [{1}].'
                                               .format(check, self._json_query))

        # Additional checks
        for field in self._individual_field_checks:
            if field in self._json_query:
                checks = self._individual_field_checks[field]
                for check in checks:
                    if not check(self._json_query[field]):
                        raise InvalidMapQueryException('Check [{0}] failed for query [{1}].'
                                               .format(check, self._json_query))


class Operations(object):
    """
    Helper class for mapping specific operations to
    fields in the response constructed by GisBackend.
    """

    @staticmethod
    def build_map_entity_list(orm_query_results):
        return [MapEntity(item).to_json() for item in orm_query_results]

    @staticmethod
    def get_annual_net_generation_aggregate(orm_query_results):
        aggregate = 0
        for result in orm_query_results:
            if result.plngenan:
                aggregate += result.plngenan
        return aggregate

    @staticmethod
    def get_result_count(orm_query_results):
        if not orm_query_results:
            return 0
        return len(orm_query_results)


class GisBackend(object):
    """
    Backend for GIS API v1.

    Constructs a response for a given query based on
    entity_type.
    """

    _RESPONSE_FIELDS = {
        'plant': {
                    'results': Operations.build_map_entity_list,
                    'count': Operations.get_result_count,
                    'annual_net_generation_aggregate': Operations.get_annual_net_generation_aggregate
        }
    }

    def get_results(self, json_query):
        """
        Constructs a response based on entity_type.

        :param json_query: a python dict representing an API query.
        :return: a list of MapEntity objects.
        """
        try:
            entity_type = json_query['entity_type']
            entity_type_response_fields = self._RESPONSE_FIELDS[entity_type]
            query_results = MapQuery(json_query).evaluate()

            # This seems redundant, but better make it explicit that arguments
            # may change when operations involving entity types other than
            # 'plant' are involved.
            operation_arguments_map = {
                'plant': {
                    'results': query_results,
                    'count': query_results,
                    'annual_net_generation_aggregate': query_results
                }
            }

            results = {}
            for response_field, operation in entity_type_response_fields.items():
                try:
                    results[response_field] = operation(operation_arguments_map[entity_type][response_field])
                except Exception as e:
                    logging.error('Error performing operation [{0}] with arguments [{1}].'
                                  .format(operation, operation_arguments_map[entity_type]))
            return results

        except Exception as e:
            raise GisBackendException('Error [{0}] occurred getting results for query [{1}].'
                                      .format(e, json_query)) from e