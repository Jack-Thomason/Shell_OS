#!/usr/bin/env python

"""my_run_shell_0.py:
Simple shell to start programs, e.g., try "PShell>ps" and "PShell>ls".

The purpose of this script is to give you simple functions
for locating an executable program in common locations in Linux/UNIX
(PATH environmental variable).

You are meant to paste your code from your solution in Part A
into the relevant points in this script.

Try to stick to Style Guide for Python Code and Docstring Conventions:
see https://peps.python.org/pep-0008 and https://peps.python.org/pep-0257/

(Note: The breakdown into Input/Action/Output in this script is just a suggestion.)
"""

from datetime import datetime
import os, shutil, sys

# Here the path is hardcoded, but you can easily optionally get your PATH environ variable
# by using: path = os.environ['PATH'] and then splitting based on ':' such as the_path = path.split(':')
path = os.environ['PATH']
THE_PATH = path.split(':')

# ========================
#   Run command
#   Run an executable somewhere on the path
#   Any number of arguments
# ========================
def runCmd(fields):
    """Returns nothing (after trying to execute user command expressed in fields).
    
    Input: takes a list of text fields (and global list of directories to search)
    Action: executes command
    Output: returns no return value
    """
    
    global THE_PATH
    cmd = fields[0]
    
    execname = add_path(cmd, THE_PATH)

    # run the executable
    if execname == None:
        print ("Executable file", cmd, "not found")
    else:
        # execute the command
        print(execname)

# execv executes a new program, replacing the current process; on success, it does not return.
# On Linux systems, the new executable is loaded into the current process, and will have the same process id as the caller.
    try:
        os.execv(execname, fields)
    except :
        print("Something went wrong there")
        os._exit(0)

# ========================
#   Constructs the full path used to run the external command
#   Checks to see if an executable file can be found in one of the provided directories.
#   Returns None on failure.
# ========================
def add_path(cmd, executable_dirs):
    """Returns command with full path when possible and None otherwise.
    
    Input: takes a command and a list of paths to search
    Action: no actions
    Output: returns external command prefaced by full path
            (returns None if executable file cannot be found in any of the paths)
    """
    if cmd[0] not in ['/', '.']:
        for dir in executable_dirs:
            execname = dir + cmd
            if os.path.isfile(execname) and os.access(execname, os.X_OK):
                return execname
        return None
    else:
        return cmd

# ========================
#   files command
#   List file and directory names
#   No arguments
# ========================
def filesCmd(fields):
    """Not yet implemented"""
    
    print("Nothing here yet. Use your files command from part A")

# ========================
#  info command
#   List file information
#   1 argument: file name
# ========================
def infoCmd(fields):
    """Not yet implemented."""
    
    print("Nothing here yet. Use your info command from part A")

# ----------------------
# Other functions
# ----------------------
def checkArgs(fields, num):
    """Returns if len(fields)-1 == num (prints error to shell if not).
    
    Input: takes a list of text fields and how many non-command fields are expected
    Action: prints an error message if the number of fields is unexpected
    Output: returns boolean value to indicate if it was expected number of fields
    """
    
    numArgs = len(fields) - 1
    if numArgs == num:
        return True
    if numArgs > num:
        print("Unexpected argument", fields[num+1], "for command", fields[0])
    else:
        print("Missing argument for command", fields[0])
    
    return False

# ---------------------------------------------------------------------

def main():
    """Returns exit code 0 (after executing the main part of this script).
    
    Input: no function arguments
    Action: run multiple user-inputted commands
    Output: return zero to indicate regular termination
    """
    
    while True:
        line = input("PShell>")
        fields = line.split()
    
        if fields[0] == "files":
            filesCmd(fields)
        elif fields[0] == "info":
            infoCmd(fields)
        else:
            runCmd(fields)
    
    return 0 # currently unreachable code

if __name__ == '__main__':
    sys.exit(main()) # run main function and then exit
