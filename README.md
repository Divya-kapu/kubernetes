# kubernetes
Projects on K8s and affiliates

## Python applications overview. 

Application contains three micro services  which together calculate acceleration by reading necessary parameters from from input URL 

Output return from these micro services is in JSON format.

## Docker installation: 

Install docker desktop by using below url.
https://docs.docker.com/desktop/install/mac-install/

Steps to build own docker images in private registry:

Step 1: 
Create private registry to pull the docker images.
docker run -d -p 5000:5000  --name registry registry:2

Step2:
Create Docker image using docker file.

Step3:
Tag the image to private repository, so that the images can be pushed into private repository.

Step4:
Push the tagged image to private repository.


## K8s cluster Installation: 

Installed k8s cluster using minikube with docker desktop.

########### 
*brew install minikube*
########### 
*minikube start —driver=docker*
########### 
*eval $(minikube docker-env)* 

Steps to spin up the kubernetes objects using helm chart, from the images created earlier

Step1:
Create the helm chart by using below command
helm create <chart name>

Step2:
Create the yaml file templates to create the kubernetes objects.
helm install <release name> <absolute path of the chart folder>

Steps to integrate custom metrics from app that running as a container in cluster.

We have to integrate the servicemonitor created in previous steps using helm to prometheus.

## Steps to install prometheus and Alertmanager using helm: 

Step1:
Reference url for installing prometheus stack with helm  below:
https://dev.to/kaitoii11/deploy-prometheus-monitoring-stack-to-kubernetes-with-a-single-helm-chart-2fbd
https://www.containiq.com/post/prometheus-alertmanager

We have to integrate the prometheus rules and alert manager with Prometheus.

## Steps to integrate the alert manager with slack to get the alert notifications. 

Step1:
Create the slack account —> Browse Slack —> Apps —> Incoming WebHooks —> Add channel to get notified —> copy the webhook URL.

Step2:
Create the alert-manager-config file and run the below command, so that alertmnager use this config file to notify these alerts in slack.
helm upgrade - to deploy the new onfig files
  
helm upgrade --reuse-values -f alertmanager-config.yaml prometheus prometheus-community/kube-prometheus-stack 

alert-manager-config file contains the details of the slack web hook url and the channel name and the text details.

