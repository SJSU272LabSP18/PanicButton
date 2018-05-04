# cmpe272-spring18

![alt text](https://github.com/SJSU272LabSP18/Project-Team-20/raw/master/wiki/img/logo.png "logo")

## We Fly High

---

## Panic Button ![alt text](https://github.com/SJSU272LabSP18/Project-Team-20/blob/master/wiki/img/icon.png "icon")

## Highlights:

* Size - a pack of gum
* Battery life - 1 month with daily usage
* Detachable

---

## What

![alt text](https://github.com/SJSU272LabSP18/Project-Team-20/raw/master/wiki/img/device_sketch.png "device_sketch")


A weareable panic button + phone app + data analytics suite.

### Retail Price: $29.99

---

## Why

---

## How

### When press once:
* notifies your friend(s) via text of a preset text message. location share once.

### When press twice:
* starts alarming, text friends with a different preset message, continue location sharing

### When press three or more times and hold for longer than 2 seconds:
* dials 911 on the phone, start real time location share with friend(s).

Tech stack:
Programmable circuit board
BLE module
Data Analytics App
Android App

### Deliverable
* a portable button device that's connected to phone with bluetooth or wifi
* a phone app that does location streaming, text/phone, and user data customization.
* a data analytics app that shows trends and analysis of data gathered from the device

---

## Data Analytics with Bluemix

### Architecture

![alt text](https://github.com/SJSU272LabSP18/Project-Team-20/raw/master/wiki/img/architecture.png "architecture")

### Technology Used

* Bluemix
* MySQL Database
* Python
* Chart.js

### Analyics Dashboard

![alt text](https://github.com/SJSU272LabSP18/Project-Team-20/raw/master/wiki/img/dsahboard.png "dashboard")

### Heat Map

1. Complete Map of US:

![alt text](https://github.com/SJSU272LabSP18/Project-Team-20/raw/master/wiki/img/map2.png "us_map")

2. Zommed-in Map of San Jose:

![alt text](https://github.com/SJSU272LabSP18/Project-Team-20/raw/master/wiki/img/map1.png "san_jose_map")

### EndPoints

1. Analytic Dashboard: https://nrupatest1.mybluemix.net/analytics
2. Heat Map: https://nrupatest1.mybluemix.net/map
3. Log new incident in database: https://nrupatest1.mybluemix.net/log?lat=<LATITUDE>&long=<LONGITITUDE>&sev=<SEVERITY>

---

## Team
* Haoji Liu
* Nrupa Chitley
* Rachit Choksni
* Watcharit Maharu Tainont
