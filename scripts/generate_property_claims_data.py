import pandas as pd
import numpy as np
import os
from datetime import datetime

# Define the function to create the dataset
def create_property_claims_dataset(num_records=100):
    # Get current date for file naming
    current_date = datetime.now().strftime("%m-%d")

    # Define lists of possible values for categorical columns
    loss_categories = ['Water Damage', 'Fire', 'Theft', 'Wind Damage', 'Hail Damage', 'Lightning Damage', 'Mold']
    loss_subcategories = {
        'Water Damage': ['Pipe Burst', 'Plumbing Leak', 'Appliance Leak', 'Sewer Backup', 'Roof Leak'],
        'Fire': ['Electrical Fire', 'Kitchen Fire', 'Heating Equipment', 'Wildfire', 'Arson'],
        'Theft': ['Burglary', 'Home Invasion', 'Package Theft', 'Vehicle Break-in'],
        'Wind Damage': ['Hurricane', 'Tornado', 'Severe Storm', 'Fallen Tree'],
        'Hail Damage': ['Roof Damage', 'Siding Damage', 'Window Damage', 'Vehicle Damage'],
        'Lightning Damage': ['Direct Strike', 'Power Surge', 'Fire from Strike'],
        'Mold': ['Water Intrusion', 'HVAC Related', 'Poor Ventilation']
    }

    loss_mechanisms = ['Freezing', 'Overheating', 'Impact', 'Wear and Tear', 'Corrosion', 'Forced Entry',
                       'Electrical Surge', 'Mechanical Failure', 'Human Error']

    origins_of_failure = ['Faulty Installation', 'Aging Infrastructure', 'Manufacturer Defect',
                         'Poor Maintenance', 'Weather Event', 'Weak Security', 'Design Flaw']

    components = ['Pipe', 'Wiring', 'Roof', 'Appliance', 'HVAC System', 'Door/Window', 'Sprinkler System',
                 'Foundation', 'Siding', 'Plumbing Fixture']

    subcomponents = {
        'Pipe': ['Pipe Joint', 'Valve', 'Fitting', 'Main Line'],
        'Wiring': ['Electrical Outlet', 'Circuit Breaker', 'Junction Box', 'Wire Insulation'],
        'Roof': ['Shingles', 'Flashing', 'Gutter', 'Vent'],
        'Appliance': ['Water Heater', 'Dishwasher', 'Washing Machine', 'Refrigerator'],
        'HVAC System': ['Furnace', 'Air Conditioner', 'Ductwork', 'Thermostat'],
        'Door/Window': ['Lock', 'Frame', 'Glass', 'Weather Stripping'],
        'Sprinkler System': ['Sprinkler Head', 'Control Valve', 'Backflow Preventer', 'Pipe'],
        'Foundation': ['Concrete', 'Footing', 'Slab', 'Basement Wall'],
        'Siding': ['Vinyl Panel', 'Wood Panel', 'Trim', 'Insulation'],
        'Plumbing Fixture': ['Toilet', 'Sink', 'Shower/Tub', 'Faucet']
    }

    manufacturers = {
        'Pipe': ['PipeCo', 'FlowMaster', 'AquaPipe', 'DuraPipe'],
        'Wiring': ['WireTech', 'ElectroPro', 'CircuitMaster', 'PowerWire'],
        'Roof': ['RoofPro', 'ShingleMaster', 'WeatherGuard', 'TopRoof'],
        'Appliance': ['ApplianceCo', 'HomeTech', 'KitchenPro', 'MajesticAppliance'],
        'HVAC System': ['CoolAir', 'TempControl', 'ClimateWorks', 'AirMaster'],
        'Door/Window': ['SecureDoor', 'WindowWorld', 'SafeEntry', 'LockSafe'],
        'Sprinkler System': ['SprinklerPro', 'WaterGuard', 'FireStop', 'SprayMaster'],
        'Foundation': ['SolidBase', 'FoundationPro', 'ConcreteMasters', 'StrongHold'],
        'Siding': ['SidingPro', 'ExteriorMaster', 'WeatherShield', 'DuraSide'],
        'Plumbing Fixture': ['FixturePro', 'BathMaster', 'WaterWorks', 'PlumbingPlus']
    }

    claim_statuses = ['Open', 'Closed', 'Pending Subrogation', 'Under Investigation', 'Denied']

    # Generate random data
    data = {
        'claim_id': [f'CLM{np.random.randint(100000, 999999)}' for _ in range(num_records)],
        'policyholder_id': [f'PH{np.random.randint(10000, 99999)}' for _ in range(num_records)],
        'date_of_loss': [datetime(2025, np.random.randint(1, 4), np.random.randint(1, 29)).strftime('%Y-%m-%d') for _ in range(num_records)],
        'location_of_loss': [f'{np.random.randint(100, 999)} {np.random.choice(["Main", "Oak", "Elm", "Maple", "Pine"])} St, {np.random.choice(["Springfield", "Denver", "Miami", "Seattle", "Chicago", "Boston", "Atlanta"])}, {np.random.choice(["IL", "CO", "FL", "WA", "IL", "MA", "GA"])}' for _ in range(num_records)]
    }

    # Generate loss categories and related fields
    loss_category_list = np.random.choice(loss_categories, num_records)
    data['loss_category'] = loss_category_list

    # Generate subcategories based on the loss category
    data['loss_subcategory'] = [np.random.choice(loss_subcategories[category]) for category in loss_category_list]

    data['loss_mechanism'] = np.random.choice(loss_mechanisms, num_records)
    data['origin_of_failure'] = np.random.choice(origins_of_failure, num_records)

    # Generate components and related fields
    component_list = np.random.choice(components, num_records)
    data['component_of_failure'] = component_list

    # Generate subcomponents based on the component
    data['sub_component_of_failure'] = [np.random.choice(subcomponents[component]) for component in component_list]

    # Generate manufacturers based on the component
    data['manufacturer_brand'] = [np.random.choice(manufacturers[component]) for component in component_list]

    data['model_serial_number'] = [f'{manufacturer[:2].upper()}-{np.random.randint(10000, 99999)}' for manufacturer in data['manufacturer_brand']]

    # Generate adjuster notes
    adjuster_notes_templates = [
        "{subcategory} due to {mechanism}.",
        "Damage caused by {subcategory} resulting from {origin}.",
        "{component} failure led to {subcategory}.",
        "{subcategory} originated from {subcomponent} issue.",
        "Property damaged by {subcategory} after {component} malfunction."
    ]

    data['adjuster_notes'] = [
        np.random.choice(adjuster_notes_templates).format(
            subcategory=data['loss_subcategory'][i],
            mechanism=data['loss_mechanism'][i],
            origin=data['origin_of_failure'][i],
            component=data['component_of_failure'][i],
            subcomponent=data['sub_component_of_failure'][i]
        ) for i in range(num_records)
    ]

    # Generate financial and status fields
    data['estimated_loss_amount'] = [f"${np.random.randint(1000, 50000)}" for _ in range(num_records)]

    subrogation_potential = np.random.choice(['Yes', 'No', 'Pending Review'], num_records, p=[0.3, 0.5, 0.2])
    data['subrogation_potential'] = subrogation_potential

    # Generate subrogation notes based on potential
    subrogation_notes = []
    for potential in subrogation_potential:
        if potential == 'Yes':
            notes = np.random.choice([
                "Manufacturer defect identified.",
                "Third-party liability established.",
                "Faulty installation by contractor.",
                "Product recall applicable.",
                "Negligence by service provider."
            ])
        elif potential == 'Pending Review':
            notes = np.random.choice([
                "Awaiting expert inspection.",
                "Investigating potential third-party liability.",
                "Reviewing product warranty information.",
                "Collecting additional evidence.",
                "Consulting with legal department."
            ])
        else:  # No
            notes = "No subrogation potential."
        subrogation_notes.append(notes)

    data['subrogation_notes'] = subrogation_notes

    data['preventable_loss'] = np.random.choice(['Yes', 'No'], num_records)

    preventive_actions = [
        "Regular maintenance recommended.",
        "Install monitoring system.",
        "Replace aging components.",
        "Improve security measures.",
        "Conduct professional inspections.",
        "Update to newer model.",
        "Implement proper insulation.",
        "Follow manufacturer guidelines.",
        "Upgrade to code-compliant fixtures.",
        "No preventive action identified."
    ]

    data['preventive_action'] = np.random.choice(preventive_actions, num_records)
    data['claim_status'] = np.random.choice(claim_statuses, num_records)

    # Generate recovery amount based on subrogation potential and claim status
    recovery_amounts = []
    for i in range(num_records):
        if data['subrogation_potential'][i] == 'Yes' and data['claim_status'][i] in ['Closed', 'Pending Subrogation']:
            # Extract the numeric value from Estimated Loss Amount
            est_loss = int(data['estimated_loss_amount'][i].replace('$', '').replace(',', ''))
            recovery = int(est_loss * np.random.uniform(0.2, 0.8))
            recovery_amounts.append(f"${recovery}")
        else:
            recovery_amounts.append("$0")

    data['recovery_amount'] = recovery_amounts
    data['underwriting_impact'] = np.random.choice(['Yes', 'No'], num_records)

    # Create DataFrame
    df = pd.DataFrame(data)

    # Create directory structure if it doesn't exist
    output_dir = os.path.join("output", f"property_claims_{current_date}")
    os.makedirs(output_dir, exist_ok=True)

    # Save to CSV
    output_file = os.path.join(output_dir, f"property_claims_{current_date}.csv")
    df.to_csv(output_file, index=False)

    print(f"Dataset created successfully: {output_file}")
    print(f"Number of records: {num_records}")

    # Return the DataFrame and file path for reference
    return df, output_file

# Execute the function
if __name__ == "__main__":
    df, file_path = create_property_claims_dataset(500)  # Create 500 records

    # Display the first few rows of the dataset
    print("\nSample of the dataset:")
    print(df.head())

    # Created/Modified files during execution:
    print("\nCreated/Modified files during execution:")
    print(file_path)