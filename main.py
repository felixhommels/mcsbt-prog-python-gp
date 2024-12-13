import os
from rapidfuzz import process
import investor
import market
import visualizer
import warnings

warnings.filterwarnings("ignore")

def create_exports_directory():
    # Check if the "Exports" directory exists
    if not os.path.exists('Exports'):
        os.makedirs('Exports')
    else:
        pass

def menu():
    print("Please select an option:")
    print("1. Load Data")
    print("2. View Overall Market Statistics")
    print("3. View Industry Statistics")
    print("4. Visualize Industry Group Statistics")
    print("5. View Top 20 Investors")
    print("6. Find Best Companies")
    print("7. Export Data")
    print("8. FAQ - Frequently Asked Questions")
    print("9. Exit Program")
    
def main():
    create_exports_directory()
    market_instance = None
    n = 0
    inv_weight = 0
    fund_weight = 0
    market_weight = 0

    print("Welcome to the VC Market Analysis Tool")

    while True:
        menu()
        choice = int(input("Enter the number of the operation you want to perform: \n"))

        if choice == 1: #Load Data
            print("Do you want to load data or use existing data?")
            print("1. Load Data")
            print("2. Existing Seed Data")
            print("3. Existing Series A Data")
            data_choice = int(input("Enter the number of the operation you want to perform: "))
            if data_choice == 1:
                file_path = input("Enter the path to the CSV file: ")
                market_instance = market.Market(file_path)
            elif data_choice == 2:
                market_instance = market.Market('InputData/Seed_Europe_min2mio_companies-25-11-2024.csv')
            elif data_choice == 3:
                market_instance = market.Market('InputData/seriesA_Europe_companies-25-11-2024.csv')
        
        elif choice == 2: #View Overall Market Statistics
            if market_instance:
                for key, value in market_instance.get_overall_statistics().items():
                    print(f"{key.title()}: {value}")
            else:
                print("No data loaded. Please load data first.")
        
        elif choice == 3: #View Industry Statistics
            if market_instance:
                industry_stats = market_instance.industry_group_statistics
                for industry, stats in industry_stats.items():
                    print(f"Industry: {industry}")
                    print(f"-Mean Total Funding: {stats['total_funding_mean']}")
                    print(f"-Median Total Funding: {stats['total_funding_median']}")
                    print(f"-Company Count: {stats['company_count']}")
                    print(f"-Mean Last Funding Amount: {stats['last_funding_mean']}")
                    print(f"-Median Last Funding Amount: {stats['last_funding_median']}")
                    print()
            else:
                print("No data loaded. Please load data first.")
        
        elif choice == 4: #Visualize Industry Group Statistics
            if market_instance: 
                stats = market_instance.industry_group_statistics
                industries = market_instance.get_industry_list()
                user_input = input("Enter Industries you want to visualize, sepearted by commas: ")
                user_industries = [industry.strip() for industry in user_input.split(",")]

                result_industries = []
                for user_industry in user_industries:
                    best_match, score, index = process.extractOne(user_industry, industries)
                    result_industries.append(best_match)

                visualizer.visualize_industry_group_statistics(market_instance, *result_industries)
                    
            else:
                print("No data loaded. Please load data first.")
        
        elif choice == 5: #View Top 20 Investors
            visualizer.visualize_top_20_investors()
        
        elif choice == 6: #Find Best Companies
            if market_instance:
                n = int(input("Enter how many companies we should find for you: "))
                inv_weight = float(input("Enter the weight for investor score: "))
                fund_weight = float(input("Enter the weight for funding difference score: "))
                market_weight = float(input("Enter the weight for market context score: "))
                best_companies = market_instance.best_companies(n, inv_weight, fund_weight, market_weight)

                for index, row in best_companies.iterrows():
                    print(row['Organization Name'])

                print("For detailed information, please use the export feature")
                print("For more information on how scores are computed, use the FAQ functionality. ")

            else:
                print("No data loaded. Please load data first.")
        
        elif choice == 7: #Export Data
            if market_instance: 
                investor.export_investor_data('top_20')
                investor.export_investor_data('all')
                market_instance.export_market_data()
                market_instance.export_top_companies(n, inv_weight, fund_weight, market_weight)
            else:
                print("No data loaded. Please load data first.")
        
        elif choice == 8: #FAQ - Frequently Asked Questions
            print(
                "1. How are the scores computed?\n"
                "Scores for investors are computed based on the number of investments and exits. The more investments and exits, the higher the score.\n"
                "Scores for companies are computed based on the investor score, funding difference score and market context score. The higher the score, the better the company. Scores are normalized to a range of 0 to 1.\n"
                "2. How are the best companies found?\n"
                "Best companies are found based on a formula which is a weighted sum of investor score, funding difference score and market context score. The weights are defined by the user.\n"
                "3. How are the top 20 investors found?\n"
                "Top 20 investors are found based on the number of investments and exits. The more investments and exits, the higher the score. The top 20 investors are then sorted by their score and the top 20 are returned.\n"
            )
        
        elif choice == 9: #Exit Program
            print("Thank you for using the VC Market Analysis Tool. Till next time!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()