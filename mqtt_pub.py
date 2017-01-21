__author__ = "madawood"

#!/usr/bin/python
# mqtt demo on Raspberry Pi 3
# Author madawood using Open Source components
# Version 1.0  --- January 12, 2017
# This is the random message publisher thread -- mqtt topics: wx, geo, buttons

import time
import threading
import signal
import random
import logging
import random
import paho.mqtt.client as mqtt
from subprocess import *

logger = logging.getLogger("mqtt_publish")

wx = [0,0,0]
geo = [0,0]
key = [0]
def _sleep_handler(signum, frame):
    print "SIGINT Received. Stopping app"
    raise KeyboardInterrupt


def _stop_handler(signum, frame):
    print "SIGTERM Received. Stopping app"
    raise KeyboardInterrupt


class MqttPub(threading.Thread):
    def __init__(self, enabled, host, port, topics, frequency=5):
        threading.Thread.__init__(self)
        self.enabled = enabled
        self.stop_event = threading.Event()
        self.setDaemon(True)
        self.host = host
        self.port = port
        self.topics = topics
        self.frequency = frequency
        logger.debug("Mqtt publisher instance is successfully initialized!")

    def on_connect(self, client, userdata, flags, rc):
        logger.debug("PUB: Connected with result code :%s" %(str(rc)))
        client.publish(client._client_id, payload=userdata, qos=0, retain=False)
        client.disconnect()

    def run(self):
        if self.enabled:
            logger.debug("Started the publisher thread!")
            while True:
                # Check for mqtt messages to display.
                if self.stop_event.is_set():
                    logger.debug("Pub: exiting from thread, as stop event is set!")
                    self.stop_event.clear()
                    break
                for topic in self.topics:
                    # Create the Publisher connection.

                    if topic == "wx":
                        wx[0] = random.randrange(240, 310, 1) / 10.0 # Temperature
                        wx[1] = random.randrange(35, 45, 1) # Humidity
                        wx[2] = random.randrange(100000, 104000, 1) / 1000.000 # Pressure
                        logger.debug("PUB: WX is:%s"%wx)
                        byteArray = bytes(wx)
                    elif topic == "geo":
                        geo[0] = random.randrange(129000, 132000, 1) / 10000.0000 # Latitude
                        geo[1] = random.randrange(770000, 790000, 1) / 10000.0000 # Longitude
                        logger.debug("PUB: GEO is:%s"%geo)
                        byteArray = bytes(geo)
                    elif topic == "buttons":
                        key[0] = random.choice(["LEFT", "RIGHT", "UP", "DOWN", "SELECT"])
                        logger.debug("PUB: KEY is:%s"%key)
                        byteArray = bytes(key)
                    else:
                        continue
                    mqttc = mqtt.Client(client_id=topic, clean_session=True, userdata=byteArray)
                    print "Connecting to broker : %s:%s" % (self.host, self.port)
                    mqttc.connect(self.host, port=int(self.port), keepalive=60)
                    mqttc.on_connect = self.on_connect
                    mqttc.loop_forever(retry_first_connection=True)
                    #mqttc.publish(topic, payload=byteArray, qos=0, retain=False)
                    #mqttc.disconnect()
                time.sleep(self.frequency)
        else:
            logger.info("Pub: Publisher is disabled, so not starting thread!")

    def close(self):
        logger.debug("pub: stop event is set!")
        self.stop_event.set()


if __name__ == "__main__":
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    logger.setLevel(10)
    console = logging.StreamHandler()
    console.setLevel(10)
    console.setFormatter(formatter)
    logger.addHandler(console)

    signal.signal(signal.SIGTERM, _stop_handler)
    signal.signal(signal.SIGINT, _sleep_handler)
    m = MqttPub(True, "localhost", 1883, ["wx", "geo", "buttons"])
    m.start()
    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            m.close()
            print "App closed"
            break
        except Exception as ex:
            print("Caught exception! Terminating..")
