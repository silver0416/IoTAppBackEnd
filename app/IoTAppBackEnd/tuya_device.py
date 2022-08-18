"""This module has components that are used for testing tuya's device control and Pulsar massage queue."""
import logging
import yaml
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
    TUYA_LOGGER,
)
with open('secret.yml', 'r') as f:
    secret = yaml.load(f, Loader=yaml.FullLoader)
# print(secret['tuya']['access_key'])

ACCESS_ID = secret['tuya']['access_id']
ACCESS_KEY = secret['tuya']['access_key']
API_ENDPOINT = "https://openapi.tuyacn.com"
MQ_ENDPOINT = "wss://mqe.tuyacn.com:8285/"

# # Enable debug log
TUYA_LOGGER.setLevel(logging.DEBUG)

# # Init openapi and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# # Call any API from Tuya
# response = openapi.get("/v1.0/statistics-datas-survey", dict())

# # Init Message Queue
# open_pulsar = TuyaOpenPulsar(
#     ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT, TuyaCloudPulsarTopic.PROD
# )
# # Add Message Queue listener
# open_pulsar.add_message_listener(lambda msg: print(f"---\nexample receive: {msg}"))

# # Start Message Queue
# open_pulsar.start()

# input()
# # Stop Message Queue
# open_pulsar.stop()

