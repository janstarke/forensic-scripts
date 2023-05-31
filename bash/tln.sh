#!/bin/bash

HOST=$(basename $(pwd))

PATH="/home/jasa/work/development/gist:/home/jasa/perl5/bin${PATH:+:${PATH}}"; export PATH;
PERL5LIB="/home/jasa/work/development/RegRipper3.0:/home/jasa/perl5/lib/perl5${PERL5LIB:+:${PERL5LIB}}"; export PERL5LIB;
PERL_LOCAL_LIB_ROOT="/home/jasa/perl5${PERL_LOCAL_LIB_ROOT:+:${PERL_LOCAL_LIB_ROOT}}"; export PERL_LOCAL_LIB_ROOT;
PERL_MB_OPT="--install_base \"/home/jasa/perl5\""; export PERL_MB_OPT;
PERL_MM_OPT="INSTALL_BASE=/home/jasa/perl5"; export PERL_MM_OPT;
rip="perl /home/jasa/work/development/RegRipper3.0/rip.pl"

function tln2csv {
      egrep '^[0-9]+\|' | awk -F '|' '{OFS="|";if ($4 == "") {print 0,$5,0,0,0,0,0,-1,$1,-1,-1} else {print 0,("<" $4 "> " $5),0,0,0,0,0,-1,$1,-1,-1} }' |mactime2 -b - -d
}

if [ ! -d "../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles" ]; then
  echo "../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles does not exist" >&2
  exit 2
fi

mkdir -p timeline
$rip -r ../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles/registry/SOFTWARE -p winver >winver.txt
$rip -r ../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles/registry/SYSTEM -p compname >compname.txt

if [ ! -f timeline/vol_c.csv.gz ]; then
  mft2bodyfile ../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles/mft/\$MFT | mactime2 -d | gzip -c >timeline/vol_c.csv.gz
fi

if [ ! -f timeline/evtx.csv.gz ]; then
  evtx2bodyfile ../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles/eventlogs/Logs/*.evtx | mactime2 -d | gzip -c >timeline/evtx.csv.gz
fi

(cd ../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles/registry; for F in *_NTUSER.DAT; do $rip -r "$F" -aT | tln2csv >../../../../../../10-WorkItems/$HOST/timeline/"tln_$(echo $F |sed 's/_NTUSER.DAT//').csv";  done )

$rip -r ../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles/registry/SOFTWARE -aT |tln2csv >timeline/software.csv
$rip -r ../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles/registry/SYSTEM -aT |tln2csv >timeline/system.csv
$rip -r ../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles/amcache/Amcache.hve -aT | tln2csv >timeline/amcache.csv
$rip -r ../../00-RawData/03-Triage/$HOST/LiveResponseData/CopiedFiles/registry/SAM -aT | tln2csv >timeline/sam.csv
