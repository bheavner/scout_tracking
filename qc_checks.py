import csv
import argparse
import os

# Function to check if there are any scouts in the advancement file not in patrols
def check_scouts_in_patrols(advancement_file, patrols_file, output_dir):
    # Load patrol data
    patrol_data = {}
    with open(patrols_file, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                continue
            scout_name, patrol = row
            scout_name = scout_name.strip().lower()
            patrol = patrol.strip()
            if patrol not in patrol_data:
                patrol_data[patrol] = []
            patrol_data[patrol].append(scout_name)

    # Load advancement data
    advancement_data = {}
    with open(advancement_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 3:
                continue
            scout, req, _ = row
            scout = scout.strip().lower()
            if scout not in advancement_data:
                advancement_data[scout] = []
            advancement_data[scout].append(req)

    # Find scouts in advancement.csv who are not in patrols.tsv
    scouts_in_advance = set(advancement_data.keys())
    scouts_in_patrols = {scout for scouts in patrol_data.values() for scout in scouts}

    unassigned_scouts = scouts_in_advance - scouts_in_patrols

    # Write the report
    output_file = os.path.join(output_dir, 'scouts_in_patrols.txt')
    with open(output_file, 'w') as file:
        file.write("Scouts in advancement.csv but not in patrols.tsv:\n")
        for scout in unassigned_scouts:
            file.write(f"{scout}\n")
    print(f"Scout report saved to {output_file}")

# Function to check if there are any requirements in advancement.csv not in requirements.tsv
def check_requirements_in_advancement(advancement_file, requirements_file, output_dir):
    # Load requirements data
    requirements = set()
    with open(requirements_file, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                continue
            requirement = row[0].strip().lower()  # Normalize the requirement name
            requirements.add(requirement)

    # Load advancement data
    advancement_requirements = set()  # Using set to track all unique requirements in the advancement data
    with open(advancement_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 3:
                continue
            _, req, _ = row
            req = req.strip().lower()  # Normalize the requirement name
            advancement_requirements.add(req)

    # Find requirements in advancement.csv that aren't in requirements.tsv
    unlisted_requirements = advancement_requirements - requirements

    # Write the report
    output_file = os.path.join(output_dir, 'requirements_in_advancement.txt')
    with open(output_file, 'w') as file:
        file.write("Requirements in advancement.csv not found in requirements.tsv:\n")
        for req in unlisted_requirements:
            file.write(f"{req}\n")
    print(f"Requirement report saved to {output_file}")

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="QC Checks for Scouts and Requirements")
    parser.add_argument('advancement_file', type=str, help="Path to the advancement data file (CSV format).")
    parser.add_argument('patrols_file', type=str, help="Path to the patrols file (TSV format).")
    parser.add_argument('requirements_file', type=str, help="Path to the requirements list file (TSV format).")
    parser.add_argument('output_dir', type=str, help="Directory to save the reports.")
    parser.add_argument('--check_scouts', action='store_true', help="Run check for scouts not in patrols.")
    parser.add_argument('--check_requirements', action='store_true', help="Run check for requirements not in advancement.")
    
    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # If no flags are provided, run both checks by default
    if not (args.check_scouts or args.check_requirements):
        args.check_scouts = True
        args.check_requirements = True

    # Run the appropriate checks
    if args.check_scouts:
        check_scouts_in_patrols(args.advancement_file, args.patrols_file, args.output_dir)
    if args.check_requirements:
        check_requirements_in_advancement(args.advancement_file, args.requirements_file, args.output_dir)


if __name__ == "__main__":
    main()

