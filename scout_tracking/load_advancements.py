# load_advancements.py

import csv

def load_advancements(advancement_file, patrol_structure, requirements):
    additional_scouts = [] 
    additional_requirements = set()

    with open(advancement_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            if len(row) != 3:
                continue  # Skip rows that don't have 3 columns (Name, Advancement Info, Date Completed)

            scout_name, advancement, _ = row  # We don't need the Date Completed for now

            # Check if the scout exists in the patrol structure
            scout_name = scout_name.lower()
            found_scout = False
            for patrol, scouts in patrol_structure.items():
                if scout_name in scouts:
                    found_scout = True
                    # Add the advancement to the scout's list in the patrol structure
                    if advancement.lower() in requirements:
                        scouts[scout_name]['advancements'].append(advancement.lower())
                    else:
                        additional_requirements.add(advancement)
                    break

            if not found_scout:
                additional_scouts.append(scout_name)

    # Debugging: Print the patrol structure after loading advancements
#    print(f"Patrol structure after loading advancements: {patrol_structure}")

    return patrol_structure, additional_scouts, list(additional_requirements)

