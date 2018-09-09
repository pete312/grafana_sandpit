#!/bin/env python3

from datetime import datetime, timedelta
from collections import Counter
#import json
from influxdb import InfluxDBClient
import sys


def speed_violations_parser(file):
    with open(file) as f:
        while True:
            data = f.readline()
            if data == '':
                return 
                
                
## header Trip ID,Taxi ID,Trip Start Timestamp,Trip End Timestamp,Trip Seconds,Trip Miles,Pickup Census Tract,Dropoff Census Tract,Pickup Community Area,Dropoff Community Area,Fare,Tips,Tolls,Extras,Trip Total,Payment Type,Company,Pickup Centroid Latitude,Pickup Centroid Longitude,Pickup Centroid Location,Dropoff Centroid Latitude,Dropoff Centroid Longitude,Dropoff Centroid  Location,Community Areas
# data ae0612e4f8fdd52cd8dc50c2863ce753cc55ba5b,075e6e86945bed6f219933b5e74ec0decc89a1e579d11c43b8f8a4409b3ced0d11116312cc4c4b42865e78a7fcc858a44fba22f31b0ca449ddaf402806be3fdb,10/18/2014 11:45:00 PM,10/19/2014 12:00:00 AM,780,2.4,17031831900,17031040401,6,4,$9.45,$0.00,$0.00,$2.50,$11.95,Cash,Taxi Affiliation Services,41.945170453,-87.668794439,POINT (-87.6687944391 41.9451704528),41.972035672,-87.686099898,POINT (-87.6860998978 41.972035672),57

                
def taxi_trips_parser(file):
    indexer  = { 'measurement' : 'taxi_trips',
        'tags' : ['trip_id', 'company','pickup_community_area', 'dropoff_community_area','trip_seconds', 'trip_miles'],
        'time' : 'trip_start_timestamp',
        'fields': ['trip_seconds', 'trip_miles', 'fare', 'tips', 'tolls','pickup_community_area', 'dropoff_community_area', 'company']}
    
    with open(file) as f:
        header = [h.lower().replace(' ', '_') for h in f.readline()[:-1].split(',')]
        lineno = 0
        while True:
            lineno += 1
            line = f.readline()[:-1]
            if line == '':
                return 
                
            # mapped into dict
            data = dict(zip(header,line.split(',')))
            
            try:
                yield translate_to_metric(data, indexer)
            except KeyError as err:
                print("Key error", err)
                print("line %s %s" % (lineno, data) )
    

def sanitize(d):
    #print("in  ", d)
    if d and d[0] == '$':
        #print("out ",d[1:])
        return d[1:]
    #print("out ",d)
    return d
    
def translate_to_metric(data, indexer):
    metric = {}
    
    ds = to_timestamp(data[indexer['time']])
    metric['measurement'] = indexer['measurement']
    metric['tags'] = {x:data[x] for x in indexer['tags']}
    metric['fields'] = {x:sanitize(data[x]) for x in indexer['fields']}
    metric['time'] = ds 
    
    
    return metric

def to_timestamp(d):
    #>>> '%s-%s-%sT%s:%s:%sZ' % datetime.datetime.now().timetuple()[:6]
    #'2018-9-5T22:44:45Z'
    
    TS = datetime.strptime(d,'%m/%d/%Y %H:%M:%S %p')
    #TS += timedelta(days=365 * 2)
    
    ampm = d[-2:].upper()
    if ampm == 'AM':
        pass
    elif ampm == 'PM':
        TS = TS + timedelta(hours=12)
    else:
        raise TypeError('date is not AM/PM format ' + str( d ) )
    
    
    return TS.strftime("%Y-%m-%dT%H:%M:%SZ")
    
def to_datetime(ds):
    return datetime.strptime(ds, "%Y-%m-%dT%H:%M:%SZ")
    
    
            
if __name__ == '__main__':
    
    connection = InfluxDBClient(host='localhost', port=8086)
    connection.switch_database('grafana')
    now = datetime.now()
    p = taxi_trips_parser('./data/Taxi_trips.csv')
    nbatch = 0
    batch = []
    for trip in p:
        nbatch += 1
        batch.append(trip)
        if nbatch > 9999:
            connection.write_points(batch)
            nbatch = 0
            batch = []
            print('.', end='')
            sys.stdout.flush()
        
