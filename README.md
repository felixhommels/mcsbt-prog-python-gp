# VC Market Analysis Tool

## Overview

The VC Market Analysis Tool is a Python application designed to analyze venture capital market data. It allows users to load data from CSV files, view overall market statistics, visualize industry group statistics, find the best companies based on various metrics, and export data for further analysis. The application leverages machine learning techniques to predict funding amounts and assess company performance based on investor activity.

## Features

- **Load Data**: Import data from CSV files or use existing datasets.
- **View Statistics**: Access overall market statistics and industry-specific statistics.
- **Visualize Data**: Generate visual representations of industry group statistics and top investors.
- **Find Best Companies**: Identify the best companies based on user-defined criteria.
- **Export Data**: Save statistics and company data to CSV files for external use.
- **FAQ Section**: Provides answers to common questions regarding the scoring and analysis methods used in the application.

## Requirements

To run this application, you need to have the following Python packages installed:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- rapidfuzz

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## File Structure

```
.
├── InputData/
│   ├── EU_Investors.csv
│   ├── US_Investors.csv
│   ├── Seed_Europe_min2mio_companies-25-11-2024.csv
│   └── seriesA_Europe_companies-25-11-2024.csv
├── Exports/
├── main.py
├── market.py
├── investor.py
├── visualizer.py
└── utils.py
```

## Usage

1. **Run the Application**: Execute the `main.py` file to start the application.

   ```bash
   python main.py
   ```

2. **Menu Options**: Follow the on-screen prompts to select an option from the menu. You can load data, view statistics, visualize data, find best companies, export data, or exit the program.

3. **Load Data**: Choose to load your own data or use existing datasets provided in the `InputData` directory.

4. **View Statistics**: After loading data, you can view overall market statistics or industry-specific statistics.

5. **Visualize Data**: Input the industries you want to visualize, and the application will generate bar charts for the selected industries.

6. **Find Best Companies**: Specify the number of companies to find and the weights for investor score, funding difference, and market context score.

7. **Export Data**: Export the statistics and top companies to CSV files in the `Exports` directory.

## Data Cleaning

The application includes a data cleaning function that ensures only relevant columns are retained and that certain fields are processed into lists for easier analysis.

## Machine Learning Model

The application uses a Random Forest Regressor to predict the expected next funding amount for companies based on historical funding data and other relevant features.

## Contributing

Contributions to the VC Market Analysis Tool are welcome! If you have suggestions for improvements or new features, please feel free to submit a pull request.
