import argparse, time, json, os
import git

#this part handles the arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', action="store", dest="d", help='route of the git directory')
arguments = parser.parse_args()

if not arguments.d:
    arguments.d = os.getcwd()
    # exit()

repo  = git.Repo(arguments.d)
tree  = repo.tree()
paths = [obj.path for obj in tree]

latest_commits = {}
dic_to_write    = {}

# for i in repo.iter_commits('master'):
#     print i


for commit in repo.iter_commits(paths=paths):

    print commit.committed_date
    print commit.message
    print commit.author.name
    print commit.diff()

    # for f in commit.stats.files.keys():
    #     p = f[:f.index('/')] if '/' in f else f
    #     if p in latest_commits:
    #         continue
    #
    #     print("adding %s for %s (was: %s)" % (commit, p, f))
    #     latest_commits[p] = commit
    #
    # if len(latest_commits) == len(paths):
    #     break

# for i in latest_commits.iteritems():
#     print i

with open('data.json', 'w') as outfile:
    json.dump(dic_to_write, outfile)
