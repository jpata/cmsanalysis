
## Resubmitting NanoAOD on local queues
```
python prepare_inputs.txt
condor_submit job.jdl
```


## Skimming and merging NanoAODs

Prepare a the file lists that you want to merge:

```bash
$ mkdir my_merge; cd my_merge

#prepare txt file with filenames for each dataset you want to merge
$ wc -l ttjets_sl_2017.txt
120 ttjets_sl_2017.txt

$ head -n5 ttjets_sl_2017.txt
/storage/user/jpata/store/mc/RunIIFall17NanoAODv5/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/9F9008FA-6F7E-4548-A188-79AE98F871FA.root
/storage/user/jpata/store/mc/RunIIFall17NanoAODv5/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/5F9459CA-8505-C34B-879E-7C87578B7951.root
/storage/user/jpata/store/mc/RunIIFall17NanoAODv5/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/3304ABCD-DD82-CC48-B1AF-A6DAE1CEC349.root
/storage/user/jpata/store/mc/RunIIFall17NanoAODv5/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/BBCE8E57-758F-2941-8F8A-4A6F5F35B2B7.root
/storage/user/jpata/store/mc/RunIIFall17NanoAODv5/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/44C5336D-0BF7-5B4D-804F-5B5DE682C8C9.root

#split each dataset into 10 chunks
$ for f in *.txt; do split -l10 -a5 $f ${f}.split.; done
```
