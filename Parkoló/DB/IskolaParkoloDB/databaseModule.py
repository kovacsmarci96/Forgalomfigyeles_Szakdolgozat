from influxdb import InfluxDBClient

client = InfluxDBClient(host = 'localhost', port = 8086)

client.create_database('IskolaParkolo')
client.switch_database('IskolaParkolo')

def saveToDB(cntCars, partOfDay):
    carsJsonBody = [
        {
            'measurement': 'Parking cars',
            'tags': {
                'partOfDay': partOfDay,
            },
            'fields': {
                'Count': cntCars,
            }
        }
    ]

    client.write_points(carsJsonBody)
    return
