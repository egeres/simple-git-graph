import argparse, time, json, os
# from git import *

#this part handles the arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', action="store", dest="d", help='route of the git directory')
arguments = parser.parse_args()

if not arguments.d:
    arguments.d = os.getcwd()
    # exit()

# repo = Repo(arguments.d)
# assert repo.bare == False

dic_to_write = {}

# for i in repo.iter_commits('master'):
#     print i

with open('data.json', 'w') as outfile:
    json.dump(dic_to_write, outfile)
