from __future__ import print_function
import sys

def get_lfn(fn):
    i0 = fn.index("/store")
    lfn = fn[i0:]
    return lfn

argfile = open("args.txt", "w")
inputfile = open("inputs.txt", "w")
for ifi, fi in enumerate(open("files.txt").readlines()):
    fi = fi.strip()
    lfn = get_lfn(fi)
    spl = list(lfn.split("/"))
    spl[3] = "MyNanoAOD"
    spl[5] = spl[5].replace("MINIAOD", "NANOAOD")
    spl[-1] = "myNano_{0}.root".format(ifi)
    out_lfn = "/".join(spl)
    print(out_lfn, lfn, file=inputfile)
    print(ifi, file=argfile)     
