# MQTT Coding challenge

A Raspberry Pi based MQTT gateway is hooked to Cisco IR8xx router. The RPI is collecting parameters from sensors behind it and pushing that data to a topic on a locally residing MQTT broker.

Create an IOx application that subscribes to these topics, fetches data, transforms data and pushes to the cloud visualizer.

* Topic names to subscribe: wx, geo, buttons
* Reuse the same cloud dashboard and dweet interface created in the previous exercise
* Build/Package your application using docker toolchain
* Deploy/Run and visualize data

# Solution block diagram
