from influxdb import InfluxDBClient

client = InfluxDBClient(host = 'localhost', port = 8086)

client.create_database('PMHDome')
client.switch_database('PMHDome')

def saveToDB(cntBig, cntSmall, cntAll, partOfDay):
    carsJsonBody = [
        {
            'measurement': 'Parking cars',
            'tags': {
                'partOfDay': partOfDay,
            },
            'fields': {
                'Big Place': cntBig,
                'Small Place': cntSmall,
                'Sum': cntAll,
            }
        }
    ]
    client.write_points(carsJsonBody)
    return
