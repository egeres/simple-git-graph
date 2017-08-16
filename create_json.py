import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', action="store", dest="d", help='route of the git directory')
arguments = parser.parse_args()

if not arguments.d:
    exit()
