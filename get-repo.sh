#!/usr/bin/env sh

git clone https://"$1"@github.com/ferra-rally/serverledge.git
cd serverledge
wget https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/config.yaml
wget https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/config_cloud.yaml
wget https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/classes.json
PATH=$PATH:/usr/local/go/bin make
PATH=$PATH:/usr/local/go/bin bash