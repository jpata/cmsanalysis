import ROOT
import sys
import numpy as np
from DataFormats.FWLite import Events, Handle

filename = sys.argv[1]
events = Events(filename)

if __name__ == "__main__":

    # loop over events
    for iev, event in enumerate(events):
        eid = event.object().id()
        eventId = (eid.run(), eid.luminosityBlock(), int(eid.event()))
        print(eventId)
