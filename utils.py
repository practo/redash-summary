# Helper module for redash emailer

import yaml
import os


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

def get_config():
    config_file_path = "./config.yml"
    if not os.path.exists(config_file_path):
        logger.error("Missing Configuration File " + config_file_path)
        raise Exception("Missing Configuration File " + config_file_path)
    with open(config_file_path, "r") as conf_yaml:
        try:
            config = yaml.load(conf_yaml)
        except yaml.YAMLError, err:
            logger.error(err, exc_info=True)
            raise

    return config