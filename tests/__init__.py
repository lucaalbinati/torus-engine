import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.join(os.path.dirname(currentdir), "torusengine")
sys.path.append(parentdir)
print(parentdir)