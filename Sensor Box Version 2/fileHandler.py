import os
import re
import csv


def initWrite(overwrite, basename):
    if overwrite:
        try:
            os.remove(f"{basename}.txt")
            os.remove(f"{basename}.csv")
            
        except OSError:
            pass
        name1 = basename
    else:
        filenames = list(filter(lambda x: basename in x, os.listdir()))
        maxnumber = max([int(i)
                        for i in re.findall(r'\d+', "".join(filenames))])
        name1 = f"{basename}{maxnumber+1}"
    rawfile = open(f"{name1}.txt", 'w')
    csvfile = open(f"{name1}.csv", 'w', newline='')
    csvwriter = csv.writer(csvfile)
    return rawfile, csvwriter
