import ROOT
import sys
import numpy as np
from DataFormats.FWLite import Events, Handle

filename = sys.argv[1]
events = Events(filename)

class HandleLabel:
    def __init__(self, dtype, label):
        self.handle = Handle(dtype)
        self.label = (label, )

    def getByLabel(self, event):
        event.getByLabel(self.label, self.handle)

    def product(self):
        return self.handle.product()

class EventDesc:
    def __init__(self):
        self.genparticle = HandleLabel("std::vector<reco::GenParticle>", "genParticles")
        self.pfcluster_ecal = HandleLabel("std::vector<reco::PFCluster>", "particleFlowClusterECAL")
        self.pfcluster_hcal = HandleLabel("std::vector<reco::PFCluster>", "particleFlowClusterHCAL")
        self.pfcluster_hf = HandleLabel("std::vector<reco::PFCluster>", "particleFlowClusterHF")
        self.pfcand = HandleLabel("std::vector<reco::PFCandidate>", "particleFlow")
        self.tracks = HandleLabel("std::vector<reco::Track>", "generalTracks")

    def get(self, event):
        self.genparticle.getByLabel(event) 
        self.pfcluster_ecal.getByLabel(event) 
        self.pfcluster_hcal.getByLabel(event) 
        self.pfcluster_hf.getByLabel(event) 
        self.pfcand.getByLabel(event) 
        self.tracks.getByLabel(event) 

class Output:
    def __init__(self):
        self.tfile = ROOT.TFile("out.root", "RECREATE")
        self.clusters = ROOT.TTree("clusters", "clusters")
        self.clusters_layer = np.zeros(1, dtype=np.int32)
        self.clusters_x = np.zeros(1, dtype=np.float32)
        self.clusters.Branch("layer", self.clusters_layer, "layer/I")

    def close(self):
        self.tfile.Write()
        self.tfile.Close()
 
evdesc = EventDesc()
output = Output()

# loop over events
for event in events:
    eid = event.object().id()
    eventId = (eid.run(), eid.luminosityBlock(), int(eid.event()))

    evdesc.get(event)

    #genpart = evdesc.genparticle.product()
    #for gp in genpart:
    #    if gp.status() == 2:
    #        print("genpart", eventId[2], gp.energy(), gp.px(), gp.py(), gp.pz(), gp.pdgId())
    
    pfcluster_ecal = evdesc.pfcluster_ecal.product()
    for cl in pfcluster_ecal:
        output.clusters_layer[0] = cl.layer()
        output.clusters_x[0] = cl.x()
        output.clusters.Fill()
    
    #pfcluster_hcal = evdesc.pfcluster_hcal.product()
    #for cl in pfcluster_hcal:
    #    print("hcal", eventId[2], cl.depth(), int(cl.layer()), cl.energy(), cl.x(), cl.y(), cl.z())
    #
    #pfcluster_hf = evdesc.pfcluster_hf.product()
    #for cl in pfcluster_hf:
    #    print("hf", eventId[2], cl.depth(), int(cl.layer()), cl.energy(), cl.x(), cl.y(), cl.z())
    #
    #tracks = evdesc.tracks.product()
    #for c in tracks:
    #    print("trk", eventId[2], c.charge(), c.innerMomentum().x(), c.innerMomentum().y(), c.innerMomentum().z(), c.px(), c.py(), c.pz(), c.outerMomentum().x(), c.outerMomentum().y(), c.outerMomentum().z())
    #
    #pfcand = evdesc.pfcand.product()
    #for c in pfcand:
    #    print("cand", eventId[2], c.energy(), c.px(), c.py(), c.pz(), c.pdgId())
