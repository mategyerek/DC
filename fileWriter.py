import os
import re


def initWrite(overwrite, basename):
    if overwrite:
        try:
            os.remove(f"{basename}.txt")
            os.remove(f"{basename}.csv")
            name = basename
        except OSError:
            pass
    else:
        filenames = list(filter(lambda x: basename in x, os.listdir()))
        maxnumber = max([int(i)
                        for i in re.findall(r'\d+', "".join(filenames))])
        name = f"{basename}{maxnumber+1}"
    rawfile = open(name, 'w')
    csvfile = open(name, 'w')
    csvwriter = csvfile.writer(csvfile)
    return rawfile, csvfile
