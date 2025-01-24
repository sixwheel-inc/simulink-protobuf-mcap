import sys
import shutil

with open(sys.argv[1], "r") as input:
    with open(sys.argv[1] + "_tmp", "w") as output:
        for line in input.readlines():
            out = line.replace('#include "controls-proto/', '#include "')
            output.write(out)

shutil.move(sys.argv[1] + "_tmp", sys.argv[1])
