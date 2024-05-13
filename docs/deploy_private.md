
# Deploying with private access

If you want to disable public access when deploying the Chat App, you can do so by setting `azd` environment values.

## Before you begin

Deploying with public access disabled adds additional cost to your deployment. Please see pricing for the following products:

1. [Private Endpoints](https://azure.microsoft.com/pricing/details/private-link/)
  1. The exact number of private endpoints created depends on the [optional features](./deploy_features.md) used.
1. [Private DNS Zones](https://azure.microsoft.com/en-in/pricing/details/dns/)
1. (Optional, but recommended)[Azure Virtual Machines](https://azure.microsoft.com/pricing/details/virtual-machines/windows/)
1. (Optional, but recommended)[Azure Bastion](https://azure.microsoft.com/pricing/details/azure-bastion/)

## Environment variables controlling private access

1. `AZURE_PUBLIC_NETWORK_ACCESS`: Controls the value of public network access on supported Azure resources. Valid values are 'Enabled' or 'Disabled'.
  1. When public network access is 'Enabled', Azure resources are open to the internet.
  1. When public network access is 'Disabled', Azure resources are only accessible over a virtual network.
1. `AZURE_USE_PRIVATE_ENDPOINT`: Controls deployment of [private endpoints](https://learn.microsoft.com/azure/private-link/private-endpoint-overview) which connect Azure resources to the virtual network.
  1. When set to 'true', ensures private endpoints are deployed for connectivity even when `AZURE_PUBLIC_NETWORK_ACCESS` is 'Disabled'.
  1. Note that private endpoints do not make the chat app accessible from the internet. Connections must be initiated from inside the virtual network.
1. `AZURE_PROVISION_VM`: Controls deployment of a [virtual machine](https://learn.microsoft.com/azure/virtual-machines/overview) and [Azure Bastion](https://learn.microsoft.com/azure/bastion/bastion-overview). Azure Bastion allows you to securely connect to the virtual machine, without being connected virtual network. Since the virtual machine is connected to the virtual network, you are able to access the chat app.
  1. You must set `AZURE_VM_USERNAME` and `AZURE_VM_PASSWORD` to provision the built-in administrator account with the virtual machine so you can log in through Azure Bastion.

## Recommended deployment strategy for private access

1. Deploy the app with private endpoints enabled and public access enabled.
```
azd env set AZURE_USE_PRIVATE_ENDPOINT true
azd env set AZURE_PUBLIC_NETWORK_ACCESS Enabled
azd up
```
2. Validate that you can connect to the chat app and it's working as expected from the internet.
3. Re-provision the app with public access disabled.
```
azd env set AZURE_PUBLIC_NETWORK_ACCESS Disabled
azd env set AZURE_PROVISION_VM true # Optional but recommended
azd env set AZURE_VM_USERNAME myadminusername # https://learn.microsoft.com/azure/virtual-machines/windows/faq#what-are-the-username-requirements-when-creating-a-vm-
azd env set AZURE_VM_PASSWORD mypassword # https://learn.microsoft.com/azure/virtual-machines/windows/faq#what-are-the-password-requirements-when-creating-a-vm-
azd provision
```
4. Log into your new VM using [Azure Bastion](https://learn.microsoft.com/azure/bastion/tutorial-create-host-portal#connect). Validate the chat app is accessible from the virtual machine using a web browser.