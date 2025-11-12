import csv

def load_graph(filename="../data/location_network.csv"):
    graph = {}
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = row["Start"].strip()
            end = row["End"].strip()
            weight = float(row["Distance"]) + float(row["Travel Time"]) + float(row["Traffic Delay"])
            graph.setdefault(start, []).append((end, weight))
            graph.setdefault(end, []).append((start, weight))  # ← add this line
    return graph