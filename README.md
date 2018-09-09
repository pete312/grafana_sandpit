# grafana_sandpit
Doing someting cool with data in grafana

* follow the install_for_fedora27.txt to get Grafana and InfluxDB working together.
* create a virtualenv with python3 and pip install influxdb
    > virtualenv -p python3 ve
    >
    > . ./ve/bin/activate
    >
    > pip install influxdb
* run ./insert_Metro_data.py in the virutal env to add some taxi trip data in InfluxDB format from data/Taxi_trips.csv. 
    > ./insert_Metro_data.py
* import the dashboard into grafana front end http://<yourserver>:3000 from the dashboard dir
