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
        
        self.pftree = ROOT.TTree("pftree", "pftree")

        #http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_10_6_2/doc/html/d6/dd4/classreco_1_1PFCluster.html
        self.nclusters = np.zeros(1, dtype=np.uint32)
        self.maxclusters = 1000
        self.clusters_layer = np.zeros(self.maxclusters, dtype=np.int32)
        self.clusters_depth = np.zeros(self.maxclusters, dtype=np.int32)
        self.clusters_type = np.zeros(self.maxclusters, dtype=np.int32)
        self.clusters_energy = np.zeros(self.maxclusters, dtype=np.float32)
        self.clusters_x = np.zeros(self.maxclusters, dtype=np.float32)
        self.clusters_y = np.zeros(self.maxclusters, dtype=np.float32)
        self.clusters_z = np.zeros(self.maxclusters, dtype=np.float32)
        
        self.pftree.Branch("nclusters", self.nclusters, "nclusters/i")
        self.pftree.Branch("clusters_layer", self.clusters_layer, "clusters_layer[nclusters]/I")
        self.pftree.Branch("clusters_depth", self.clusters_depth, "clusters_depth[nclusters]/I")
        self.pftree.Branch("clusters_type", self.clusters_type, "clusters_type[nclusters]/I")
        self.pftree.Branch("clusters_energy", self.clusters_energy, "clusters_energy[nclusters]/F")
        self.pftree.Branch("clusters_x", self.clusters_x, "clusters_x[nclusters]/F")
        self.pftree.Branch("clusters_y", self.clusters_y, "clusters_y[nclusters]/F")
        self.pftree.Branch("clusters_z", self.clusters_z, "clusters_z[nclusters]/F")
        
        self.ngenparticles = np.zeros(1, dtype=np.uint32)
        self.maxgenparticles = 1000
        self.genparticles_pt = np.zeros(self.maxgenparticles, dtype=np.float32)
        self.genparticles_eta = np.zeros(self.maxgenparticles, dtype=np.float32)
        self.genparticles_phi = np.zeros(self.maxgenparticles, dtype=np.float32)
        self.genparticles_x = np.zeros(self.maxgenparticles, dtype=np.float32)
        self.genparticles_y = np.zeros(self.maxgenparticles, dtype=np.float32)
        self.genparticles_z = np.zeros(self.maxgenparticles, dtype=np.float32)
        self.genparticles_pdgid = np.zeros(self.maxgenparticles, dtype=np.int32)
        
        self.pftree.Branch("ngenparticles", self.ngenparticles, "ngenparticles/i")
        self.pftree.Branch("genparticles_pt", self.genparticles_pt, "genparticles_pt[ngenparticles]/F")
        self.pftree.Branch("genparticles_eta", self.genparticles_eta, "genparticles_eta[ngenparticles]/F")
        self.pftree.Branch("genparticles_phi", self.genparticles_phi, "genparticles_phi[ngenparticles]/F")
        self.pftree.Branch("genparticles_x", self.genparticles_x, "genparticles_x[ngenparticles]/F")
        self.pftree.Branch("genparticles_y", self.genparticles_y, "genparticles_y[ngenparticles]/F")
        self.pftree.Branch("genparticles_z", self.genparticles_z, "genparticles_z[ngenparticles]/F")
        self.pftree.Branch("genparticles_pdgid", self.genparticles_pdgid, "genparticles_pdgid[ngenparticles]/I")
       
        #http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_10_6_2/doc/html/dd/d5b/classreco_1_1Track.html 
        self.ntracks = np.zeros(1, dtype=np.uint32)
        self.maxtracks = 1000
        self.tracks_pt = np.zeros(self.maxtracks, dtype=np.float32)
        self.tracks_eta = np.zeros(self.maxtracks, dtype=np.float32)
        self.tracks_phi = np.zeros(self.maxtracks, dtype=np.float32)
        self.tracks_charge = np.zeros(self.maxtracks, dtype=np.float32)
        
        self.pftree.Branch("ntracks", self.ntracks, "ntracks/i")
        self.pftree.Branch("tracks_pt", self.tracks_pt, "tracks_pt[ntracks]/F")
        self.pftree.Branch("tracks_eta", self.tracks_eta, "tracks_eta[ntracks]/F")
        self.pftree.Branch("tracks_phi", self.tracks_phi, "tracks_phi[ntracks]/F")
        self.pftree.Branch("tracks_charge", self.tracks_charge, "tracks_charge[ntracks]/F")
       
        #http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_10_6_2/doc/html/dc/d55/classreco_1_1PFCandidate.html 
        self.npfcands = np.zeros(1, dtype=np.uint32)
        self.maxpfcands = 1000
        self.pfcands_pt = np.zeros(self.maxpfcands, dtype=np.float32)
        self.pfcands_eta = np.zeros(self.maxpfcands, dtype=np.float32)
        self.pfcands_phi = np.zeros(self.maxpfcands, dtype=np.float32)
        self.pfcands_charge = np.zeros(self.maxpfcands, dtype=np.float32)
        self.pfcands_energy = np.zeros(self.maxpfcands, dtype=np.float32)
        self.pfcands_pdgid = np.zeros(self.maxpfcands, dtype=np.int32)
        
        self.pftree.Branch("npfcands", self.npfcands, "npfcands/i")
        self.pftree.Branch("pfcands_pt", self.pfcands_pt, "pfcands_pt[npfcands]/F")
        self.pftree.Branch("pfcands_eta", self.pfcands_eta, "pfcands_eta[npfcands]/F")
        self.pftree.Branch("pfcands_phi", self.pfcands_phi, "pfcands_phi[npfcands]/F")
        self.pftree.Branch("pfcands_charge", self.pfcands_charge, "pfcands_charge[npfcands]/F")
        self.pftree.Branch("pfcands_energy", self.pfcands_energy, "pfcands_energy[npfcands]/F")
        self.pftree.Branch("pfcands_pdgid", self.pfcands_pdgid, "pfcands_pdgid[npfcands]/I")

    def close(self):
        self.tfile.Write()
        self.tfile.Close()

    def clear(self):
        self.nclusters[0] = 0        
        self.clusters_layer[:] = 0
        self.clusters_depth[:] = 0
        self.clusters_type[:] = 0
        self.clusters_energy[:] = 0
        self.clusters_x[:] = 0
        self.clusters_y[:] = 0
        self.clusters_z[:] = 0
        
        self.ngenparticles[0] = 0
        self.genparticles_pt[:] = 0 
        self.genparticles_eta[:] = 0
        self.genparticles_phi[:] = 0
        self.genparticles_x[:] = 0
        self.genparticles_y[:] = 0
        self.genparticles_z[:] = 0
        self.genparticles_pdgid[:] = 0
        
        self.ntracks[0] = 0
        self.tracks_pt[:] = 0
        self.tracks_eta[:] = 0
        self.tracks_phi[:] = 0
        self.tracks_charge[:] = 0
        
        self.npfcands[0] = 0
        self.pfcands_pt[:] = 0
        self.pfcands_eta[:] = 0
        self.pfcands_phi[:] = 0
        self.pfcands_charge[:] = 0
        self.pfcands_energy[:] = 0
        self.pfcands_pdgid[:] = 0
 
