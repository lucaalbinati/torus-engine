
SETUP_FILE = "setup.py"
VERSION_TAG = "version=\""

# open "setup.py" file
f = open(SETUP_FILE, "r")
text = f.read()

# find current version number
version_tag_idx = text.index(VERSION_TAG)
start_version_idx = version_tag_idx + len(VERSION_TAG)
end_version_idx = start_version_idx +  text[start_version_idx:].index("\"")

current_version = text[start_version_idx:end_version_idx]
second_dot_idx = current_version.rindex(".")
version_third_value = int(current_version[second_dot_idx+1:])

# increment last version value by 1
new_version_third_value = version_third_value + 1
new_version = current_version[:second_dot_idx+1] + str(new_version_third_value)

# replace version number
text = text.replace(current_version, new_version)
f.close()

# rewrite file with new version number
f = open(SETUP_FILE, "w")
f.write(text)
f.close()