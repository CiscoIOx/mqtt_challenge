__author__ = "madawood"

# !/usr/bin/python
# mqtt demo on Raspberry Pi 3
# Author madawood using Open Source components
# Version 1.0  --- January 12, 2017
# This is the random message publisher thread -- mqtt topics: wx, geo, buttons

import time
import random
import paho.mqtt.client as mqtt

wx = [0, 0, 0]
geo = [0, 0]
key = [0]


def run(host, port, topics):
    print("Started the publisher thread!")
    while True:
        for topic in topics:
            # Create the Publisher connection.
            if topic == "wx":
                wx[0] = random.randrange(240, 310, 1) / 10.0  # Temperature
                wx[1] = random.randrange(35, 45, 1)  # Humidity
                wx[2] = random.randrange(100000, 104000, 1) / 1000.000  # Pressure
                print("PUB: WX is:%s" % wx)
                byteArray = bytes(wx)
            elif topic == "geo":
                geo[0] = random.randrange(129000, 132000, 1) / 10000.0000  # Latitude
                geo[1] = random.randrange(770000, 790000, 1) / 10000.0000  # Longitude
                print("PUB: GEO is:%s" % geo)
                byteArray = bytes(geo)
            elif topic == "buttons":
                key[0] = random.choice(["LEFT", "RIGHT", "UP", "DOWN", "SELECT"])
                print("PUB: KEY is:%s" % key)
                byteArray = bytes(key)
            else:
                continue
            mqttc = mqtt.Client(clean_session=True)
            print "Connecting to broker : %s:%s" % (host, port)
            mqttc.connect(host, port=int(port), keepalive=60)
            mqttc.publish(topic, payload=byteArray)
            mqttc.disconnect()
        time.sleep(5)

if __name__ == "__main__":
    run("localhost", 1883, ["wx", "geo", "buttons"])
