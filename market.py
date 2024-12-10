import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
import json
import utils
import investor

class Market:
    def __init__(self, file_path: str):
        self.raw_df = pd.read_csv(file_path)
        self.file_validity()
        self.cleaned_df = utils.clean_data(self.raw_df)
        self.investors = investor.investor_data_frame()
        self.overall_statistics = self.get_overall_statistics()
        self.industry_group_statistics = self.industry_group_statistics()
        self.predictive_model = self.train_predictive_model()
        
    #First check whether the file is valid for this application (Crunchbase format)    
    def file_validity(self):
        benchmark_file = pd.read_csv('InputData/seriesA_Europe_companies-25-11-2024.csv')
        if list(self.raw_df.columns) == list(benchmark_file.columns):
            pass
        else:
            raise ValueError('File is not valid, the column layout is not compatible with this application')
        
        #Check whether the file is all of the same funding round (e.g. Series A)
        if len(self.raw_df['Last Funding Type'].unique()) == 1:
            pass
        else:
            raise ValueError('File is not valid, there is a mix of different funding rounds')
        
    def get_industry_list(self):
        exploded_df = self.cleaned_df.explode('Industry Groups')
        unique_industries = exploded_df['Industry Groups'].unique().tolist()
        return unique_industries
        
    def get_overall_statistics(self):
        #Total Funding Stats
        total_funding_stats = {
            'mean_total_funding': int(self.cleaned_df['Total Funding Amount (in USD)'].mean()),
            'median_total_funding': int(self.cleaned_df['Total Funding Amount (in USD)'].median())
        }
        
        #Last Funding Stats
        last_funding_stats = {
            'mean_last_funding': int(self.cleaned_df['Last Funding Amount (in USD)'].mean()),
            'median_last_funding': int(self.cleaned_df['Last Funding Amount (in USD)'].median())
        }
        
        all_stats = {**total_funding_stats, **last_funding_stats} #Using Kwargs to unpack the dictionaries
        return all_stats
    
    def industry_group_statistics(self):
        # Create a new dataframe with exploded industry groups since there are multiple industries per company
        exploded_df = self.cleaned_df.explode('Industry Groups')
        
        # Group by individual industries and calculate statistics
        industry_stats = exploded_df.groupby('Industry Groups').agg({
            'Total Funding Amount (in USD)': ['mean', 'median', 'count'],
            'Last Funding Amount (in USD)': ['mean', 'median']
        }).round(0)
        
        simplified_stats = {}
        for industry in industry_stats.index: #Using index to get the unique industry name
            simplified_stats[industry] = {
                'total_funding_mean': int(industry_stats.loc[industry,  ('Total Funding Amount (in USD)', 'mean')]),
                'total_funding_median': int(industry_stats.loc[industry, ('Total Funding Amount (in USD)', 'median')]),
                'company_count': int(industry_stats.loc[industry, ('Total Funding Amount (in USD)', 'count')]),
                'last_funding_mean': int(industry_stats.loc[industry, ('Last Funding Amount (in USD)', 'mean')]),
                'last_funding_median': int(industry_stats.loc[industry, ('Last Funding Amount (in USD)', 'median')])
            }

        return simplified_stats
    
    def train_predictive_model(self):
        X = pd.DataFrame()

        # Convert date columns to datetime before subtraction
        self.cleaned_df['Last Funding Date'] = pd.to_datetime(self.cleaned_df['Last Funding Date'])
        self.cleaned_df['Founded Date'] = pd.to_datetime(self.cleaned_df['Founded Date'])
        
        X['days_since_founding'] = (self.cleaned_df['Last Funding Date'] - self.cleaned_df['Founded Date']).dt.days
        X['days_since_founding_log'] = np.log1p(X['days_since_founding'])
        
        # Add funding-related features
        X['total_funding'] = self.cleaned_df['Total Funding Amount (in USD)']
        X['funding_rounds'] = self.cleaned_df['Number of Funding Rounds']
        X['avg_funding_per_round'] = X['total_funding'] / X['funding_rounds']
        X['funding_velocity'] = X['total_funding'] / X['days_since_founding']
        
        # Add industry count as a feature instead of dummies
        X['industry_count'] = self.cleaned_df['Industry Groups'].apply(lambda x: len(x) if x is not None else 0)

        # Target variable: Last funding amount
        y = self.cleaned_df['Last Funding Amount (in USD)']

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_scaled, y)

        # Add predictions to cleaned_df
        self.cleaned_df['Expected Next Funding'] = model.predict(X_scaled)
        
        self.cleaned_df['Funding Difference'] = self.cleaned_df['Expected Next Funding'] - self.cleaned_df['Last Funding Amount (in USD)']
        
        # Store model and scaler if needed for future predictions
        self.model = model
        self.scaler = scaler
        self.feature_columns = X.columns
        
        # Calculate performance using cross-validation
        cv_scores = cross_val_score(model, X_scaled, y, cv=5)
        
        return {
            'cross_val_scores': cv_scores,
            'mean_cv_score': cv_scores.mean(),
            'feature_importance': dict(zip(X.columns, model.feature_importances_))
        }
    
    def best_companies(self, n: int, inv_weight: float, fund_weight: float, market_weight: float):
        desired_amount = n
        companies = self.cleaned_df
        
        #Get the investor score sum
        companies['Investor Score Sum'] = 0
        
        for index, row in companies.iterrows():
            investor_list = row['Top 5 Investors'] if isinstance(row['Top 5 Investors'], list) else []
            
            investor_scores = [self.investors.loc[self.investors['Organization/Person Name'] == investor, 'Score'].values[0] 
                               for investor in investor_list if investor in self.investors['Organization/Person Name'].values]
            companies.at[index, 'Investor Score Sum'] = sum(investor_scores)
        
        #Normalize the investor score sum
        companies['Investor Score Sum'] = companies['Investor Score Sum'] / companies['Investor Score Sum'].max()
    
        #Normalize Funding Difference
        companies['Funding Difference'] = companies['Funding Difference'] / companies['Funding Difference'].max()


        #Perform Overall Market Context Score based on overall statistics
        companies['Market Context Score'] = 0

        for index, row in companies.iterrows():
            total_fund_median = self.overall_statistics['median_total_funding']
            last_fund_median = self.overall_statistics['median_last_funding']
            
            # Calculate scores based on total funding and last funding
            total_funding_score = row['Total Funding Amount (in USD)'] / total_fund_median
            last_funding_score = row['Last Funding Amount (in USD)'] / last_fund_median
            
            # Average the two scores
            companies.at[index, 'Market Context Score'] = (total_funding_score + last_funding_score) / 2

        #Peform Overall Score based on the weights
        companies['Overall Score'] = 0
        companies['Overall Score'] = (companies['Investor Score Sum'] * inv_weight) + (companies['Funding Difference'] * fund_weight) + (companies['Market Context Score'] * market_weight)

        sorted_companies = companies.sort_values(by='Overall Score', ascending=False).copy()
        top_n_companies = sorted_companies[:n]
        return top_n_companies

    def export_market_data(self):
        overall_stats_file = 'Exports/Overall_Statistics.txt'
        with open(overall_stats_file, 'w') as file:
            for key, value in self.overall_statistics.items():
                file.write(f"{key}: {value}\n")

        industry_stats_file = 'Exports/Industry_Group_Statistics.csv'
        industry_stats_df = pd.DataFrame(self.industry_group_statistics).T
        industry_stats_df.to_csv(industry_stats_file, index=True)

    def export_top_companies(self, n: int, inv_weight: float, fund_weight: float, market_weight: float):
        top_companies = self.best_companies(n, inv_weight, fund_weight, market_weight)
        top_companies_file = 'Exports/Top_Companies.csv'
        top_companies.to_csv(top_companies_file, index=False)


