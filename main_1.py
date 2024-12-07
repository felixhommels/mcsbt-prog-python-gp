import pandas as pd
from investor import Investor

# Load the combined dataset
us_eu_investors = pd.read_csv("/Users/cankuloglu/Desktop/Python Files/Python_Project/Combined_Investors_with_Scores_and_Region.csv")

# Create Investor objects
investors = [
    Investor(
        name=row['Organization/Person Name'],
        num_investments=row['Number of Investments'],
        num_exits=row['Number of Exits']
    )
    for _, row in us_eu_investors.iterrows()
]

# Sort investors by score and select the top 20
top_investors = sorted(investors, key=lambda inv: inv.calculate_score(), reverse=True)[:20]

# Extract top 20 investors as a DataFrame
top_investors_data = pd.DataFrame({
    'Organization/Person Name': [inv.name for inv in top_investors],
    'Score': [inv.calculate_score() for inv in top_investors],
})

# Merge with the original dataset to include the 'Region' column
top_investors_df = pd.merge(
    top_investors_data,
    us_eu_investors[['Organization/Person Name', 'Region']],
    on='Organization/Person Name',
    how='left'
)

# Print the top 20 investors
print("Top 20 Investors:")
print(top_investors_df)

# Save the top 20 investors to a new CSV file
output_file = "/Users/cankuloglu/Desktop/Python Files/Python_Project/Top_20_Investors_with_Region.csv"
top_investors_df.to_csv(output_file, index=False)
print(f"Top 20 investors saved to {output_file}")