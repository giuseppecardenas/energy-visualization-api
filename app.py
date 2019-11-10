"""
    Python version: 3.7.5
    PostgreSQL version: 11.5
    PostGIS version: 2.5
"""

from flask import Flask

app = Flask(__name__)

import json
import logging
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backends import GisBackend

engine = create_engine('postgres://default_user1@localhost:5432/db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/api/v1/gis/', methods = ['GET'])
def api_v1_gis():
    """
    GIS API handler.

    Fails silently.

    :return: A list of MapEntity objects, and additional
    fields depending on the attribute entity_type.
    """
    backend = GisBackend()
    results = []
    try:
        results = backend.get_results(json.loads(request.data.decode('UTF-8')))
    except Exception as e:
        logging.error('Error [{0}] occurred handling request [{1}].'.format(e, request.data))

    return json.dumps(results, indent=4)