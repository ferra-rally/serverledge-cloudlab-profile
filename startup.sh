#!/usr/bin/env sh

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
python3 -m pip install --user ansible