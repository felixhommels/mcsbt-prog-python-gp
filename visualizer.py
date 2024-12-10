import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import market
import matplotlib.ticker as ticker
import os
import investor

    
def visualize_industry_group_statistics(market_obj: market.Market, *industry_groups: str):
    data = market_obj.industry_group_statistics
    industry_groups = [group for group in industry_groups] #List Comprehension to convert tuple to list
    repeated_industry_groups = [group for group in industry_groups for _ in range(4)]

    metric = ["Mean Total Funding", "Median Total Funding", "Mean Last Funding Amount", "Median Last Funding Amount"] * len(industry_groups)
    value = [data[group]["total_funding_mean"] for group in industry_groups] + [data[group]["total_funding_median"] for group in industry_groups] + [data[group]["last_funding_mean"] for group in industry_groups] + [data[group]["last_funding_median"] for group in industry_groups]

    seaborn_data = pd.DataFrame({
        "Industry": repeated_industry_groups,
        "Metrics": metric,
        "Values": value
    })

    plt.figure(figsize=(10, 6))
    
    sns.barplot(x="Industry", y="Values", hue="Metrics", data=seaborn_data, palette="Blues")

    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x/1000000)}M'))

    plt.xlabel("Industry")
    plt.ylabel("Values (in millions)")
    plt.title("Industry Group Funding Statistics")
    
    plt.show()

def visualize_top_20_investors(investor_data=investor.investor_data_frame()):
    # Filter top 20 investors from each region
    top_20_us = investor_data[investor_data['Region'] == 'US'].nlargest(20, 'Score')
    top_20_eu = investor_data[investor_data['Region'] == 'EU'].nlargest(20, 'Score')

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
    plt.show()
