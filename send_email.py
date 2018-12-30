# Script to send tabular email of redash data
# This will send only top 10 data points 

import requests
from json2html import *
import json
import bs4
from utils import parse_argument, get_config, send_email
import csv

config = get_config()
redash_config = config['redash']
def get_html_table(jsonData, query_id):
  jsonData = jsonData['query_result']['data']['rows']
  jsonData = jsonData[:10]
  redash_url = redash_config['redash_query_url'] + query_id
  template = "<html><body><table cellpadding=10 border=1></table></body></html>"
  soup = bs4.BeautifulSoup(template, 'html.parser')
  if len(jsonData) > 0:
    header_data = jsonData[0].keys()
  else:
    return str(soup)
  table_header_row = bs4.BeautifulSoup('<thead><tr></tr></thead>', 'html.parser')
  for header_col in header_data:
    table_header_data = bs4.BeautifulSoup('<th bgcolor=#dddddd>' + header_col + '</th>', 'html.parser')
    table_header_row.tr.append(table_header_data)
  soup.body.table.append(table_header_row)
  for row in jsonData:
    table_row = bs4.BeautifulSoup('<tr></tr>', 'html.parser')
    for header in header_data:
      table_row_data = bs4.BeautifulSoup('<td>' + str(row[header]) + '</td>', 'html.parser')
      table_row.append(table_row_data)
    soup.body.table.append(table_row)
  table_url_link = bs4.BeautifulSoup("<a href="+ redash_url + ">View more on redash</a>", 'html.parser')
  soup.body.append(table_url_link)
  template = str(soup)
  return template

def get_query_details(query_id):
  query_url = redash_config['query_url'] + query_id
  query_details = requests.get(query_url, 
    params={'api_key': redash_config['user_api_key']}).json()
  return query_details
  
def get_query_results(query_id):
  query_url = redash_config['query_url'] + query_id + "/results.json"
  query_results = requests.get(query_url, 
        params={'api_key': redash_config['user_api_key']}).json()
  return query_results

# function to put the refresh query logic
def put_query_refresh():
  pass

def send_query_dump(query_id):
  with requests.Session() as s:
    CSV_URL = redash_config['query_url'] + query_id + "/results.csv"
    download = s.get(CSV_URL,
      params={'api_key': redash_config['user_api_key']})
    temp_file_name = query_id + '_results.csv'
    with open(temp_file_name, 'w') as temp_file:
      temp_file.writelines(download.content)
    return temp_file_name

def send_email_alert(query_details, query_result, recepient_emails, query_id, file_name):
  message = get_html_table(query_result, query_id)
  send_email(recepient_emails, query_details['name'], message, file_name)

options = parse_argument()
query_details = get_query_details(options.query_id)
query_result = get_query_results(options.query_id)
temp_file_name = None
if options.send_dump:
  temp_file_name = get_csv_dump(options.query_id)
send_email_alert(query_details, query_result, 
  options.recepient_emails, options.query_id, temp_file_name)
