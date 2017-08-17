import argparse, time, json, os
import git


EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

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



def diff_size(diff):
    """
    Computes the size of the diff by comparing the size of the blobs.
    """
    if diff.b_blob is None and diff.deleted_file:
        # This is a deletion, so return negative the size of the original.
        return diff.a_blob.size * -1

    if diff.a_blob is None and diff.new_file:
        # This is a new file, so return the size of the new value.
        return diff.b_blob.size

    # Otherwise just return the size a-b
    return diff.a_blob.size - diff.b_blob.size

def diff_type(diff):
    """
    Determines the type of the diff by looking at the diff flags.
    """
    if diff.renamed: return 'R'
    if diff.deleted_file: return 'D'
    if diff.new_file: return 'A'
    return 'M'

# for commit in repo.iter_commits(branch):
for commit in repo.iter_commits(paths=paths):


    # parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
    # diffs  = {
    #     diff.a_path: diff for diff in commit.diff(parent)
    # }
    #
    # for objpath, stats in commit.stats.files.items():
    #     # Select the diff for the path in the stats
    #     diff = diffs.get(objpath)
    #     print 'size', diff_size(diff),
    #     print 'type', diff_type(diff),

    print "0", commit.committed_date
    print "0", time.asctime(time.gmtime(commit.committed_date))
    print "0", time.strftime("%a, %d %b %Y %H:%M", time.gmtime(commit.committed_date))
    print "1", commit.message
    print "2", commit.author.name
    print "3", commit.diff()

    for i in commit.diff():
        print "5", diff_size(i), "6", diff_type(i)



    print "\n\n"







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
