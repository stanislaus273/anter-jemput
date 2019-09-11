import json
import requests
import urllib

class Member:
    def__init__(self, name, address):
        self.name = name
        self.address = address



""" collect and complile the detailed data into one variable
    drivers: array of member Class
    route: Anter/Jemput
    passengets: array of member Class
"""
def create_data_model(self, drivers, route, passengers):

    data = {}
    data['API_key'] = 'AIzaSyBAWVu3hvu595tKB33ciDSkCbJ9FHPK4Us'
    data['num_vehicles'] = len(drivers)
    data['starts'] = []
    data['ends'] = []

    if (route == "Anter"):
        data['starts'] = [0] * len(drivers)
        for d in drivers:
            data['ends'] = range(1, len(drivers))
    elif (route == "Jemput"):
        data['ends'] = [0] * len(drivers)
        for d in drivers:
            data['ends'] = range(1, len(drivers))

    data['addresses'] = [self.gereja.address]
    data['names'] = [self.gereja.name]
    for d in drivers:
        data['addresses'].append(d.address)
        data['names'].append(d.name)
    for p in passengers:
        data['addresses'].append(p.address)
        data['names'].append(p.name)

    data['drivers'] = drivers

    return data


def create_distance_matrix(data):
    addresses = data['addresses']
    API_key = data['API_key']

    max_elements = 100
    num_addresses = len(addresses)
    max_rows = max_elements
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []

    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
    def build_address_str(addresses):
        address_str = ''
        for i in range(len(addresses) - 1):
            address_str += addresses[i] + '|'
        
        address_str += addresses[-1]
        return address_str

    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    origin_addresses_str = build_address_str(origin_addresses)
    dest_addresses_str = build_address_str(dest_addresses)
    request = request + '&origins=' + origin_addresses_str + '&destination=' + dest_addresses_str + '&key=' + API_key
    jsonResult = urllib.request.urlopen(request).read()
    response = json.loads(jsonResult)
    return response
    
def build_distance_matrix(response):
    distance_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix

def build_duration_matrix(response):
    distance_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['duration']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix

def prin_solution(data, manager, routing, solution):
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(data['drivers'][vehicle_id].name)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(data['names'][manager.IndexToNode(index)])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(data['names'][manager.IndexToNode(index)])
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distance: {}m'.format(max_route_distance))

