#!/usr/bin/env python

import argparse
import sys

class GitMaster(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
        usage='''git <command> [<args>]
The git commands are:
add    Add a file from working directory to the staging area.
commit Commit a file from staging area to the local repository.
 ''')
        parser.add_argument('command', help='git commands')
        parser.add_argument('-v','--version', help='show version and   exit', action='version', version='1.0')
        #Read the first argument (add/commit)
        args = parser.parse_args(sys.argv[1:2])
        #use dispatch pattern to invoke method with same name of the argument
        getattr(self, args.command)()
    def add(self):
        parser = argparse.ArgumentParser(description='Adds a file')
        parser.add_argument('-f','--file-name', required=True,   help='file to be added')
        #we are inside a subcommand, so ignore the first argument and read the rest
        args = parser.parse_args(sys.argv[2:])
        git_add(args.file_name)
    
    def commit(self):
        parser = argparse.ArgumentParser(description='Commits a file')
        parser.add_argument('-m','--comment', required=True, help='comment to be used for commit')
        #we are inside a subcommand, so ignore the first argument and read the rest
        args = parser.parse_args(sys.argv[2:])
        git_commit(args.comment)

#Dummy Functions
def git_add(filename):
    #Write the required logic for the action “add”
     print('Inside add action')
     print('Passed file name is %s ' %filename)
     
def git_commit(comment):
    #Write the required logic for the action “commit”
    print('Inside commit action')
    print('Passed comment is %s ' %comment)

if __name__ == '__main__':
    GitMaster()