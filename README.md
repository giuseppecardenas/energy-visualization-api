# -----
The API was constructed using Flask, SQLAlchemy, GeoAlchemy2 running on a Postgres 11.5 database with PostGIS 2.5 enabled. The creation script for the database is provided. It already contains the relevant data from the given excel file.

## API Usage Examples:

### Return 10 largest power plants in the US

```
$ curl -H "Content-Type: application/json" -X GET -d '{"entity_type":"plant", "limit":"10", "sort": {"field": "PLNGENAN", "order": "desc" }}' http://localhost:5000/api/v1/gis/

Response:

{
    "results": [
        {
            "plant_name": "Palo Verde",
            "state": "AZ",
            "nameplate_capacity": 4209.6,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 32377477,
            "latitude": 33.3881,
            "longitude": -112.8617,
            "state_contribution_percentage": 29.776601069962716
        },
        {
            "plant_name": "Browns Ferry",
            "state": "AL",
            "nameplate_capacity": 3494.0,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 26214623,
            "latitude": 34.7042,
            "longitude": -87.1189,
            "state_contribution_percentage": 18.349452945348293
        },
        {
            "plant_name": "Peach Bottom",
            "state": "PA",
            "nameplate_capacity": 2784.6,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 21875435,
            "latitude": 39.758936,
            "longitude": -76.268742,
            "state_contribution_percentage": 10.171474443749863
        },
        {
            "plant_name": "South Texas Project",
            "state": "TX",
            "nameplate_capacity": 2708.6,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 21694303,
            "latitude": 28.795,
            "longitude": -96.0481,
            "state_contribution_percentage": 4.779098319665932
        },
        {
            "plant_name": "Oconee",
            "state": "SC",
            "nameplate_capacity": 2666.7,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 21177103,
            "latitude": 34.7939,
            "longitude": -82.8986,
            "state_contribution_percentage": 21.83526955564324
        },
        {
            "plant_name": "Turkey Point",
            "state": "FL",
            "nameplate_capacity": 3678.7,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 20506630,
            "latitude": 25.4356,
            "longitude": -80.3308,
            "state_contribution_percentage": 8.608041589743351
        },
        {
            "plant_name": "Comanche Peak",
            "state": "TX",
            "nameplate_capacity": 2430.0,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 20385142,
            "latitude": 32.298365,
            "longitude": -97.785515,
            "state_contribution_percentage": 4.490699603409771
        },
        {
            "plant_name": "West County Energy Center",
            "state": "FL",
            "nameplate_capacity": 4263.0,
            "fuel_category": "GAS",
            "annual_net_generation": 20297460,
            "latitude": 26.6986,
            "longitude": -80.3747,
            "state_contribution_percentage": 8.520238568997057
        },
        {
            "plant_name": "McGuire",
            "state": "NC",
            "nameplate_capacity": 2440.6,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 19884289,
            "latitude": 35.4331,
            "longitude": -80.9486,
            "state_contribution_percentage": 15.20575808698621
        },
        {
            "plant_name": "Vogtle",
            "state": "GA",
            "nameplate_capacity": 4520.0,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 19860229,
            "latitude": 33.1427,
            "longitude": -81.7625,
            "state_contribution_percentage": 14.943483096884533
        }
    ],
    "count": 10,
    "annual_net_generation_aggregate": 224272691
}
```

### Return all nuclear power plants in Texas

```
$ curl -H "Content-Type: application/json" -X GET -d '{"entity_type":"plant", "filter": {"PSTATABB": "TX", "PLFUELCT": "NUCLEAR"}, "sort": {"field": "PLNGENAN", "order": "desc" } }' http://localhost:5000/api/v1/gis/

Response:

{
    "results": [
        {
            "plant_name": "South Texas Project",
            "state": "TX",
            "nameplate_capacity": 2708.6,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 21694303,
            "latitude": 28.795,
            "longitude": -96.0481,
            "state_contribution_percentage": 4.779098319665932
        },
        {
            "plant_name": "Comanche Peak",
            "state": "TX",
            "nameplate_capacity": 2430.0,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 20385142,
            "latitude": 32.298365,
            "longitude": -97.785515,
            "state_contribution_percentage": 4.490699603409771
        }
    ],
    "count": 2,
    "annual_net_generation_aggregate": 42079445
}
```

