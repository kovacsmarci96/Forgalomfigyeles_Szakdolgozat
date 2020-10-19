from influxdb import InfluxDBClient

client = InfluxDBClient(host = 'localhost', port = 8086)

client.create_database('Sportcsarnok')
client.switch_database('Sportcsarnok')

def saveToDB(counterLR, counterRL, dayTime):
    LR_json_body = [
        {
            'measurement': 'Cars',
            'tags': {
                'dayTime': dayTime,
                'Direction': 'FromLeft'
            },
            'fields': {
                'Vehicles': counterLR
            }
        }
    ]
    
    RL_json_body = [
        {
            'measurement': 'Cars',
            'tags': {
                'dayTime': dayTime,
                'Direction': 'FromRight'
            },
            'fields': {
                'Vehicles': counterRL
            }
        }
    ]

    client.write_points(LR_json_body)
    client.write_points(RL_json_body)
    return
