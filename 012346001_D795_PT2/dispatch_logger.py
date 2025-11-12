import csv, os

def log_dispatch(call, amb, route, time_cost):
    record = {
        "CallID": call["Call ID"],
        "CallType": call["Call Type"],
        "CallLocation": call["Location"],
        "Ambulance": amb["Ambulance Number"],
        "Route": " -> ".join(route or []),
        "Time": f"{time_cost:.2f}"
    }
    log_path = "ambulance_call_log.csv"
    file_exists = os.path.isfile(log_path)
    with open(log_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=record.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)
