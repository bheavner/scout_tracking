import csv

def load_requirements(filename):
    requirements = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header row
        for row in reader:
            if len(row) == 2:
                requirement, alt_text = row
                requirements[requirement.lower()] = alt_text.strip()
    return requirements

