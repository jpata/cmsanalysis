import sys
from myNanoProdMc2018_NANO import *

ijob = int(sys.argv[-1]) - 1
job_output_input = open("inputs.txt").readlines()[ijob].strip()
job_input = job_output_input.split()[1:]

process.source.fileNames = job_input
process.maxEvents.input = -1
