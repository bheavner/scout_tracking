def initialize_patrol_structure(patrol_data):
    # Initialize a 3D dictionary: patrol -> scout -> dictionary with advancements list
    patrol_structure = {}

    # Loop through each scout and their patrol
    for scout, patrol_name in patrol_data.items():
        # Initialize patrol if not already present
        if patrol_name not in patrol_structure:
            patrol_structure[patrol_name] = {}

        # Add scout to the appropriate patrol and initialize their advancement list as a dictionary
        patrol_structure[patrol_name][scout] = {'advancements': []}

    return patrol_structure

