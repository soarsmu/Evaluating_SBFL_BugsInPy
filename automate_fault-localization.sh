#!/bin/bash
DONE=false
  until $DONE ;do
  read || DONE=true
  if [ "$REPLY" != "" ]; then
     project="$(cut -d' ' -f 1 <<< $REPLY)"
     amount="$(cut -d' ' -f 2 <<< $REPLY)"
     for i in $(seq 1 $amount); do 
         bugsinpy-checkout -p $project -i $i -v 0 -w /mnt/e/FAULTLOC_BUGSINPY/$project_$i
         cd /mnt/e/FAULTLOC_BUGSINPY/$project_$i/$project
         bugsinpy-compile
         source env/bin/activate
         pip install git+https://github.com/nedbat/pytest-cov.git@nedbat/contexts
         pip install coverage>=5.1
         pip install pytest-pinpoint
         deactivate
         cp -v /mnt/e/pytest_pinpoint.py /mnt/e/FAULTLOC_BUGSINPY/$project_$i/$project/env/lib/python3.8/site-packages
         source env/bin/activate
         python -m pytest --cov=. --cov-context=test --cov-branch --pinpoint --show_all
         deactivate
     done
  fi
  done < running_file.txt
