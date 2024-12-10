#This files purpose is to clean the data and return a relevant dataframe for the application

import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    
    columns_to_keep = [
        "Organization Name",
        "Organization Name URL",
        "Full Description",
        "Founded Date",
        "Last Funding Date",
        "Number of Funding Rounds",
        "Founders",
        "Last Funding Type",
        "Top 5 Investors",
        "Industry Groups",
        "Total Funding Amount (in USD)",
        "Last Funding Amount (in USD)",
        "Number of Employees"
        ]
    df = df[columns_to_keep]

    #Using the df.loc method to apply a lambda function to the specified columns
    df.loc[:,"Founders"] = df["Founders"].apply(lambda x: x.split(', ') if isinstance(x, str) else None)
    df.loc[:,"Top 5 Investors"] = df["Top 5 Investors"].apply(lambda x: x.split(', ') if isinstance(x, str) else None)
    df.loc[:,"Industry Groups"] = df["Industry Groups"].apply(lambda x: x.split(', ') if isinstance(x, str) else None)

    return df