#Made by: Marek Betka, 16324334

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

routingTable={'10001':{'10003':100,'10005':500,'10101':100},
'10002':{'10006':100},
'10003':{'10001':100,'10006':200,'10008':200},
'10004':{'10006':150,'10007':50,'10100':50},
'10005':{'10001':500,'10006':25,'10007':25},
'10006':{'10002':100,'10003':200,'10004':150},
'10007':{'10004':50,'10005':25,'10008':100},
'10008':{'10003':200,'10007':100},
'10100':{'10004':50},
'10101':{'10001':100}}

def get_shortest_path(weighted_graph, start, end):
    # We always need to visit the start
    nodes_to_visit = {start}
    visited_nodes = set()
    # Distance from start to start is 0
    distance_from_start = {start: 0}
    tentative_parents = {}

    while nodes_to_visit:
        # The next node should be the one with the smallest weight
        current = min(
            [(distance_from_start[node], node) for node in nodes_to_visit]
        )[1]

        # The end was reached
        if current == end:
            break

        nodes_to_visit.discard(current)
        visited_nodes.add(current)

        edges = weighted_graph[current]
        unvisited_neighbours = set(edges).difference(visited_nodes)
        for neighbour in unvisited_neighbours:
            neighbour_distance = distance_from_start[current] + \
                                 edges[neighbour]
            if neighbour_distance < distance_from_start.get(neighbour,
                                                            float('inf')):
                distance_from_start[neighbour] = neighbour_distance
                tentative_parents[neighbour] = current
                nodes_to_visit.add(neighbour)

    return _deconstruct_path(tentative_parents, end)


def _deconstruct_path(tentative_parents, end):
    if end not in tentative_parents:
        return None
    cursor = end
    path = []
    while cursor:
        path.append(cursor)
        cursor = tentative_parents.get(cursor)
    return list(reversed(path))

controller_address = ('localhost', 1050)
print('starting up on {} port {}'.format(*controller_address))
sock.bind(controller_address)

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(len(data), address))
    print(data)

    data = data.decode()

    data = data.split(":")
    routeFrom = data[1]
    routeTo = data[3]
    #Find shortest path
    path = get_shortest_path(routingTable, routeFrom,routeTo)
    data = "a"
    #Format packet to add delimiters to the path
    for each in path:
        data += each + ":"
    print(data)
    data = data.encode("UTF-8")
    
    if data:
        sent = sock.sendto(data, address)
        print('sent {} bytes back to {}'.format(sent, address))
