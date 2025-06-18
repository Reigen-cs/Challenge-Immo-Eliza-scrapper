import time
from threading import Thread
from time import perf_counter
import requests
from bs4 import BeautifulSoup
import json
import csv
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pandas as pd

def scrape_property_urls(base_url, page_number, url_collection):
    """
    Extracts property URLs from a specific page of the real estate website.
    
    Args:
        base_url (str): The foundation URL for property searches.
        page_number (int): The specific page to scrape.
        url_collection (list): Collection to store discovered property URLs.
    """
    target_url = f"{base_url}&page={page_number}"
    start_timer = perf_counter()
    response = requests.get(target_url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for element in soup.select('article.card.card--result div.card--result__body a.card__title-link'):
            url_collection.append(element.attrs["href"])
        elapsed_time = perf_counter() - start_timer
        print(f"Page {page_number} processed in {elapsed_time:.4f} seconds.")
    else:
        print(f"Failed to process page {page_number}")
    
def harvest_urls_from_range(website_url, first_page, last_page, url_storage):
    """
    Collects property URLs from a range of pages using concurrent processing.
    
    Args:
        website_url (str): The base website URL for property listings.
        first_page (int): The initial page number to start from.
        last_page (int): The final page number to process.
        url_storage (list): Storage container for collected property URLs.
    """
    page_range = list(range(first_page, last_page))
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda page: scrape_property_urls(website_url, page, url_storage), page_range)

def output_urls_to_file(file_destination, url_list):
    """
    Exports the collected property URLs to a CSV file format.
    
    Args:
        file_destination (str): The target file path for CSV export.
        url_list (list): Collection of property URLs to export.
    """
    print("Writing URLs to CSV file")
    with open(file_destination, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for link in url_list:
            writer.writerow([link])

def extract_nested_value(dictionary: dict, key_path: list, fallback: Any = None):
    """
    Extracts a deeply nested value from a dictionary using a sequence of keys.
    
    Args:
        dictionary (dict): The source dictionary to search.
        key_path (list): The sequence of keys to navigate through.
        fallback (Any, optional): The value to return if navigation fails. Defaults to None.

    Returns:
        Any: The discovered value or the fallback value.
    """
    current_obj = dictionary
    for key in key_path:
        if not current_obj or key not in current_obj:
            return fallback
        current_obj = current_obj[key]
    return current_obj

def determine_sale_category(property_data):
    """
    Identifies the category of property sale based on various flags.
    
    Args:
        property_data (dict): The complete property information.

    Returns:
        str: The identified sale category, or None if undetermined.
    """
    sale_flags = ["isPublicSale", "isNotarySale", "isLifeAnnuitySale", "isAnInteractiveSale", 
                  "isNewlyBuilt", "isInvestmentProject", "isUnderOption", "isNewRealEstateProject"]
    for flag in sale_flags:
        if extract_nested_value(property_data, ["flags", flag]) == True:
            return flag.replace("is", "")
    return None

def extract_property_details(property_index, property_url):
    """
    Retrieves detailed property information from a specific URL and processes the data.
    
    Args:
        property_index (int): The unique identifier for the property.
        property_url (str): The URL containing property details.

    Returns:
        tuple: The property index and dictionary containing processed property information.
    """
    response = requests.get(property_url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
    extracted_info = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.select('iw-load-advertisements')
        if len(elements) > 0 and elements[0].has_attr(":classified"):
            property_data = json.loads(elements[0].attrs[":classified"])
            extracted_info["typeOfSale"] = determine_sale_category(property_data)
    return property_index, extracted_info

def write_property_database(file_destination, column_headers, property_records):
    """
    Creates a CSV database file with property information.
    
    Args:
        file_destination (str): The target location for the CSV database.
        column_headers (list): The column names for the database structure.
        property_records (list): Collection of property data dictionaries.
    """
    with open(file_destination, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_headers)
        writer.writeheader()
        for record in property_records:
            writer.writerow(record)
    print("Property database created successfully.")

def sanitize_and_store_dataset(dataset_path):
    """
    Performs data cleaning operations and saves the refined dataset.
    
    Args:
        dataset_path (str): The location of the raw dataset file.
    """
    dataframe = pd.read_csv(dataset_path)
    dataframe.drop_duplicates(subset=['postal_code', 'street', 'number', 'box'], inplace=True)
    dataframe.dropna(how='all', inplace=True)
    dataframe.to_csv("data/cleaned_dataset.csv", index="house_index")

def run_scraping_pipeline():
    """
    Orchestrates the complete property data collection and processing workflow.
    """
    pipeline_start = perf_counter()
    collected_urls = []
    search_url_1950_1999 = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minConstructionYear=1950&maxConstructionYear=1999"
    search_url_2000_plus = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minConstructionYear=2000"
    target_urls = [search_url_1950_1999, search_url_2000_plus]
    for search_url in target_urls:
        harvest_urls_from_range(search_url, 1, 334, collected_urls)
    print(len(collected_urls))
    urls_file = 'Data/property_links.csv'
    output_urls_to_file(urls_file, collected_urls)
    
    time.sleep(30)
    final_output = "Data/all_properties_output.csv"
    sanitize_and_store_dataset(final_output)

if __name__ == "__main__":
    run_scraping_pipeline()