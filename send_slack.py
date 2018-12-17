import os
from slackclient import SlackClient
from utils import parse_argument, get_config, send_email
import bs4
import pandas as pd
import requests

config = get_config()
redash_config = config['redash']
slack_config = config['slack']
slack_token = slack_config['token']
sc = SlackClient(slack_token)

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

def send_slack_alert(query_details, query_result,channel,query_id):
	# message = get_html_table(query_result, query_id)
	jsonData = query_result['query_result']['data']['rows'];
	jsonData = jsonData[:10]
	header_data = jsonData[0].keys()
	pandadata = pd.DataFrame(jsonData, columns=header_data);
	message_text = "*"+query_details['name'] + "* \n" \
					+ "```"+pandadata.to_string(index=False)+"```"
	message_text = message_text + "\n click "  \
					+ redash_config['redash_query_url'] + str(query_id)
	sc.api_call(
	  "chat.postMessage",
	  channel=channel,
	  text= message_text,
	  mrkdwn=True
	)

options = parse_argument()
query_details = get_query_details(options.query_id)
query_result = get_query_results(options.query_id)
send_slack_alert(query_details,query_result,options.channel,options.query_id)