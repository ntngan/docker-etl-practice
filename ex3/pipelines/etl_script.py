from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime, timezone, timedelta

def extract(**kwargs):
    # Selenium setup
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Load the webpage
    driver.get("https://en.wikipedia.org/wiki/List_of_countries_with_KFC_franchises")
    html_page = driver.page_source    
    soup = BeautifulSoup(html_page, 'html.parser')

    # Find the desired table
    table = soup.find_all('table')[2]

    # Extract headers
    headers = [th.get_text(strip=True) for th in table.thead.find_all('th')]

    # Extract table rows
    table_content = []
    for tr in table.tbody.find_all('tr'):
        td_tags = tr.find_all('td')
        td_texts = [td.get_text(strip=True) for td in td_tags]
        table_content.append(td_texts)

    # Create DataFrame
    df = pd.DataFrame(table_content, columns=headers)
    kwargs['ti'].xcom_push(key='extracted_data', value=df)
    driver.quit()

def transform(**kwargs):
    df = kwargs['ti'].xcom_pull(key='extracted_data', task_ids='extract_task')
    columns_to_clean = ['Year entered', 'Outlets', 'First outlet', 'Owner/major operator', 'Notes']  # Add column names you want to clean
    # Clean each column in the list
    for col in columns_to_clean:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(
                lambda x: re.sub(r'\[.*?\]', '', x).strip()  # Remove content inside square brackets
            ) \
            .replace('?', '') \
            .replace('N/A', '')
    print(df[columns_to_clean].head())
    kwargs['ti'].xcom_push(key='transformed_data', value=df)

def load(**kwargs):
    # Save to CSV
    df = kwargs['ti'].xcom_pull(key='transformed_data', task_ids='transform_task')
    utc_plus_7 = timezone(timedelta(hours=7))
    now = datetime.now(utc_plus_7).strftime("%Y-%m-%d_%H-%M-%S")
    df.to_csv(f'./data/{now}.csv', index=False)

