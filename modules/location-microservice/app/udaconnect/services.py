import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def retrieve_all() -> List[Location]:
        return db.session.query(Location).all()

    """
    Below method is a copy of the following method https://github.com/udacity/nd064-c2-message-passing-projects-starter/blob/3fc91d84bb7246daa6baaf55a9eddb4c05669401/modules/api/app/udaconnect/services.py#L17
    It have been adapt to handle only one location at a time

    It returns all location events that have occurred in the same location and in the specified time range
    """
    @staticmethod
    def retrieve_location_by_proximity(person_id: int, start_date: datetime, end_date: datetime, latitude: float, longitude: float, meters=5) -> List[Location]:
        data = {
                    "person_id": person_id,
                    "longitude": longitude,
                    "latitude": latitude,
                    "meters": meters,
                    "start_date": start_date,
                    "end_date": end_date
                }
        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Location] = []
        for (
            exposed_person_id,
            location_id,
            exposed_lat,
            exposed_long,
            exposed_time,
        ) in db.engine.execute(query, **data):
            location = Location(
                id=location_id,
                person_id=exposed_person_id,
                creation_time=exposed_time,
            )
            location.set_wkt_with_coords(exposed_lat, exposed_long)
            result.append(location)
        return result

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        return new_location