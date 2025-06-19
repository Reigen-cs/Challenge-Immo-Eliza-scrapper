# Real Estate Data Scraping and Processing Pipeline

This project consists of two main Python scripts that work together to scrape, process, and clean real estate property data from Immoweb (Belgian real estate website).

## Project Overview

The pipeline performs the following operations:
1. **Data Scraping**: Collects property URLs from multiple pages of search results
2. **Data Extraction**: Extracts detailed property information from individual listings
3. **Data Cleaning**: Removes duplicates, handles missing values, and optimizes data types
4. **Data Export**: Saves the processed data to CSV files

## Files Description

### main.py
The main scraping script that handles:
- **URL Collection**: Scrapes property URLs from search result pages
- **Concurrent Processing**: Uses ThreadPoolExecutor for efficient multi-page scraping
- **Data Extraction**: Extracts property details from individual property pages
- **Sale Type Detection**: Identifies different types of property sales (public, notary, etc.)
- **CSV Export**: Saves collected data to CSV files

### clean_dataset.py
The data processing script that handles:
- **Data Import**: Loads raw CSV data into pandas DataFrames
- **Data Cleaning**: Removes duplicates and empty rows
- **Type Optimization**: Converts columns to appropriate data types (categorical, etc.)
- **Data Export**: Saves cleaned data with proper indexing

## Requirements

```python
pandas
requests
beautifulsoup4
concurrent.futures
```

## Installation

1. Clone or download the project files
2. Install required dependencies:
   ```bash
   pip install pandas requests beautifulsoup4
   ```
3. Create the following directory structure:
   ```
   Data/
   ├── property_links.csv (generated)
   ├── all_properties_output.csv (generated)
   └── cleaned_dataset.csv (generated)
   ```

## Usage

### Running the Complete Pipeline

1. **Execute the main scraping script**:
   ```bash
   python main.py
   ```
   This will:
   - Scrape property URLs from Immoweb
   - Save URLs to `Data/property_links.csv`
   - Process the data and save to `Data/all_properties_output.csv`

2. **Execute the data cleaning script**:
   ```bash
   python clean_dataset.py
   ```
   This will:
   - Load the raw data from `Data/all_properties_output.csv`
   - Clean and process the data
   - Save the cleaned dataset to `Data/cleaned_dataset.csv`

### Key Functions

#### main.py Functions:
- `scrape_property_urls()`: Extracts property URLs from a single page
- `harvest_urls_from_range()`: Processes multiple pages concurrently
- `extract_property_details()`: Gets detailed information from property pages
- `determine_sale_category()`: Identifies the type of property sale
- `write_property_database()`: Exports data to CSV format

#### clean_dataset.py Functions:
- `import_csv_data()`: Loads CSV data into pandas DataFrame
- `process_and_sanitize_data()`: Performs comprehensive data cleaning
- `export_processed_data()`: Saves cleaned data with proper indexing

## Data Processing Features

### Data Cleaning Operations:
- **Duplicate Removal**: Based on postal code, street, number, and box
- **Empty Row Elimination**: Removes completely empty entries
- **Data Type Optimization**: Converts categorical columns for better memory usage
- **Outlier Detection**: Removes unrealistic entries (e.g., properties with 200+ bedrooms)
- **Missing Value Handling**: Replaces NaN values with None

### Search Criteria:
The scraper targets properties with:
- **Construction Year**: 1950-1999 and 2000+
- **Property Types**: Houses and apartments
- **Location**: Belgium
- **Listing Type**: For sale

## Output Files

1. **property_links.csv**: Contains all scraped property URLs
2. **all_properties_output.csv**: Raw property data with detailed information
3. **cleaned_dataset.csv**: Processed and cleaned dataset ready for analysis

[See result here](https://rowzero.io/workbook/67BF8E5F6B165532DF351546/0)

## Performance Features

- **Concurrent Processing**: Uses ThreadPoolExecutor with 10 workers for efficient scraping
- **Memory Optimization**: Categorical data types reduce memory usage
- **Error Handling**: Robust error handling for network requests
- **Progress Tracking**: Real-time feedback on scraping progress

## Notes

- The script includes a 30-second delay between major operations to respect the website's rate limits
- User-Agent headers are used to mimic browser requests
- The pipeline processes  333 pages 
- Data is automatically indexed and sorted for consistent output

## Troubleshooting

- Ensure stable internet connection for web scraping
- Check that the `Data/` directory exists before running scripts
- Verify that all required Python packages are installed
- Monitor memory usage for large datasets
- Prepare way to be hidden / change IP.

## Legal Considerations

This tool is designed for educational and research purposes. Please ensure compliance with the target website's robots.txt and terms of service when using this scraper.