def fill_clusters(source, output, cluster_type, nclusters):
    for cl in sorted(source, key=lambda x: x.energy(), reverse=True):
        output.clusters_layer[nclusters] = int(cl.layer())
        output.clusters_depth[nclusters] = cl.depth()
        output.clusters_energy[nclusters] = cl.energy()
        output.clusters_x[nclusters] = cl.x()
        output.clusters_y[nclusters] = cl.y()
        output.clusters_z[nclusters] = cl.z()
        output.clusters_type[nclusters] = cluster_type
        nclusters += 1

    return nclusters 

if __name__ == "__main__":
    evdesc = EventDesc()
    output = Output()
    
    # loop over events
    for event in events:
        eid = event.object().id()
        eventId = (eid.run(), eid.luminosityBlock(), int(eid.event()))
        print(eventId)
    
        evdesc.get(event)
        output.clear()
    
        genpart = evdesc.genparticle.product()
        ngenparticles = 0
        for gp in sorted(genpart, key=lambda x: x.pt(), reverse=True):
            if gp.status() == 2:
                output.genparticles_pt[ngenparticles] = gp.pt() 
                output.genparticles_eta[ngenparticles] = gp.eta() 
                output.genparticles_phi[ngenparticles] = gp.phi() 
                output.genparticles_pdgid[ngenparticles] = gp.pdgId() 
                output.genparticles_x[ngenparticles] = gp.px() 
                output.genparticles_y[ngenparticles] = gp.py() 
                output.genparticles_z[ngenparticles] = gp.pz() 
                ngenparticles += 1
        output.ngenparticles[0] = ngenparticles
     
        pfcluster_ecal = evdesc.pfcluster_ecal.product()
        nclusters = 0
        nclusters = fill_clusters(pfcluster_ecal, output, 0, nclusters)  
        assert(nclusters == len(pfcluster_ecal))
    
        pfcluster_hcal = evdesc.pfcluster_hcal.product()
        nclusters = fill_clusters(pfcluster_hcal, output, 1, nclusters)
        assert(nclusters == len(pfcluster_ecal) + len(pfcluster_hcal))
      
        pfcluster_hf = evdesc.pfcluster_hf.product()
        nclusters = fill_clusters(pfcluster_hf, output, 2, nclusters)
        output.nclusters[0] = nclusters
        
        tracks = evdesc.tracks.product()
        ntracks = 0
        for c in sorted(tracks, key=lambda x: x.pt(), reverse=True):
            output.tracks_pt[ntracks] = c.pt()
            output.tracks_eta[ntracks] = c.eta()
            output.tracks_phi[ntracks] = c.phi()
            output.tracks_charge[ntracks] = c.charge()
            ntracks += 1
        output.ntracks[0] = ntracks
        
        pfcand = evdesc.pfcand.product()
        npfcands = 0
        for c in sorted(pfcand, key=lambda x: x.pt(), reverse=True):
            output.pfcands_pt[npfcands] = c.pt()
            output.pfcands_eta[npfcands] = c.eta()
            output.pfcands_phi[npfcands] = c.phi()
	    output.pfcands_charge[npfcands] = c.charge()
	    output.pfcands_energy[npfcands] = c.energy()
            output.pfcands_pdgid[npfcands] = c.pdgId()
            npfcands += 1
        output.npfcands[0] = npfcands
        output.pftree.Fill()
    pass 
    #end of event loop 

    output.close()
