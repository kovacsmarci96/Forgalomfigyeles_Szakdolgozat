from influxdb import InfluxDBClient

client = InfluxDBClient(host = 'localhost', port = 8086)

client.create_database('PajtaOldal')
client.switch_database('PajtaOldal')

def saveToDBBusLeft(counterLRBus, dayPart):
    LR_json_body = [
        {
            'measurement': 'Vehicles',
            'tags': {
                'dayPart': dayPart,
                'Direction': 'FromLeft'
            },
            'fields': {
                'BusShouldCome': counterLRBus,
            }
        }
    ]

    client.write_points(LR_json_body)
    return

def saveToDBBusRight(counterRLBus, dayPart):
    RL_json_body = [
        {
            'measurement': 'Vehicles',
            'tags': {
                'dayPart': dayPart,
                'Direction': 'FromRight'
            },
            'fields': {
                'BusShouldCome': counterRLBus,
            }
        }
    ]

    client.write_points(RL_json_body)
    return
