#!/bin/env python

# insert some test data into influxDB
from influxdb import InfluxDBClient
import datetime


def test_influxdb_inserts():
    client = InfluxDBClient(host='localhost', port=8086)
    #client.create_database('test_one')
    print( "existing databases " , client.get_list_database() )
    
    client.switch_database('grafana')
    
    json_body = [
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "%s-%s-%sT8:01:00Z" % ( datetime.datetime.now().timetuple()[:3] ),
        "fields": {
            "duration": 127
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "%s-%s-%sT8:04:00Z" % ( datetime.datetime.now().timetuple()[:3] ),
        "fields": {
            "duration": 132
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "%s-%s-%sT8:02:00Z"  % ( datetime.datetime.now().timetuple()[:3] ),
        "fields": {
            "duration": 129
        }
    }
    ]
    print( "insert ",  client.write_points(json_body) )
    
    
    
    
def do_query():
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('grafana')
    print ( client.query('SELECT "duration" FROM "autogen"."brushEvents" WHERE time > now() - 4d GROUP BY "user"') )
   
    


if __name__ == "__main__":
    test_influxdb_inserts()
    
    do_query()