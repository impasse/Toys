from collections import defaultdict
import sys

counter = defaultdict(int)
with open(sys.argv[1]) as f:
    for word in f.read().split():
        counter[word] += 1

for key in sorted(counter.keys()):
    print("{}: {}".format(key, counter[key]))
