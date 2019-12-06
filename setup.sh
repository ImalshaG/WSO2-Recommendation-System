#!/bin/bash
# script to setup the environment needed to run the recommendation server

pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_lg
python3 -m spacy link en_core_web_lg en
