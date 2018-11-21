# Script to send tabular email of redash data
# This will send only top 10 data points 

import requests
from json2html import *
import json
import bs4

def get_html_table(jsonData):
	jsonData = jsonData['query_result']['data']['rows']
	jsonData = jsonData[:10]
	template = "<html><body><table cellpadding=10 border=1></table></body></html>"
	soup = bs4.BeautifulSoup(template)
	header_data = jsonData[1].keys()
	table_header_row = bs4.BeautifulSoup('<thead><tr></tr></thead>')
	for header_col in header_data:
		table_header_data = bs4.BeautifulSoup('<th bgcolor=#dddddd>' + header_col + '</th>')
		table_header_row.tr.append(table_header_data)
	soup.body.table.append(table_header_row)
	template = str(soup)
	return template

def __get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def parse_argument():
	parser = optparse.OptionParser()
    parser.add_option('-q', '--query',
                      dest="query_id",
                      default="",
                      type="string",
                      )
    parser.add_option('-e', '--email',
                      type='string',
                      action='callback',
                      callback=__get_comma_separated_args,
                      dest="recepient_emails",
                      default=[],
                      )
    options, remainder = parser.parse_args()

    return options

def get_query_details(query_id):
	return {}
	
def get_query_results():
	return {}

def send_email_alert(query_details, query_result, recepient_emails):
    message = get_html_table(query_result)
    request_url = 'https://api.mailgun.net/v3/<staging>/messages'
    response = requests.post(request_url, auth=('api', 'key'), data={
        'from': 'noreply@redash.practo.com',
        'to': 'sandeep.pandey@practo.com',
        'subject': 'Redash data veirfy',
        'html': message
    })
    # print response

options = parse_argument()
query_details = get_query_details(options.query_id)
query_result = get_query_results(options.query_id)
send_email_alert(query_details, query_result, options.recepient_emails)








