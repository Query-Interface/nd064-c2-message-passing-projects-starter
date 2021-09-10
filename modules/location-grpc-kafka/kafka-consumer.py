import os
from kafka import KafkaConsumer
import json
from sqlalchemy import create_engine
from sqlalchemy.sql import text

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER)
for message in consumer:
    print (message)
    payload = message.value.decode('utf-8')
    location = json.loads(payload)
    data = {
        "person_id": int(location["personId"]),
        "latitude": float(location["latitude"]),
        "longitude": float(location["longitude"])
    }

    engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    engine.execute(
        text("""INSERT INTO location(person_id, coordinate) VALUES(:person_id, ST_Point(:latitude, :longitude))"""),
        **data)

