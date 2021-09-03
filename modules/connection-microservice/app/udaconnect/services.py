import logging
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

PERSON_SERVICE_API_URL = os.environ["PERSON_SERVICE_API_URL"]
LOCATION_SERVICE_API_URL = os.environ["LOCATION_SERVICE_API_URL"]

class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        all_locations: List = LocationService.retrieve_all()
        filtered = filter(lambda l: l.person_id == person_id, all_locations)
        filtered = filter(lambda l: l.creation_time < end_date, filtered)
        filtered = filter(lambda l: l.creation_time >= start_date, filtered)
        locations = list(filtered)
        """
        .filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()
        """

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {person.id: person for person in PersonService.retrieve_all()}

        # Prepare arguments for queries
        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        result: List[Connection] = []
        for line in tuple(data):
            locations = LocationService.retrieve_locations_by_proximity(line["person_id"], line["start_date"], line["end_date"], line["latitude"], line["longitude"], line["meters"])
            for item in locations:
                result.append(
                    Connection(
                        person=person_map[line["person_id"]], location=location,
                    )
                )

        return result

class LocationService:
    @staticmethod
    def retrieve_all() -> List[Location]:
        locations : List[Location] = []
        response = requests.get(LOCATION_SERVICE_API_URL)
        body = response.json()
        for item in body:
            location = Location()
            location.person_id = item["person_id"]
            location.creation_time = datetime.strptime(item['creation_time'], "%Y-%m-%dT%H:%M:%S")
            location.set_wkt_with_coords(item["latitude"], item["longitude"])
            location.id = item["id"]
            locations.append(location)

        return locations

    def retrieve_locations_by_proximity(person_id: int, start_date: datetime, end_date: datetime, latitude: float, longitude: float, meters: int) -> List[Location]:
        locations : List[Location] = []
        response = requests.get("{}/persons/{}?start_date={}&end_date={}&latitude={}&longitude={}&meters".format(LOCATION_SERVICE_API_URL, person_id, start_date, end_date, latitude, longitude, meters))
        body = response.json()
        for item in body:
            location = Location()
            location.person_id = item["person_id"]
            location.creation_time = datetime.strptime(item['creation_time'], "%Y-%m-%dT%H:%M:%S")
            location.set_wkt_with_coords(item["latitude"], item["longitude"])
            location.id = item["id"]
            locations.append(location)

        return locations

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


class PersonService:
    @staticmethod
    def retrieve_all() -> List[Person]:
        persons : List[Person] = []
        response = requests.get(PERSON_SERVICE_API_URL)
        body = response.json()
        for item in body:
            person = Person()
            person.id = item["id"]
            person.first_name = item["first_name"]
            person.last_name = item["last_name"]
            person.company_name = item["company_name"]
            persons.append(person)

        return persons
