import pandas as pd
import random
from faker import Faker
import os
from datetime import datetime

# Initialize Faker
fake = Faker()

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "../output")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define constants for mock data
sales_stages = ["Lead", "Prospect", "Negotiation", "Closed Won", "Closed Lost"]
industries = ["Technology", "Manufacturing", "Healthcare", "Finance", "Retail"]
regions = ["North America", "Europe", "Asia", "South America", "Australia"]
lead_sources = ["Website Inquiry", "Trade Show", "Referral", "Cold Call", "Email Campaign"]
customer_types = ["New Customer", "Existing", "Returning"]
products_services = ["SaaS Platform", "Consulting", "Hardware", "Cloud Services", "Training"]
deal_priorities = ["High", "Medium", "Low"]

# Generate mock data
data = []
for _ in range(1000):
    customer_name = fake.company()
    deal_value = round(random.uniform(5000, 100000), 2)  # Random deal value between $5,000 and $100,000
    sales_stage = random.choice(sales_stages)
    close_date = fake.date_between(start_date="-1y", end_date="today")
    sales_rep = fake.name()
    industry = random.choice(industries)
    region = random.choice(regions)
    lead_source = random.choice(lead_sources)
    probability = random.randint(10, 100)  # Probability percentage
    contract_length = random.randint(1, 36)  # Contract length in months
    customer_size = random.randint(10, 1000)  # Number of employees
    annual_revenue = round(random.uniform(1000000, 50000000), 2)  # Annual revenue in dollars
    customer_type = random.choice(customer_types)
    engagement_score = random.randint(0, 100)  # Engagement score
    last_contact_date = fake.date_between(start_date="-6m", end_date="today")
    next_follow_up_date = fake.date_between(start_date="today", end_date="+1m")
    product_service = random.choice(products_services)
    competitor_involved = random.choice(["Yes", "No"])
    deal_priority = random.choice(deal_priorities)
    notes_comments = fake.sentence()

    # Append row to data
    data.append([
        customer_name, deal_value, sales_stage, close_date, sales_rep, industry, region,
        lead_source, probability, contract_length, customer_size, annual_revenue,
        customer_type, engagement_score, last_contact_date, next_follow_up_date,
        product_service, competitor_involved, deal_priority, notes_comments
    ])

# Create DataFrame
columns = [
    "Customer Name", "Deal Value", "Sales Stage", "Close Date", "Sales Rep", "Industry", "Region",
    "Lead Source", "Probability (%)", "Contract Length (Months)", "Customer Size (Employees)",
    "Annual Revenue ($)", "Customer Type", "Engagement Score", "Last Contact Date",
    "Next Follow-Up Date", "Product/Service", "Competitor Involved", "Deal Priority", "Notes/Comments"
]
df = pd.DataFrame(data, columns=columns)

# Generate file name with current date
current_date = datetime.now()
file_name = f"crm_data_{current_date.strftime('%m-%d')}.csv"
output_path = os.path.join(output_dir, file_name)

# Save to CSV
df.to_csv(output_path, index=False)

# Output file name
print(f"Mock data generated and saved to {output_path}")

# Created/Modified files during execution:
print(f"Created file: {output_path}")