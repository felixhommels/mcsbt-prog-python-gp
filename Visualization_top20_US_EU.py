import pandas as pd
import matplotlib.pyplot as plt
from investor import Investor

# Load the datasets
us_investors = pd.read_csv('/Users/cankuloglu/Desktop/Python Files/Python_Project/US_Investors_.csv')
eu_investors = pd.read_csv('/Users/cankuloglu/Desktop/Python Files/Python_Project/EU_Investors_.csv')

# Add a column indicating the region
us_investors['Region'] = 'US'
eu_investors['Region'] = 'EU'

# Combine the datasets
all_investors = pd.concat([us_investors, eu_investors], ignore_index=True)

# Add a new column 'Score' by creating Investor objects and calculating the score
all_investors['Score'] = all_investors.apply(
    lambda row: Investor(
        name=row['Organization/Person Name'],
        num_investments=row['Number of Investments'],
        num_exits=row['Number of Exits']
    ).calculate_score(), axis=1
)

# Filter top 20 investors from each region
top_20_us = all_investors[all_investors['Region'] == 'US'].nlargest(20, 'Score')
top_20_eu = all_investors[all_investors['Region'] == 'EU'].nlargest(20, 'Score')

# Plotting
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Horizontal bar chart for US investors
axes[0].barh(top_20_us['Organization/Person Name'], top_20_us['Score'], color='blue', label='US')
axes[0].set_title('Top 20 US Investors by Score', fontsize=16)
axes[0].set_ylabel('Investor', fontsize=12)
axes[0].invert_yaxis()  # Align bars from top to bottom
axes[0].legend()

# Add score labels for US investors
for i, (score, name) in enumerate(zip(top_20_us['Score'], top_20_us['Organization/Person Name'])):
    axes[0].text(score, i, f"{score}", va='center', ha='left', fontsize=10)

# Horizontal bar chart for EU investors
axes[1].barh(top_20_eu['Organization/Person Name'], top_20_eu['Score'], color='green', label='EU')
axes[1].set_title('Top 20 EU Investors by Score', fontsize=16)
axes[1].set_ylabel('Investor', fontsize=12)
axes[1].invert_yaxis()  # Align bars from top to bottom
axes[1].legend()

# Add score labels for EU investors
for i, (score, name) in enumerate(zip(top_20_eu['Score'], top_20_eu['Organization/Person Name'])):
    axes[1].text(score, i, f"{score}", va='center', ha='left', fontsize=10)

# Shared x-axis
plt.xlabel('Score', fontsize=14)

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()








