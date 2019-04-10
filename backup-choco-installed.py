#!/usr/bin/env python
# -*- coding utf-8 -*-

"""
backup-choco-installed.py
Description
USAGE: python backup-choco-installed.py
Lists installed chocolatey packages and outputs a file listing packages and a script that allows reinstallation
equivalent of 'choco list -lo > choco-installed.txt'

Created: 13:54:24 Saturday 05 May 2018
v20180510_093858 Cleanup
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

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# ---------------------------------------- 
# Configuration
DEFAULT_CONFIG_FILE=os.path.join(os.path.dirname(sys.argv[0]), 'config.ini')

# This configuration can be picked up from config.ini file
DEFAULT_OUTPUT_FOLDER=r'.'
DEFAULT_OUTPUT_FILE = 'choco-installed-versions_{}.txt'.format(timestamp)
DEFAULT_REINSTALL_SCRIPT = 'choco-reinstall-{}.ps1'.format(timestamp)
# ---------------------------------------- 

# Text file, contains list of installed packages plus version

config = configparser.ConfigParser()

# check for config file
if not os.path.isfile(DEFAULT_CONFIG_FILE):
  raise FileNotFoundError('The default config file was not found at path: "{}"'.format(DEFAULT_CONFIG_FILE))

config.read(DEFAULT_CONFIG_FILE)

output_folder = DEFAULT_OUTPUT_FOLDER
if config['Config']['OutputDirectory']:
  output_folder = config['Config']['OutputDirectory']

output_file = DEFAULT_OUTPUT_FILE
if config['Config']['OutputFileName']:
  output_file = config['Config']['OutputFile']

reinstall_script_file = DEFAULT_REINSTALL_SCRIPT
if config['Config']['OutputScriptName']:
  output_file = config['Config']['OutputScriptName']

# Regex pattern to match package name only in output of choco list
pattern = '^(?!Chocolatey.*)(.*?)\s\d.*'
capture_group = 1 # capture the middle group in regex pattern

# Generate file with installed packages + versions
# output_file = os.path.join(os.getcwd(), output_file)
output_file = os.path.join(output_folder, output_file)
print('Writing output to file {}'.format(output_file))

subprocess.call(['choco', 'list', '-lo', '>', output_file], shell=True)

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
    print(cmd)
    outfile.write(cmd)

#if __name__ == "__main__": 