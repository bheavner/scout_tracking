import csv
import os
import argparse

# Load advancement data
def load_advancement_data(filename):
    advancement_data = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 3:  # Ensure the row has 3 columns
                continue
            scout, requirement, _ = row
            scout = scout.strip().lower()  # Normalize name to lowercase
            requirement = requirement.strip()
            if scout not in advancement_data:
                advancement_data[scout] = set()  # Use set to avoid duplicates
            advancement_data[scout].add(requirement)  # Add the completed requirement
    return advancement_data

# Load patrol data
def load_patrol_data(filename):
    patrol_data = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                continue
            scout, patrol = row
            scout = scout.strip().lower()
            patrol = patrol.strip()
            if patrol not in patrol_data:
                patrol_data[patrol] = []
            patrol_data[patrol].append(scout)
    return patrol_data

# Load requirements data
def load_requirements(filename):
    requirements = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                continue
            requirement, alt_text = row
            requirements.append((requirement.strip(), alt_text.strip()))
    return requirements

# Generate the patrol report
def generate_patrol_report(advancement_data, patrol_data, requirements, patrol_name):
    # Get the list of Scouts in the specified patrol
    scouts_in_patrol = patrol_data.get(patrol_name, [])
    report = []

    # Add the header row with the requirement names and patrol members
    header = ['Requirement'] + scouts_in_patrol
    report.append(header)

    # For each requirement, check if each scout has completed it
    for req, alt_text in requirements:
        row = [alt_text if alt_text else req]  # Use alternative text if available
        for scout in scouts_in_patrol:
            completed = '✔' if req in advancement_data.get(scout, []) else ''
            row.append(completed)
        report.append(row)

    return report

# Save the report to a file
def save_report(report, patrol_name, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the path for the TSV file
    output_file = os.path.join(output_dir, f"{patrol_name}_report.tsv")
    
    # Write the report to the TSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(report)

    print(f"Report for patrol '{patrol_name}' saved to {output_file}.")

# Main function to parse arguments and generate report
def main():
    parser = argparse.ArgumentParser(description="Generate a scout advancement report for a specific patrol.")
    
    # Arguments for input files
    parser.add_argument('advancement_file', type=str, help="Path to the advancement data file (CSV format).")
    parser.add_argument('patrol_file', type=str, help="Path to the patrol membership file (TSV format).")
    parser.add_argument('requirements_file', type=str, help="Path to the requirements list file (TSV format).")
    
    # Argument for the output directory
    parser.add_argument('output_dir', type=str, help="Directory where the reports will be saved.")
    
    # Argument for the patrol name to generate the report for
    parser.add_argument('patrol_name', type=str, help="Name of the patrol to generate the report for (e.g., 'Lions').")
    
    args = parser.parse_args()

    # Load data
    advancement_data = load_advancement_data(args.advancement_file)
    patrol_data = load_patrol_data(args.patrol_file)
    requirements = load_requirements(args.requirements_file)

    # Generate the report for the specified patrol
    report = generate_patrol_report(advancement_data, patrol_data, requirements, args.patrol_name)

    # Save the report
    save_report(report, args.patrol_name, args.output_dir)

if __name__ == "__main__":
    main()

