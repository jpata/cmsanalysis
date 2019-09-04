#!/bin/bash
export DELPHES_PATH=/build/Delphes-3.4.2/
export WORKDIR=`pwd`
export CARD=`realpath delphes_card_CMS_PileUp.tcl`
cd $DELPHES_PATH
./DelphesPythia8 $CARD examples/Pythia8/configNoLHE.cmnd $WORKDIR/delphes_nolhe.root
