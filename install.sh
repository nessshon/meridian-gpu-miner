#!/bin/bash

sudo apt-get update

sudo apt-get install -y nano \
    software-properties-common \
    python3-software-properties

sudo add-apt-repository -y ppa:deadsnakes/ppa

sudo apt-get update

sudo apt-get install -y \
    python3.10 \
    python3.10-venv

python3.10 -m venv venv

source venv/bin/activate && pip install -r requirements.txt