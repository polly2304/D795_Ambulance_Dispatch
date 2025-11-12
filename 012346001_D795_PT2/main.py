import csv
import heapq
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

def heuristic(a, b):
    return 0  

def a_star(graph, start, goal):
    open_set = [(0, start)]
    g_score = {start: 0}
    came_from = {}
    visited = set()

    while open_set:
        current_f, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current), g_score[current]

        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph[current]:
            tentative_g = g_score[current] + weight
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return [], float('inf') 


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))

@Timer
def process_calls():
    for call in calls:
        call["Priority"] = priority_map.get(call["Call Type"], 3)
    calls_sorted = sorted(calls, key=lambda x: (int(x["Priority"]), int(x["Call ID"])))

    for call in calls_sorted[:10]:
        print(f"Processing call {call['Call ID']} at {call['Location']} ({call['Call Type']})")
        best_amb, best_time, best_route = None, float('inf'), None
        for amb in ambulances:
            route, time_cost = a_star(graph, amb["Staging Location"], call["Location"])
            if time_cost < best_time:
                print(f"  Trying {amb['Ambulance Number']} from {amb['Staging Location']} -> {call['Location']}, cost={time_cost}")
                best_amb, best_time,

if __name__ == "__main__":
    process_calls()