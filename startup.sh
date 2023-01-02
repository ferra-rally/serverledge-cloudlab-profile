#!/usr/bin/env sh

wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
python3 -m pip install --user ansible
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release prometheus nginx
echo "export PATH=$PATH:/usr/local/go/bin" >> "$HOME"/.profile
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
wget  https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/get-repo.sh -P $HOME

mkdir -p /usr/java
curl -O https://download.java.net/java/GA/jdk18/43f95e8614114aeaa8e8a5fcf20a682d/36/GPL/openjdk-18_linux-x64_bin.tar.gz
tar xvf openjdk-18_linux-x64_bin.tar.gz
sudo mv jdk-18 /opt/

mkdir -p /usr/jmeter
wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.5.tgz -P /usr/jmeter
tar -zxvf /usr/jmeter/apache-jmeter-5.5.tgz

sudo wget  https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/nginx.conf -P /etc/nginx/nginx.conf
sudo systemctl start nginx
setenv PATH ${PATH}:"/usr/local/go/bin"
bash
