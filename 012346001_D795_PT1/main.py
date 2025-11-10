import csv
from heapq import heappush, heappop
from graph_builder import load_graph
from performance_timer import Timer
from dispatch_logger import log_dispatch

def load_csv(path):
    with open(path, newline='') as f:
        return [row for row in csv.DictReader(f)]

ambulances = load_csv("../data/ambulance.csv")
calls = load_csv("../data/calls.csv")
priority_map = {row["Call Type"]: int(row["Priority"]) for row in load_csv("../data/call_priority.csv")}
graph = load_graph("../data/location_network.csv")

def dijkstra(graph, start, goal):
    queue = [(0, start)]
    visited = set()
    distances = {start: 0}
    prev = {}

    while queue:
        cost, node = heappop(queue)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            path = []
            while node in prev:
                path.append(node)
                node = prev[node]
            path.append(start)
            path.reverse()
            return path, cost

        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if new_cost < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_cost
                prev[neighbor] = node
                heappush(queue, (new_cost, neighbor))
    return None, float('inf')

@Timer
def process_calls():
    for call in calls:
        call["Priority"] = priority_map.get(call["Call Type"], 3)
    calls_sorted = sorted(calls, key=lambda x: (int(x["Priority"]), int(x["Call ID"])))

    for call in calls_sorted[:10]:   # limit to 10 calls for first test
        best_amb, best_time, best_route = None, float('inf'), None
        for amb in ambulances:
            route, time_cost = dijkstra(graph, amb["Staging Location"], call["Location"])
            if time_cost < best_time:
                best_amb, best_time, best_route = amb, time_cost, route

        if best_amb:
            log_dispatch(call, best_amb, best_route, best_time)
            print(f"Dispatched {best_amb['Ambulance Number']} to {call['Location']} | ETA: {best_time:.2f}")

process_calls()
