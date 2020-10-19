from influxdb import InfluxDBClient

client = InfluxDBClient(host = 'localhost', port = 8086)

client.create_database('PajtaOldal')
client.switch_database('PajtaOldal')

def saveToDB(counterLR, counterLRCars, counterLRVan, counterLRTruck, counterRL, counterRLCars, counterRLVan, counterRLTruck, dayPart):
    LR_json_body = [
        {
            'measurement': 'Vehicles',
            'tags': {
                'dayPart': dayPart,
                'Direction': 'FromLeft'
            },
            'fields': {
                'All': counterLR,
                'Cars': counterLRCars,
                'Vans': counterLRVan,
                'Trucks': counterLRTruck,
            }
        }
    ]
    
    RL_json_body = [
        {
            'measurement': 'Vehicles',
            'tags': {
                'dayPart': dayPart,
                'Direction': 'FromRight'
            },
            'fields': {
                'All': counterRL,
                'Cars': counterRLCars,
                'Vans': counterRLVan,
                'Trucks': counterRLTruck,
            }
        }
    ]

    client.write_points(LR_json_body)
    client.write_points(RL_json_body)
    return

def saveToDBNight(counterLR, counterRL, dayPart):
    LR_json_body = [
        {
            'measurement': 'Vehicles',
            'tags': {
                'dayPart': dayPart,
                'Direction': 'FromLeft'
            },
            'fields': {
                'All': counterLR,
            }
        }
    ]
    
    RL_json_body = [
        {
            'measurement': 'Vehicles',
            'tags': {
                'dayPart': dayPart,
                'Direction': 'FromRight'
            },
            'fields': {
                'All': counterRL,
            }
        }
    ]

    client.write_points(LR_json_body)
    client.write_points(RL_json_body)
    return

def saveToDBBusLeft(counterLRBus, dayPart):
    LR_json_body = [
        {
            'measurement': 'Vehicles',
            'tags': {
                'dayPart': dayPart,
                'Direction': 'FromLeft'
            },
            'fields': {
                'Buses': counterLRBus,
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
                'Buses': counterRLBus,
            }
        }
    ]

    client.write_points(RL_json_body)
    return
