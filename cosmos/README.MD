
https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-s3


https://www.thomasmaurer.ch/2019/05/how-to-install-azcopy-for-azure-storage/
https://askubuntu.com/questions/688956/bash-usr-bin-lein-permission-denied

Replace azcopy folder

https://github.com/Azure/azure-storage-azcopy/issues/452

If this error comes up

 RESPONSE Status: 403 This request is not authorized to perform this operation using this permission.



https://stackoverflow.com/questions/60602497/azcopy-error-this-request-is-not-authorized-to-perform-this-operation


https://github.com/Azure/azure-storage-azcopy/issues/452




https://github.com/Azure/azure-cosmos-python for python 

https://docs.microsoft.com/en-us/azure/cosmos-db/sql/quickstart-dotnet?tabs=azure-cli%2Clinux for cli


before start python set these 

RES_GROUP=Msdocs-cosmosdb-rg-13976262
ACCT_NAME=msdocs-account-cosmos-13976262
export ACCOUNT_URI=$(az cosmosdb show --resource-group $RES_GROUP --name $ACCT_NAME --query documentEndpoint --output tsv)
export ACCOUNT_KEY=$(az cosmosdb keys list --resource-group $RES_GROUP --name $ACCT_NAME --query primaryMasterKey --output tsv)