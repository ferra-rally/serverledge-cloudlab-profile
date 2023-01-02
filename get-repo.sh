#!/usr/bin/env sh

git clone https://"$1"@github.com/ferra-rally/serverledge.git
cd serverledge
wget https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/config.yaml
wget https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/config_cloud.yaml
wget https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/classes.json
wget https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/start-prometheus.sh
wget https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/stop-prometheus.sh
wget https://raw.githubusercontent.com/ferra-rally/serverledge-cloudlab-profile/main/prometheus.yaml
PATH=$PATH:/usr/local/go/bin make
PATH=$PATH:/usr/local/go/bin:/opt/jdk-18 JAVA_HOME=/opt/jdk-18  bash