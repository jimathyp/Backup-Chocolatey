# python3
# 13:54:24 Saturday 05 May 2018
# parse choco output to produce a script to update config if laptop reset
# choco list -lo > choco-installed.txt
# powershell_script = "choco list -lo > {filename}"
#
# v20180510_093858 Cleanup

import subprocess
import os
import re
import datetime
import jputils

timestamp = jputils.datetime_timestamp()

# Text file, contains list of installed packages plus version
output_file = "choco-installed-versions_{}.txt".format(timestamp)

# Regex pattern to match package name only in output of choco list
pattern = "^(?!Chocolatey.*)(.*?)\s\d.*"
capture_group = 1 # capture the middle group in regex pattern

# Generate file with installed packages + versions
output_file = os.path.join(os.getcwd(), output_file)
subprocess.call(["choco", "list", "-lo", ">", output_file], shell=True)

# Output file to write Powershell command to 
cmd_script = "choco-reinstall-{}.ps1".format(timestamp) 

# Generate powershell command to write to script file
with open(output_file, "r") as infile, open(cmd_script, "w") as outfile:
    cmd = ["choco", "install", "-y"]
    for line in infile:
        search = re.search(pattern, line)
        if search:
            cmd.append(search.group(capture_group))
    cmd = " ".join(cmd)
    print(cmd)
    outfile.write(cmd)
