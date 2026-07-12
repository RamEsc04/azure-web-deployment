targetScope = 'resourceGroup'

@description('Región donde se crearán los recursos.')
param location string = resourceGroup().location

@description('Tamaño de la máquina virtual del nodo de AKS.')
param aksNodeVmSize string = 'Standard_D2s_v3'

@description('Cantidad inicial de nodos de AKS.')
@minValue(1)
@maxValue(3)
param aksNodeCount int = 1

// Nombres fijos y descriptivos para los recursos.
var acrName = 'webdeploymentprojectre1'
var keyVaultName = 'web-deployment-re1-kv'
var aksName = 'web-deployment-project-re1-aks'
var logAnalyticsName = 'web-deployment-project-re1-logs'
var dnsPrefix = 'web-deployment-re1'

var commonTags = {
  environment: 'dev'
  project: 'azure-web-deployment'
}

// Azure Container Registry
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2025-04-01' = {
  name: acrName
  location: location

  sku: {
    name: 'Basic'
  }

  properties: {
    adminUserEnabled: false
    anonymousPullEnabled: false
    dataEndpointEnabled: false
    publicNetworkAccess: 'Enabled'
  }

  tags: commonTags
}

// Azure Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2025-05-01' = {
  name: keyVaultName
  location: location

  properties: {
    tenantId: tenant().tenantId

    sku: {
      family: 'A'
      name: 'standard'
    }

    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    publicNetworkAccess: 'Enabled'
    accessPolicies: []
  }

  tags: commonTags
}

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location

  properties: {
    retentionInDays: 30

    sku: {
      name: 'PerGB2018'
    }
  }

  tags: commonTags
}

// Azure Kubernetes Service
resource aksCluster 'Microsoft.ContainerService/managedClusters@2024-10-01' = {
  name: aksName
  location: location

  identity: {
    type: 'SystemAssigned'
  }

  properties: {
    dnsPrefix: dnsPrefix
    enableRBAC: true

    agentPoolProfiles: [
      {
        name: 'systempool'
        count: aksNodeCount
        vmSize: aksNodeVmSize
        osType: 'Linux'
        osSKU: 'Ubuntu'
        mode: 'System'
        type: 'VirtualMachineScaleSets'
        osDiskSizeGB: 30
      }
    ]

    networkProfile: {
      networkPlugin: 'kubenet'
      loadBalancerSku: 'standard'
    }

    addonProfiles: {
      omsagent: {
        enabled: true

        config: {
          logAnalyticsWorkspaceResourceID: logAnalytics.id
        }
      }
    }
  }

  tags: commonTags
}

// Salidas del despliegue
output containerRegistryName string = containerRegistry.name
output containerRegistryLoginServer string = containerRegistry.properties.loginServer
output keyVaultName string = keyVault.name
output aksClusterName string = aksCluster.name
output logAnalyticsWorkspaceName string = logAnalytics.name