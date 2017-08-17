## Imports
import os
import git
import csv
import argparse

output        = []
used          = []
list_of_files = []

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', action="store", dest="directory", help='route of the git directory')
parser.add_argument('-f', action="store", dest="file_list", help='list of files to keep track of')
arguments = parser.parse_args()

if not arguments.directory:
    arguments.directory = os.getcwd()

if arguments.file_list:
    with open(arguments.file_list) as f:
        list_of_files = f.readlines()
    list_of_files = [x.strip() for x in list_of_files]

print "list_of_files       =", list_of_files
print "arguments.directory =", arguments.directory
print "arguments.directory =", arguments.directory.replace("\\","\\\\")

## Module Constants
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def versions(path, branch='master'):
    """
    This function returns a generator which iterates through all commits of
    the repository located in the given path for the given branch. It yields
    file diff information to show a timeseries of file changes.
    """

    # Create the repository, raises an error if it isn't one.
    repo = git.Repo(path)

    # Iterate through every commit for the given branch in the repository
    for commit in repo.iter_commits(branch):
        # Determine the parent of the commit to diff against.
        # If no parent, this is the first commit, so use empty tree.
        # Then create a mapping of path to diff for each file changed.
        parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
        diffs  = {
            diff.a_path: diff for diff in commit.diff(parent)
        }

        # The stats on the commit is a summary of all the changes for this
        # commit, we'll iterate through it to get the information we need.
        for objpath, stats in commit.stats.files.items():

            # Select the diff for the path in the stats
            diff = diffs.get(objpath)

            # If the path is not in the dictionary, it's because it was
            # renamed, so search through the b_paths for the current name.
            if not diff:
                for diff in diffs.values():
                    if diff.b_path == path and diff.renamed:
                        break

            # Update the stats with the additional information
            stats.update({
                'message': commit.message,
                'object': os.path.join(path, objpath),
                'commit': commit.hexsha,
                'author': commit.author.email,
                'timestamp': commit.authored_datetime.strftime(DATE_TIME_FORMAT),
                'time'     : commit.committed_date,
                'size': diff_size(diff),
                'type': diff_type(diff),
            })

            yield stats


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

# print arguments.d

data = versions(str(arguments.directory))

#list_of_files

for i in data:

    # print "\n"*3
    # for j in i.iteritems(): print j

    if i["time"] not in used:
        used.append(i["time"])
        # output.append([i["time"], i["insertions"] , i["deletions"], i["timestamp"].split("+")[0]])
        output.append([ i["time"], 0, 0, i["timestamp"].split("+")[0] ])

    if len(list_of_files) == 0:
        for n, j in enumerate(output):
            if j[0] == i["time"]:
                output[n][1] += i["insertions"]
                output[n][2] += i["deletions"]
    else:
        # aa = len(arguments.directory.replace("\\","\\\\")) + 2
        aa = len(arguments.directory) + 1

        print arguments.directory.replace("\\","\\\\")
        print len(arguments.directory.replace("\\","\\\\"))
        print i["object"]
        print i["object"][aa::]
        print i["object"][aa::] in list_of_files

        if i["object"][aa::] in list_of_files:
            for n, j in enumerate(output):
                if j[0] == i["time"]:
                    output[n][1] += i["insertions"]
                    output[n][2] += i["deletions"]

output = sorted(output, key=lambda x: x[0])
# print output





with open('changes.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(["date", "insertions", "deletions"])
    for i in output:
        wr.writerow([i[3], i[1], i[2]])










#
