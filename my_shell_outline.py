#!/usr/bin/env python

"""my_shell_outline.py:
Simple shell that interacts with the filesystem, e.g., try "PShell>files".

Try to stick to Style Guide for Python Code and Docstring Conventions:
see https://peps.python.org/pep-0008 and https://peps.python.org/pep-0257/

(Note: The breakdown into Input/Action/Output in this script is just a suggestion.)
"""

import glob
import os
import pwd
import shutil
import sys
import time
import datetime

# ========================
#    delete command
#    delete file in argument
# ========================

def delete_cmd(field):
    try:
        os.remove(field)
    except FileExistsError:
        print("Error: File does not exist")
    except PermissionError:
        print("Error: Permissions required")
    except Exception as e:
        print("An error has occured: ", e)
    else:
        print("Delete successful")
    finally:
        return

# ========================
#    move file command
#    move file to directory argument
# ========================

def move_cmd(file, dest_dir):
    return shutil.move(file, dest_dir)

# ========================
#    make dir command
#    make dir in current directory
# ========================

def make_cmd(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print("Error: A directory with this name already exists")
    except Exception as e:
        print("An error has occured: ", e)
    else:
        print("Directory successfully created")
    finally:
        return
    
# ========================
#    into command
#    change directory to specified destination
# ========================
    
def into_cmd(dest):
    try:
        os.chdir(dest)
    except FileNotFoundError:
        print("Error: directory does not exist")
    except NotADirectoryError:
        print("Error: Argument must be a directory")
    except PermissionError:
        print("Error: Permissions required")
    except Exception as e:
        print("An error has occured: ", e)
    else:
        print("Successful")
    finally:
        return

def out_cmd(dest):
    try:
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)   
        root_dir = os.path.abspath(os.sep)
        os.chdir(parent_dir)
    except FileNotFoundError:
        print("Error: directory does not exist")
    except NotADirectoryError:
        print("Error: Argument must be a directory")
    except current_dir == root_dir:
        print('Error: In root directory already')
    except Exception as e:
        print("An error has occured: ", e)
    finally:
        return
    

    


# ========================
#    files command
#    List file and directory names
#    No command arguments
# ========================
def files_cmd(fields):
    """Return nothing after printing names/types of files/dirs in working directory.
    
    Input: takes a list of text fields
    Action: prints for each file/dir in current working directory their type and name
            (unless list is non-empty in which case an error message is printed)
    Output: returns no return value
    """
    
    if checkArgs(fields, 0):
        for filename in os.listdir('.'):
            if os.path.isdir(os.path.abspath(filename)):
                print("dir:", filename)
            else:
                print("file:", filename)

# ========================
#  info command
#     List file information
#     1 command argument: file name
# ========================
                
infoHeaders = ["File Name", "Type", "Owner", "Modification Time", "Size", "Executable"]  # column headers
infoWidth = [25, 21, 15, 25, 25, 20]

def info_cmd(name):
    print_header(infoHeaders, infoWidth)

    info = file_info(name)
    print_file_info(info, infoWidth)


def file_info(name):
    #global info
    info = []
    info.append(name)  # the file name

    type = ""
    if os.path.islink(name):
        type = "Symbolic Link"
    elif os.path.isfile(name):
        type = "Regular File"
    elif os.path.isdir(name):
        type = "Directory"
    else:
        type = "Unknown"
    info.append(type)

    info.append(os.stat(name).st_uid)  # the owner
    info.append(datetime.datetime.fromtimestamp(os.path.getmtime(name)).strftime('%b %d %Y %H:%M:%S')) # mod time
    if type == "Regular File":
        info.append(os.path.getsize(name)) # size
        execute = os.access(name, os.X_OK) # executable
        if not execute: 
            info.append("No")
        else:
            info.append("Yes")

    else: 
        info.append("N/A")
        info.append("N/A")
        

    return info

def print_file_info(info, width):
    #global info
    fieldNum = 0
    output = ''
    while fieldNum < len(info):
        output += '{field:{fill}<{width}}'.format(field=info[fieldNum], fill=' ', width=width[fieldNum])
        fieldNum += 1
    print(output)

def print_header(headers, width):
    field_num = 0
    output = ''
    while field_num < len(headers):
        output += '{field:{fill}<{width}}'.format(field=headers[field_num], fill=' ', width=width[field_num])
        field_num += 1

    print(output)
    length = sum(width)
    print("-" * length)

# ----------------------
# Other functions
# ----------------------
def checkArgs(fields, num):
    """Returns if len(fields)-1 == num and print an error in shell if not.
    
    Input: takes a list of text fields and how many non-command fields are expected
    Action: prints error to shell if the number of fields is unexpected
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

def checkExists(field, index):
    if not os.path.exists(field):
        print("Error: Arg{index} invalid file/directory path ")
        return False
    return True

def checkFile(field, index):
    if not os.path.isfile(field):
        print("Error: Arg{index} must be file")
        return False
    return True

def checkDir(field, index):
    if not os.path.isdir(field):
        print("Error: Arg{index} must be a directory")
        return False
    return True


# ---------------------------------------------------------------------

def main():
    """Returns exit code 0 (after executing the main part of this script).
    
    Input: no function arguments
    Action: run multiple user-inputted commands
    Output: return zero to indicate regular termination
    """
    status = True
    while status:
        line = input("PShell>")
        fields = line.split()
        # split the command into fields stored in the fields list
        # fields[0] is the command name and anything that follows (if it follows) is an argument to the command
        
        if fields[0] == "files":
            files_cmd(fields)

        elif fields[0] == "info":
            if checkArgs(fields, 1):   
                if checkExists(fields[1], 1):
                    info_cmd(fields[1])

        elif fields[0] == "delete":
            if checkArgs(fields, 1):
                    delete_cmd(fields)

        elif fields[0] == "move":
            if checkArgs(fields, 2):
                if checkExists(fields[1], 1) and checkFile(fields[1], 1):
                    if checkExists(fields[2], 2) and checkDir(fields[2], 2):
                        move_cmd(fields[1], fields[2])

        elif fields[0] == "into":
            if checkArgs(fields, 1):
                into_cmd(fields[1])
        
        elif fields[0] == "out":
            if checkArgs(fields, 1):
                out_cmd(fields[1])

        elif fields[0] == "make":
            if checkArgs(fields, 1):
                make_cmd(fields[1])

        elif fields[0] == "finish":                             
            status = False
        else:
            print("Unknown command", fields[0])
    
    return 0 # currently unreachable code

if __name__ == '__main__':
    sys.exit( main() ) # run main function and then exit