### Return 5 largest power plants in Florida in descending order

```
$ curl -H "Content-Type: application/json" -X GET -d '{"entity_type":"plant", "limit":"5", "filter": {"PSTATABB": "FL"}, "sort": {"field": "PLNGENAN", "order": "desc" } }' http://localhost:5000/api/v1/gis/

Response:

{
    "results": [
        {
            "plant_name": "Turkey Point",
            "state": "FL",
            "nameplate_capacity": 3678.7,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 20506630,
            "latitude": 25.4356,
            "longitude": -80.3308,
            "state_contribution_percentage": 8.608041589743351
        },
        {
            "plant_name": "West County Energy Center",
            "state": "FL",
            "nameplate_capacity": 4263.0,
            "fuel_category": "GAS",
            "annual_net_generation": 20297460,
            "latitude": 26.6986,
            "longitude": -80.3747,
            "state_contribution_percentage": 8.520238568997057
        },
        {
            "plant_name": "St Lucie",
            "state": "FL",
            "nameplate_capacity": 2160.0,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 15586562,
            "latitude": 27.348611,
            "longitude": -80.246389,
            "state_contribution_percentage": 6.542750999901657
        },
        {
            "plant_name": "Hines Energy Complex",
            "state": "FL",
            "nameplate_capacity": 3297.0,
            "fuel_category": "GAS",
            "annual_net_generation": 12300686,
            "latitude": 27.788215,
            "longitude": -81.869983,
            "state_contribution_percentage": 5.163443075257796
        },
        {
            "plant_name": "Martin",
            "state": "FL",
            "nameplate_capacity": 6071.5,
            "fuel_category": "GAS",
            "annual_net_generation": 10884521,
            "latitude": 27.0536,
            "longitude": -80.5628,
            "state_contribution_percentage": 4.568981322256992
        }
    ],
    "count": 5,
    "annual_net_generation_aggregate": 79575859
}
```

### Return 3 largest nuclear power plants in the US

```
$ curl -H "Content-Type: application/json" -X GET -d '{"entity_type":"plant", "limit":"3", "filter": {"PLFUELCT": "NUCLEAR"}, "sort": {"field": "PLNGENAN", "order": "desc" } }' http://localhost:5000/api/v1/gis/

Response:

{
    "results": [
        {
            "plant_name": "Palo Verde",
            "state": "AZ",
            "nameplate_capacity": 4209.6,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 32377477,
            "latitude": 33.3881,
            "longitude": -112.8617,
            "state_contribution_percentage": 29.776601069962716
        },
        {
            "plant_name": "Browns Ferry",
            "state": "AL",
            "nameplate_capacity": 3494.0,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 26214623,
            "latitude": 34.7042,
            "longitude": -87.1189,
            "state_contribution_percentage": 18.349452945348293
        },
        {
            "plant_name": "Peach Bottom",
            "state": "PA",
            "nameplate_capacity": 2784.6,
            "fuel_category": "NUCLEAR",
            "annual_net_generation": 21875435,
            "latitude": 39.758936,
            "longitude": -76.268742,
            "state_contribution_percentage": 10.171474443749863
        }
    ],
    "count": 3,
    "annual_net_generation_aggregate": 80467535
}
```

### Return all solar power plants within 80 miles of San Francisco, California

