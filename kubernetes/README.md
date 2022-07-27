README.MD

Step 1-
    Install Az CLI and login your azure account
    https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt

Step 2-
    AZ Login
        https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli

Step 3-
    1-Az account list
    2-get subscription id
    3-Set Subscription ID (https://docs.microsoft.com/en-us/azure/cloud-shell/quickstart)
      az account set --subscription 4266b0d8-0c3d-4df1-a542-21d9e8135d1e

Step 4
    1-Install kubectl
        https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest
    2-get node pools az aks nodepool   
    3- create cluster az aks create
    4-az aks get-credentials

Step 5

Install ELK
    1-create resource group and then crate cluster if you not created  otherwise start from step 2
        https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-cli

    2-    az aks get-credentials --resource-group DefaultResourceGroup-CUS --name elk
    3-rest follow commands

 https://www.elastic.co/blog/how-to-run-elastic-cloud-on-kubernetes-from-azure-kubernetes-service

Importna Coammands
 az account set --subscription 4266b0d8-0c3d-4df1-a542-21d9e8135d1e
 az aks get-credentials --resource-group DefaultResourceGroup-CUS --name elk
 kubectl create -f kube-logging.yaml
 kubectl get namespaces
 kubectl create -f elasticsearch_svc.yaml
 kubectl get services --namespace=kube-logging
 kubectl apply -f service-manifest.yaml
 kubectl rollout status sts/es-cluster --namespace=kube-logging
 kubectl get storageclass
 kubectl get services --namespace=elasticsearch_statefulset
 kubectl get nodes
 kubectl delete node es-cluster-0
 kubectl get namespaces
 kubectl get deployments
 kubectl get deployments --all-namespaces
 kubectl delete deployment kube-logging
 kubectl get pod --all-namespaces
 kubectl delete pods --namespace=kube-logging kibana-84cf7f59c-vhsx6 --force
 kubectl kill pods --namespace=kube-logging
 https://stackoverflow.com/questions/47685246/kubectl-update-service-with-new-label-and-service-names