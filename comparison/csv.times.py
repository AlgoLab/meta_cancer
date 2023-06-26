import sys
import glob
import re

print("ix,tool,seconds")
for file in glob.glob(f"benchmark/*/{sys.argv[1]}/*"):
    m = re.search(r"benchmark/(\w+)/.*/sim_(\d+)\..*", file)
    with open(file) as fin:
        lines = fin.readlines()

    print(m.group(2), m.group(1).upper(), lines[-1].split()[0], sep=',')