def get_scout_patrol(scout, patrol_structure):
    # Search for the scout across all patrols and return the patrol name if found
    for patrol, scouts in patrol_structure.items():
        if scout in scouts:
            return patrol
    return None  # Scout not found in any patrol

def report_extra_advancements(extra_advancements):
    if extra_advancements:
        print("\nExtra advancements detected:")
        for item in extra_advancements:
            print(f"- {item}")
    else:
        print("No extra advancements.")

