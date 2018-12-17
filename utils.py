# Helper module for redash emailer

import yaml
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import optparse

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
    parser.add_option('-c', '--channel',
                      type='string',
                      dest="channel",
                      default=[],
                      )

    options, remainder = parser.parse_args()

    return options

def get_config():
    config_file_path = "./config.yml"
    if not os.path.exists(config_file_path):
        logger.error("Missing Configuration File " + config_file_path)
        raise Exception("Missing Configuration File " + config_file_path)
    with open(config_file_path, "r") as conf_yaml:
        try:
            config = yaml.load(conf_yaml)
        except yaml.YAMLError, err:
            print err
            raise

    return config

def send_email(recipients, subject, html_data):
    config = get_config()
    smpt_config = config['smtp']
    server = smtplib.SMTP(smpt_config['host'], smpt_config['port'])
    server.ehlo()
    server.starttls()
    server.login(smpt_config['login'], smpt_config['password'])
    from_address = 'noreply@redash.practo.com'
    for recipient in recipients:
        msg = MIMEMultipart()
        msg['Subject'] = 'Redash:' + subject
        msg['From'] = from_address
        msg['To'] = recipient
        msg.attach(MIMEText(html_data, 'html'))
        server.sendmail(from_address, recipient, msg.as_string())
    server.quit()