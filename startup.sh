#!/usr/bin/env sh

wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
python3 -m pip install --user ansible
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
echo "export PATH=$PATH:/usr/local/go/bin" >> "$HOME"/.profile
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
python3 -m pip install --user ansible