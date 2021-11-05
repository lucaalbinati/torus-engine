import sys
import subprocess

command_options = {
    "-M": "major release",
    "-m": "minor release",
    "-p": "patch release"
}

if len(sys.argv) != 2:
    message = "Must pass an argument to indicate which kind of version upgrade this is:\n"
    for option, description in command_options.items():
        message += "\t{}\t\t{}\n".format(option, description)
    raise Exception(message)

type_of_upgrade = sys.argv[1]
if not type_of_upgrade in command_options.keys():
    raise Exception("Unknown type of version upgrade: '{}'".format(type_of_upgrade))

# check there are no files staged
staged_files_out = subprocess.check_output("git diff --name-only --cached".split())
staged_files_out = staged_files_out.decode("utf-8")
contains_staged_files = len(staged_files_out) > 0
if contains_staged_files:
    raise Exception("Cannot proceed when there are staged files. Please remove them (either 'restore' or 'commit').")

# bump version
new_version_out = subprocess.check_output("bump {} -r".format(type_of_upgrade).split())
new_version = new_version_out.decode("utf-8").split()[0]
new_version_tag = "v{}".format(new_version)

# push code
subprocess.run("git add setup.py".split())
subprocess.run(["git", "commit", "-m", "{} {}".format(command_options[type_of_upgrade], new_version_tag)])
subprocess.run("git push".split())

# release
subprocess.run(["gh", "release", "create", new_version_tag, "--notes", "{} release".format(new_version_tag)])