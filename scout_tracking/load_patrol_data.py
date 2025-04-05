import csv

def load_patrol_data(filename):
    patrol_data = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header row
        for row in reader:
            if len(row) == 2:
                scout_name, patrol_name = row
                patrol_data[scout_name.lower()] = patrol_name.lower()
    return patrol_data