```
$ curl -H "Content-Type: application/json" -X GET -d '{"entity_type":"plant", "filter": {"PLFUELCT": "SOLAR"}, "within_radius": { "point": { "latitude": "37.762460", "longitude": "-122.446957" }, "radius": "80" } }' http://localhost:5000/api/v1/gis/

Response:

{
    "results": [
        {
            "plant_name": "ASTI",
            "state": "CA",
            "nameplate_capacity": 1.0,
            "fuel_category": "SOLAR",
            "annual_net_generation": 1541,
            "latitude": 38.761389,
            "longitude": -122.975278,
            "state_contribution_percentage": 0.0007809497480071286
        },
        {
            "plant_name": "Bear Creek Solar",
            "state": "CA",
            "nameplate_capacity": 1.5,
            "fuel_category": "SOLAR",
            "annual_net_generation": 3722,
            "latitude": 38.136389,
            "longitude": -121.148889,
            "state_contribution_percentage": 0.001886239430293662
        },
        {
            "plant_name": "Beringer",
            "state": "CA",
            "nameplate_capacity": 1.2,
            "fuel_category": "SOLAR",
            "annual_net_generation": 1629,
            "latitude": 38.510833,
            "longitude": -122.479722,
            "state_contribution_percentage": 0.0008255464889705468
        },
        {
            "plant_name": "California PV Energy at ISD WWTP",
            "state": "CA",
            "nameplate_capacity": 1.0,
            "fuel_category": "SOLAR",
            "annual_net_generation": 2193,
            "latitude": 38.001111,
            "longitude": -121.703889,
            "state_contribution_percentage": 0.001111371056054272
        },
        {
            "plant_name": "Cloverdale Solar I",
            "state": "CA",
            "nameplate_capacity": 1.5,
            "fuel_category": "SOLAR",
            "annual_net_generation": 2245,
            "latitude": 38.773056,
            "longitude": -123.017778,
            "state_contribution_percentage": 0.0011377236757144737
        },
        {
            "plant_name": "Columbia Solar Energy, LLC",
            "state": "CA",
            "nameplate_capacity": 19.2,
            "fuel_category": "SOLAR",
            "annual_net_generation": 40794,
            "latitude": 38.019671,
            "longitude": -121.86506,
            "state_contribution_percentage": 0.02067363012342817
        },
        {
            "plant_name": "Cottonwood Solar, LLC Cottonwood Carport",
            "state": "CA",
            "nameplate_capacity": 1.0,
            "fuel_category": "SOLAR",
            "annual_net_generation": 828,
            "latitude": 38.129759,
            "longitude": -122.568158,
            "state_contribution_percentage": 0.0004196147899739797
        },
        
        ...
        
        "count": 48,
        "annual_net_generation_aggregate": 434009
}
```
        
### Return all plants in a polygon about 80 kms by 120 kms, encompassing Charleston and Huntington, WV

```
$ curl -H "Content-Type: application/json" -X GET -d '{"entity_type":"plant","within_polygon":{"points":[{"latitude":  "38.779234","longitude": "-82.681891"},{"latitude":  "38.161377","longitude": "-82.599994"},{"latitude":  "38.204311", "longitude": "-81.334090"},{"latitude":  "38.767503","longitude": "-81.054471"}]}}' http://localhost:5000/api/v1/gis/

Response:

{
    "results": [
        {
            "plant_name": "Winfield",
            "state": "WV",
            "nameplate_capacity": 24.5,
            "fuel_category": "HYDRO",
            "annual_net_generation": 107993,
            "latitude": 38.5274,
            "longitude": -81.91392,
            "state_contribution_percentage": 0.14220276457986208
        },
        {
            "plant_name": "Big Sandy Peaker Plant",
            "state": "WV",
            "nameplate_capacity": 353.4,
            "fuel_category": "GAS",
            "annual_net_generation": 114396,
            "latitude": 38.3441,
            "longitude": -82.5938,
            "state_contribution_percentage": 0.15063409162517852
        },
        {
            "plant_name": "Ceredo Generating Station",
            "state": "WV",
            "nameplate_capacity": 519.0,
            "fuel_category": "GAS",
            "annual_net_generation": 110627,
            "latitude": 38.3681,
            "longitude": -82.5339,
            "state_contribution_percentage": 0.14567115680809314
        },
        {
            "plant_name": "John E Amos",
            "state": "WV",
            "nameplate_capacity": 2932.6,
            "fuel_category": "COAL",
            "annual_net_generation": 14311262,
            "latitude": 38.4731,
            "longitude": -81.8233,
            "state_contribution_percentage": 18.844749391411725
        },
        {
            "plant_name": "Marmet",
            "state": "WV",
            "nameplate_capacity": 14.4,
            "fuel_category": "HYDRO",
            "annual_net_generation": 78551,
            "latitude": 38.2526,
            "longitude": -81.5695,
            "state_contribution_percentage": 0.10343419814722016
        }
    ],
    "count": 5,
    "annual_net_generation_aggregate": 14722829
}
```
