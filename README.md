# Brighthive Mock Data Generator

This repository contains scripts to generate synthetic datasets that support Brighthive demos and storytelling for various use cases. The generated data is designed to be realistic and representative of real-world scenarios while maintaining privacy and security.

## Purpose

The mock data generator serves several key purposes:
- Create realistic datasets for demonstration purposes
- Support storytelling and use case presentations
- Enable testing and development without using real production data
- Provide consistent, reproducible data for demos and training

## Getting Started

### Prerequisites

1. Python 3.7 or higher
2. Required Python packages (install using pip):
   ```bash
   pip install -r requirements.txt
   ```

### Directory Structure

```
brighthive-mock-data/
├── documentation/     # Documentation files
├── output/           # Generated data files
├── scripts/          # Data generation scripts
└── requirements.txt  # Python dependencies
```

### Generating Datasets

#### Step-by-Step Example: Generating CRM Data

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the data generation script. Here is an example for CRM data:
   ```bash
   python scripts/generate_crm_data.py
   ```

5. The script will:
   - Create an `output` directory if it doesn't exist
   - Generate synthetic CRM data with realistic fields
   - Save the data as a CSV file in the `output` directory with the current date
   - The output file will be named `crm_data_MM-DD.csv`

5. Verify the generated data:
   - Check the `output` directory for the new CSV file


## Available Datasets

The repository includes generators for various types of data:
- CRM data
- Healthcare data
- Financial data
- Student data
- Web analytics data
- Health devices data

Each script generates data specific to its domain while maintaining realistic relationships and patterns.

## Contributing

When adding new data generators:
1. Follow the existing code structure and patterns
2. Include appropriate documentation
3. Use realistic data ranges and distributions
4. Ensure data privacy and security
5. Add your script to this README's "Available Datasets" section