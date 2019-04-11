#!/usr/bin/env python
# -*- coding utf-8 -*-

"""
backup-choco-installed.py

Description:
  Lists installed chocolatey packages and outputs a file listing packages and a script that allows reinstallation
  equivalent of 'choco list -lo > choco-installed.txt'

USAGE: 
  python backup-choco-installed.py

Created: 13:54:24 Saturday 05 May 2018
Modified: 09:38:58 Thursday 10 May 2018 cleanup
Modified: 12:45:52 Thursday 11 April 2019 add logging and click modules
"""

__author__  = ""
__email__   = ""
__version__ = "0.1.0"
__status__  = "Dev"

import subprocess
import os
import re
import datetime
import configparser
from datetime import datetime
import sys
import logging
import click

# ---------------------------------------- 
# Configuration
DEFAULT_CONFIG_FILE = 'config.ini'
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# This configuration can be picked up from config.ini file
DEFAULT_OUTPUT_FOLDER= os.path.dirname(sys.argv[0])
DEFAULT_CONFIG_FILE=os.path.join(os.path.dirname(sys.argv[0]), DEFAULT_CONFIG_FILE)
DEFAULT_OUTPUT_FILE = 'choco-installed-versions_{}.txt'.format(timestamp)
DEFAULT_REINSTALL_SCRIPT = 'choco-reinstall-{}.ps1'.format(timestamp)
# ---------------------------------------- 

# LOGGER = logging.getLOGGER('backup-choco-installed')
LOGGER = logging.getLogger(__name__ + '.LOGGER')
CONSOLE_HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('[%(filename)s:%(lineno)s %(asctime)s %(name)-12s %(levelname)-6s - %(funcName)s()] %(message)s')
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

def get_config(config_file):
  LOGGER.info(f'Entering method')
  LOGGER.debug(f'config_file = {config_file}')
  config = configparser.ConfigParser()

  # check for config file
  if not os.path.isfile(config_file):
    LOGGER.error('FileNotFound')
    raise FileNotFoundError('The default config file was not found at path: "{}"'.format(config_file))

  config.read(config_file)

  output_folder = DEFAULT_OUTPUT_FOLDER
  if config['Config']['OutputDirectory']:
    output_folder = config['Config']['OutputDirectory']

  output_file = DEFAULT_OUTPUT_FILE
  if config['Config']['OutputFileName']:
    output_file = config['Config']['OutputFile']

  reinstall_script_file = DEFAULT_REINSTALL_SCRIPT
  if config['Config']['OutputScriptName']:
    reinstall_script_file = config['Config']['OutputScriptName']
  LOGGER.debug(f'output_folder = {output_folder}')
  LOGGER.debug(f'output_file = {output_file}')
  LOGGER.debug(f'reinstall_script_file = {reinstall_script_file}')
  return (output_folder, output_file, reinstall_script_file)

def generate_installed_versions_file(output_file):
  LOGGER.info(f'Entering method')
  LOGGER.debug(f'output_file: {output_file}')
  # Generate file with installed packages + versions
  # Text file, contains list of installed packages plus version
  LOGGER.debug('Writing output to file: {}'.format(output_file))
  subprocess.call(['choco', 'list', '-lo', '>', output_file], shell=True)
  LOGGER.info(f'Exiting')

@click.command()
@click.option('-v', '--verbose', help='Change the log level to logging.DEBUG (10)', is_flag=True)
@click.option('-q', '--quiet', help='Change the log level to logging.NOTSET (0)', is_flag=True)
def backup_choco_installed_main(verbose, quiet): 

  # meh
  if verbose:
    log_level = logging.DEBUG
  elif quiet:
    log_level = logging.NOTSET
  else:
    log_level = logging.INFO

  LOGGER.setLevel(log_level)
  LOGGER.info('Entering method')

  LOGGER.debug(f'Log level = {log_level}')
  output_folder, output_file, reinstall_script_file = get_config(DEFAULT_CONFIG_FILE)

  output_file = os.path.join(output_folder, output_file)
  generate_installed_versions_file(output_file)

  # Regex pattern to match package name only in output of choco list
  pattern = '^(?!Chocolatey.*)(.*?)\s\d.*'
  capture_group = 1 # capture the middle group in regex pattern

  # Output file to write Powershell command to 
  cmd_script = os.path.join(output_folder, reinstall_script_file)

  # Generate powershell command to write to script file
  with open(output_file, 'r') as infile, open(cmd_script, 'w') as outfile:
      cmd = ['choco', 'install', '-y']
      for line in infile:
          search = re.search(pattern, line)
          if search:
              cmd.append(search.group(capture_group))
      cmd = ' '.join(cmd)
      LOGGER.info('Powershell command to reinstall all packages:\n{}'.format(cmd))
      LOGGER.debug(f'Writing Powershell command to file {cmd_script}')
      outfile.write(cmd)
  LOGGER.info('Exiting')


if __name__ == "__main__": 
  backup_choco_installed_main()