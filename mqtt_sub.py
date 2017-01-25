__author__ = "madawood"

# !/usr/bin/python
# mqtt demo on Raspberry Pi 3 using Sain Smart or Adafruit 16x2 LCD and button module
# Author madawood using Open Source components
# Version 1.3  --- January 11, 2017
# This is the LCD message subscriber thread.

import json
import paho.mqtt.client as mqtt

data = {}


def on_connect(client, userdata, flags, rc):
    print("SUB: Connected with result code :%s" % (str(rc)))
    client.subscribe(str(userdata))


def on_message(client, userdata, msg):
    print("SUB: Payload from : %s" % userdata)
    print("SUB: Payload is : %s" % msg.payload)
    payload = msg.payload
    payload = payload.replace("'", "\"")
    global data
    try:
        payload = json.loads(payload)
    except ValueError:
        print("Given payload is not in json format!")
    if userdata == "wx":
        data["Temperature"] = payload[0]
        data["Humidity"] = payload[1]
        data["Pressure"] = payload[2]
    elif userdata == "geo":
        data["Latitude"] = payload[0]
        data["Longitude"] = payload[1]
    elif userdata == "buttons":
        data["Key"] = payload
    # data = {str(userdata): json.loads(paylaod)}
    client.disconnect()


def run(host, port, topics):
    print("Started the subscription thread!")
    while True:
        try:
            for topic in topics:
                client = mqtt.Client(clean_session=True, userdata=topic)
                client.connect(host, port=int(port), keepalive=60)
                client.on_connect = on_connect
                client.on_message = on_message
                client.loop_forever(timeout=3)
        except Exception as ex:
            print("Error in subscription:%s" % str(ex))
            break


if __name__ == "__main__":
    run("localhost", 1883, ["wx", "geo", "buttons"])
