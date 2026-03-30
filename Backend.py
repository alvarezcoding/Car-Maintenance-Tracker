import json

#File Name For services.json
DATA_FILE = "services.json"

DEFAULT_DATA = {

    "current_miles": 100000
    ,
    "services": [
    #Cell 0 name holds oil change, and interval holds 6000
        {"name": "Oil Change", "category": "Fluids", "interval": 6000, "last_done": 100000}
        ,
        #Cell 1
        {"name": "Wiper Fluid", "category": "Fluids", "interval": 5000, "last_done": 100000}
        ,
        #Cell 2
        {"name": "Tire Rotation", "category": "Wheels", "interval": 6000, "last_done": 100000}
        ,
        #Cell 3
        {"name": "Brake Pads", "category": "Wheels", "interval": 45000, "last_done": 100000}
    ]
}



#Function that loads data or uses default data
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_DATA

#Function that opens file and dumps "data" dictionary
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

#Function that takes the data and input of category and uses only what matches category input
def service_by_category(data, category):
    matching_services = []

    for service in data["services"]:
        if service["category"] == category:
            matching_services.append(service)

    return matching_services

#Function that updates sevice miles and current miles
def mark_done(data, service_name, current_miles):
    for service in data["services"]:
        if service["name"] == service_name:
            service["last_done"] = current_miles
            data["current_miles"] = current_miles
            save_data(data)
            return True
    return False

#Function that gives due information on services
def service_status(data, current_miles):
    status_list = []

    for service in data["services"]:
        due_at = service["last_done"] + service["interval"]
        remaining = due_at - current_miles

        if remaining <= 0:
            status = {
                "name": service["name"]
                ,
                "category": service["category"]
                ,
                "due_at": due_at
                ,
                "remaining": remaining
                ,
                "is_due": True
                ,
                "message": f"{service['name']} is DUE ({-remaining} miles overdue)"
            }
        else:
            status = {
                "name": service["name"]
                ,
                "category": service["category"]
                ,
                "due_at": due_at
                ,
                "remaining": remaining
                ,
                "is_due": False
                ,
                "message": f"{service['name']} is NOT DUE ({remaining} miles left)"
            }
        
        status_list.append(status)
    return status_list

if __name__ == "__main__":
    data = load_data()
    print(f"Loaded data: \n{data}")

    print("\nFluids only:")
    print(service_by_category(data, "Fluids"))

    print("\nCurrent Status:")
    print(service_status(data, data["current_miles"]))

    success = mark_done(data, "Oil Change", 105000)

    if success:
        print("Success")
    else:
        print("fail")

    print("\nUpdated Status:")
    print(service_status(data, data["current_miles"]))

Initial commit - added project files
