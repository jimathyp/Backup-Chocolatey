# python3
# 13:54:24 Saturday 05 May 2018
# parse choco output to produce a script to update config if laptop reset
# choco list -lo > choco-installed.txt
# powershell_script = "choco list -lo > {filename}"

output_list = "choco-installed.txt"

import subprocess
import os
import re


output_file = "choco-installed.txt"
output_file = os.path.join(os.getcwd(), output_file)
print(output_file)

subprocess.call(["choco", "list", "-lo", ">", output_file], shell=True)

cmd_script = "choco-reinstall.ps1" 

#read the output_file in
with open(output_file, "r") as f:

# parse file:
    for line in f:
        # if not line.startswith("Chocolatey") and not line[0].isdigit():

        print(line)
    # remove 1st line "Chocolatey v0.10.8"
    # remove version from each line 7zip.commandline 16.02.0.20170209
    # remove last line 70 packages installed.
    
    

    
    