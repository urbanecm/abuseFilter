#!/bin/bash

cd ~/abuseFilter
python abuseFilter.py > result.json
python to_db.py
