import requests

# URL for the available variables in the dataset
variables_url = "http://api.census.gov/data/timeseries/eits/advm3/variables.json"

# Make the GET request to fetch the list of variables
response = requests.get(variables_url)

# Check if the request was successful
if response.status_code == 200:
    variables_data = response.json()

    # Extract the variables from the JSON response
    variables = variables_data.get('variables', {})

    # Iterate through the variables and print their name, label, and possible values
    print("Available Variables and Their Possible Values:")

    for variable_name, details in variables.items():
        # Extract the variable's label/description
        label = details.get('label', 'No description available')

        print(f"\nVariable: {variable_name} - {label}")
        
        # Check if the variable has enumerated values
        if 'values' in details:
            print("  Possible Values:")
            for value, value_label in details['values'].items():
                print(f"    {value}: {value_label}")
        else:
            print("  No enumerated values available for this variable.")
else:
    print(f"Failed to fetch variables: {response.status_code}")

