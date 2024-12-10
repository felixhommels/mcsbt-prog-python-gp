import pandas as pd
import os

class Investor:
    def __init__(self, name, num_investments, num_exits):
        self.name = name
        self.num_investments = num_investments
        self.num_exits = num_exits

    def calculate_score(self):
        return (self.num_investments * 1) + (self.num_exits * 2)

    def __str__(self):
        return f"Investor(name={self.name}, score={self.calculate_score()})"

def investor_data_frame(file1='InputData/EU_Investors.csv', file2='InputData/US_Investors.csv'):
    eu_investors = pd.read_csv(file1)
    us_investors = pd.read_csv(file2)

    combined_investor_data = pd.concat([eu_investors, us_investors])
    combined_investor_data['Region'] = ['EU'] * len(eu_investors) + ['US'] * len(us_investors)

    investors = [
        Investor(
            name=row['Organization/Person Name'],
            num_investments=row['Number of Investments'],
            num_exits=row['Number of Exits']
        )
        for i, row in combined_investor_data.iterrows()
    ]

    #Using list comprehension and polymorphism to calculate the score for each investor and save it in the dataframe
    combined_investor_data['Score'] = [inv.calculate_score() for inv in investors] 

    return combined_investor_data

def get_top_20_investors(file1='InputData/EU_Investors.csv', file2='InputData/US_Investors.csv'):
    # Use the investor_data_frame function to get combined investor data
    us_eu_investors = investor_data_frame(file1, file2)

    top_investors = sorted(us_eu_investors.itertuples(), key=lambda inv: inv.Score, reverse=True)[:20]

    top_investors_data = pd.DataFrame({
        'Organization/Person Name': [inv._1 for inv in top_investors],  #where _1 is first column
        'Region': [inv.Region for inv in top_investors],
        'Score': [inv.Score for inv in top_investors],
    })

    return top_investors_data, us_eu_investors  # Return both dataframes for further processing

def export_investor_data(scope):
    if scope == 'top_20':
        top_20_df, _ = get_top_20_investors('InputData/EU_Investors.csv', 'InputData/US_Investors.csv')
        top_20_df.to_csv('Exports/Top_20_Investors_with_Region.csv', index=False)
    elif scope == 'all':
        all_investors_df = investor_data_frame('InputData/EU_Investors.csv', 'InputData/US_Investors.csv')
        all_investors_df.to_csv('Exports/All_Investors_with_Scores_and_Region.csv', index=False)
    else:
        raise ValueError("Invalid scope. Please specify 'top_20' or 'all'.")
