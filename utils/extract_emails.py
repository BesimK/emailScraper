import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


def extract_emails(filename):
    df = pd.read_excel(filename)
    emails = []

    for website in df['website']:
        if pd.notna(website):
            search_query = f'@gmail.com site:{website}'
            emails.extend(duckduckgo_search_emails(search_query))

    return emails


def duckduckgo_search_emails(query):
    url = f'https://duckduckgo.com/?q={query}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    emails = re.findall(r'[a-zA-Z0-9._%+-]+@gmail.com', soup.text)
    return emails
