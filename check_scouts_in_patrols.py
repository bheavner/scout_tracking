import csv
import argparse

# Load patrol data
def load_patrol_data(filename):
    patrol_data = set()
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 2:
                continue
            scout, patrol = row
            scout = scout.strip().lower()  # Normalize scout name to lowercase
            patrol_data.add(scout)
    return patrol_data

# Load advancement data
def load_advancement_data(filename):
    advancement_data = set()
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            if len(row) != 3:
                continue
            scout, _, _ = row
            scout = scout.strip().lower()  # Normalize scout name to lowercase
            advancement_data.add(scout)
    return advancement_data

# Check for scouts in advancement data that are not in patrols data
def check_scouts_not_in_patrols(advancement_data, patrol_data):
    scouts_not_in_patrols = advancement_data - patrol_data
    return scouts_not_in_patrols

# Main function to parse arguments and check for errors
def main():
    parser = argparse.ArgumentParser(description="Check for Scouts in advancement.csv who are not in patrols.tsv.")
    parser.add_argument('advancement_file', type=str, help="Path to the advancement data file (CSV format).")
    parser.add_argument('patrol_file', type=str, help="Path to the patrol membership file (TSV format).")
    
    args = parser.parse_args()

    # Load the data
    advancement_data = load_advancement_data(args.advancement_file)
    patrol_data = load_patrol_data(args.patrol_file)

    # Check for Scouts not in patrols
    scouts_not_in_patrols = check_scouts_not_in_patrols(advancement_data, patrol_data)

    if scouts_not_in_patrols:
        print("Scouts in advancement.csv not found in patrols.tsv:")
        for scout in scouts_not_in_patrols:
            print(scout)
    else:
        print("All Scouts in advancement.csv are assigned to a patrol.")

if __name__ == "__main__":
    main()

