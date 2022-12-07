#!/bin/bash

# Install microk8s
sudo snap install microk8s --classic --channel=1.22/stable

# Add user to microk8s group
sudo usermod -a -G microk8s $USER
newgrp microk8s
sudo chown -f -R $USER ~/.kube

microk8s status --wait-ready

# Enable microk8s addons
#   - dns: so the applications can find each other
#   - storage & ingress: controller so we can access Kubeflow components and the MetalLB load balancer application
#   - registry: so we can push images to the local registry
#   - dashboard: so we can access the Kubernetes dashboard
#   - istio & metallb: so we can use the Kubeflow Pipelines UI
sudo microk8s enable dns storage registry ingress istio dashboard metallb:10.64.140.43-10.64.140.49

microk8s status --wait-ready

# Alias kubectl to microk8s kubectl
# echo `alias kubectl='microk8s kubectl'` >> ~/.bash_aliases
# source ~/.bash_aliases

# Install JUJU
sudo snap install juju --classic

juju bootstrap microk8s

# Deploy Kubeflow
juju add-model kubeflow
juju deploy kubeflow-lite --trust
watch -c juju status --color