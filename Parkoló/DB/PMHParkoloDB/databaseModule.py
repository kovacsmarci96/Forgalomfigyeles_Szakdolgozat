from influxdb import InfluxDBClient

client = InfluxDBClient(host = 'localhost', port = 8086)

client.create_database('PMHParkolo')
client.switch_database('PMHParkolo')

def saveToDB(cntMiddle, cntFront, cntBack, cntAll):
    carsJsonBody = [
        {
            'measurement': 'Parking cars',
            'fields': {
                'Middle Place': cntMiddle,
                'Front Place': cntFront,
                'Back Place': cntBack,
                'All': cntAll,
            }
        }
    ]

    client.write_points(carsJsonBody)
    return
