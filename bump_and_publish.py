import sys
import config
import subprocess

command_options = {
    "-M":   "major upgrade",
    "-m":   "minor upgrade",
    "-p":   "patch upgrade"
}

if len(sys.argv) != 2:
    message = "Must pass an argument to indicate which kind of version upgrade this is:\n"
    for option, description in command_options.items():
        message += "\t{}\t\t{}\n".format(option, description)
    raise Exception(message)

type_of_upgrade = sys.argv[1]
if not type_of_upgrade in command_options.keys():
    raise Exception("Unknown type of version upgrade: '{}'".format(type_of_upgrade))
    
# bump version
subprocess.run(["bump", type_of_upgrade, "-r"])

# build python project
subprocess.run(["python", "-m", "build"])

# publish using twine
try:
    subprocess.run(["twine", "upload", "dist/*", "-u", config.PYPI_TOKEN_USERNAME, "-p", config.PYPI_TOKEN_PASSWORD])
except AttributeError as e:
    print("Make sure you have a file named 'config.py' in the project's root with both 'PYPI_TOKEN_USERNAME' and 'PYPI_TOKEN_PASSWORD' set.")
finally:
    # remove build files
    subprocess.run(["rm", "-r", "dist"])
    subprocess.run(["rm", "-r", "src/torus_engine.egg-info"])