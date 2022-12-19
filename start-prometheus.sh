#!/usr/bin/env sh

# Start Prometheus
sudo prometheus --config.file=prometheus.yaml --web.listen-address=:8080 --web.enable-admin-api