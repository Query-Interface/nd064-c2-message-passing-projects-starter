from datetime import datetime

from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling

@api.route("/locations")
class LocationsResource(Resource):
    @responds(schema=LocationSchema, many=True)
    def get(self) -> List[Location]:
        locations: List[Location] = LocationService.retrieve_all()
        return locations
    
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        location: Location = LocationService.create(request.get_json())
        return location

@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location

@api.route("/locations/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
@api.param("start_date", "Lower bound of date range", _in="query", required=True)
@api.param("end_date", "Upper bound of date range", _in="query", required=True)
@api.param("latitude", "Latitude of thge position of the current user", _in="query", required=True)
@api.param("longitude", "Latitude of thge position of the current user", _in="query", required=True)
@api.param("meters", "Proximity to a given user in meters", _in="query", required=True)
class LocationByProximityResource(Resource):
    @responds(schema=LocationSchema, many=True)
    def get(self, person_id) -> List[Location]:
        locations: List[Location] = LocationService.retrieve_location_by_proximity(person_id, start_date=request.args["start_date"], end_date=request.args["end_date"],
                latitude=request.args["latitude"], longitude=request.args["longitude"], meters=request.args["meters"])
        return locations
