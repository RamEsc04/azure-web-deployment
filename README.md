# Azure Web Deployment

Proyecto DevOps para automatizar el despliegue de una aplicación web desarrollada con Python y Flask en Microsoft Azure.

La solución utiliza infraestructura como código, contenedores, Kubernetes y un pipeline de GitHub Actions para automatizar la construcción, publicación y despliegue de la aplicación.

## Problemática

Current Lighting utiliza Daintree Control Systems (DCS), una aplicación web para la administración y monitoreo de sistemas de iluminación inteligente utilizada por clientes y agentes de soporte para la resolución de problemas y el monitoreo de los sistemas.

Actualmente, las actualizaciones de la aplicación se realizan manualmente por el equipo de ingeniería. Los cambios se comparten mediante correo electrónico y Microsoft Teams, lo que requiere la intervención del personal responsable para implementar los cambios y validar el funcionamiento de la plataforma.

Este proceso manual puede ocasionar:

- Mayor tiempo de implementación.
- Errores durante el despliegue.
- Falta de estandarización.
- Dependencia de intervención manual.
- Dificultad para mantener la trazabilidad de los cambios.
- Diferencias entre versiones y ambientes.

## Objetivo

Diseñar e implementar un proceso DevOps que permita automatizar la construcción, publicación y despliegue de una aplicación web Flask en Microsoft Azure.

La solución busca:

- Reducir la intervención manual.
- Disminuir errores durante los despliegues.
- Estandarizar el proceso de actualización.
- Mantener trazabilidad entre el código y la imagen desplegada.
- Centralizar las imágenes de contenedor.
- Facilitar la validación de la aplicación.
- Mantener una infraestructura reproducible mediante Bicep.

## Arquitectura de la solución

El flujo general del proyecto es:

```text
Desarrollador
     |
     v
Repositorio de GitHub
     |
     v
GitHub Actions
     |
     v
Autenticación con Azure
     |
     v
Construcción de imagen Docker
     |
     v
Azure Container Registry
webdeploymentprojectre1
     |
     v
Azure Kubernetes Service
web-deployment-project-re1-aks
     |
     v
Deployment app-flask
     |
     v
2 pods de Kubernetes
     |
     v
Service LoadBalancer
app-flask-service
     |
     v
Aplicación web disponible
```

## Tecnologías

- Git
- GitHub
- GitHub Actions
- Python
- Flask
- Docker
- Bicep
- Microsoft Azure
- Azure Container Registry
- Azure Kubernetes Service
- Azure Key Vault
- Azure App Service
- Azure Log Analytics
- Kubernetes
- Azure CLI
- PowerShell

## Recursos implementados en Azure

| Recurso | Nombre | Función |
|---|---|---|
| Resource Group | `rg-devops-curso-RE1` | Agrupa y administra los recursos del proyecto |
| Azure Container Registry | `webdeploymentprojectre1` | Almacena las imágenes Docker de la aplicación |
| Azure App Service | `webapp-devops-cursore1` | Servicio de alojamiento de aplicaciones web |
| Azure Key Vault | `web-deployment-re1-kv` | Almacena secretos y valores sensibles |
| Log Analytics Workspace | `web-deployment-project-re1-logs` | Centraliza registros y datos de monitoreo |
| Azure Kubernetes Service | `web-deployment-project-re1-aks` | Ejecuta y administra la aplicación contenerizada |

## Azure Container Registry

El registro utilizado para almacenar la imagen Docker es:

```text
webdeploymentprojectre1
```

La dirección del servidor del registro es:

```text
webdeploymentprojectre1.azurecr.io
```

La imagen utilizada por la aplicación es:

```text
azure-web-app:v1
```

La referencia completa de la imagen es:

```text
webdeploymentprojectre1.azurecr.io/azure-web-app:v1
```

La imagen fue construida directamente en Azure Container Registry con:

```powershell
az acr build `
  --registry webdeploymentprojectre1 `
  --image azure-web-app:v1 `
  --file .\docker\Dockerfile `
  .
```

Este comando:

1. Envía los archivos del proyecto a Azure.
2. Utiliza el archivo `docker/Dockerfile`.
3. Construye la imagen Docker.
4. Asigna la etiqueta `v1`.
5. Almacena la imagen en Azure Container Registry.

## Azure Kubernetes Service

El clúster utilizado para desplegar la aplicación es:

```text
web-deployment-project-re1-aks
```

AKS administra:

- Deployments.
- Pods.
- Réplicas.
- Servicios.
- Actualizaciones de la aplicación.
- Recuperación automática de contenedores.
- Integración con Azure Container Registry.

## Configuración de Kubernetes

La aplicación fue desplegada con la siguiente configuración:

| Propiedad | Valor |
|---|---|
| Namespace | `labfinal-re1` |
| Deployment | `app-flask` |
| Réplicas deseadas | `2` |
| Réplicas disponibles | `2` |
| Pods en ejecución | `2` |
| Service | `app-flask-service` |
| Tipo de Service | `LoadBalancer` |
| Puerto | `80` |
| IP pública | `20.245.48.19` |

## Deployment

El Deployment utilizado para la aplicación se llama:

```text
app-flask
```

Su función es:

- Crear los pods de la aplicación Flask.
- Mantener dos réplicas disponibles.
- Utilizar la imagen almacenada en ACR.
- Recuperar los pods si alguno falla.
- Permitir futuras actualizaciones de la imagen.

La validación del Deployment se realizó con:

```powershell
kubectl get deployments -n labfinal-re1
```

Resultado esperado:

```text
NAME        READY   UP-TO-DATE   AVAILABLE
app-flask   2/2     2            2
```

## Pods

El Deployment creó dos pods para ejecutar la aplicación.

La validación se realizó con:

```powershell
kubectl get pods -n labfinal-re1
```

El resultado confirmó que ambos pods se encontraban en estado:

```text
READY    STATUS
1/1      Running
1/1      Running
```

Esto indica que:

- Los contenedores iniciaron correctamente.
- La imagen pudo descargarse desde ACR.
- La aplicación se encuentra ejecutándose.
- Las dos réplicas están disponibles.

## Service

El servicio utilizado para exponer la aplicación se llama:

```text
app-flask-service
```

Su tipo es:

```text
LoadBalancer
```

La validación se realizó con:

```powershell
kubectl get service app-flask-service -n labfinal-re1
```

Configuración obtenida:

```text
NAME                TYPE           CLUSTER-IP    EXTERNAL-IP    PORT
app-flask-service   LoadBalancer   10.0.17.81   20.245.48.19   80
```

La aplicación puede accederse mediante:

```text
http://20.245.48.19
```

> La dirección IP pública puede cambiar si el servicio no tiene configurada una IP estática.

## Ambiente implementado

La versión actual del proyecto utiliza:

- Resource Group: `rg-devops-curso-RE1`
- Namespace: `labfinal-re1`
- Deployment: `app-flask`
- Réplicas: `2`
- Imagen: `azure-web-app:v1`
- Service: `app-flask-service`
- Tipo: `LoadBalancer`
- Puerto: `80`

## Infraestructura con Bicep

La infraestructura se define en:

```text
infra/main.bicep
```

El archivo Bicep permite crear de forma automatizada y reproducible:

- Azure Container Registry.
- Azure Kubernetes Service.
- Azure Key Vault.
- Log Analytics Workspace.
- Azure App Service.
- Identidades y configuraciones relacionadas.

La plantilla puede validarse con:

```powershell
az bicep build --file .\infra\main.bicep
```

El despliegue se realiza con:

```powershell
az deployment group create `
  --resource-group rg-devops-curso-RE1 `
  --template-file .\infra\main.bicep
```

## Pipeline de GitHub Actions

GitHub Actions automatiza el proceso de integración y despliegue continuo.

El pipeline realiza las siguientes etapas:

1. Descarga el código del repositorio.
2. Inicia sesión en Microsoft Azure.
3. Utiliza las credenciales almacenadas en GitHub Secrets.
4. Construye la imagen Docker.
5. Publica la imagen en Azure Container Registry.
6. Obtiene las credenciales del clúster AKS.
7. Aplica los manifiestos de Kubernetes.
8. Actualiza el Deployment.
9. Verifica el estado del despliegue.

## Autenticación con Azure

GitHub Actions utiliza un Service Principal para autenticarse con Microsoft Azure.

Las credenciales se almacenan dentro de GitHub Secrets y no se publican en el repositorio.

El secreto configurado para la autenticación es:

```text
AZURE_CREDENTIALS
```

No deben almacenarse en el código:

- Client Secret.
- Contraseñas.
- Tokens.
- Credenciales de Azure.
- Claves de acceso.
- Datos sensibles.

## Comandos de verificación

Obtener las credenciales del clúster:

```powershell
az aks get-credentials `
  --resource-group rg-devops-curso-RE1 `
  --name web-deployment-project-re1-aks
```

Verificar el Deployment:

```powershell
kubectl get deployments -n labfinal-re1
```

Verificar los pods:

```powershell
kubectl get pods -n labfinal-re1
```

Verificar el servicio:

```powershell
kubectl get service app-flask-service -n labfinal-re1
```

Ver información detallada del Deployment:

```powershell
kubectl describe deployment app-flask -n labfinal-re1
```

Ver los logs de un pod:

```powershell
kubectl logs -n labfinal-re1 <nombre-del-pod>
```

Verificar el estado del rollout:

```powershell
kubectl rollout status deployment/app-flask -n labfinal-re1
```

## Resultados

Al finalizar el proyecto se confirmó que:

- La infraestructura fue creada correctamente en Azure.
- Los recursos se encuentran dentro de `rg-devops-curso-RE1`.
- La imagen Docker fue construida en Azure Container Registry.
- AKS pudo acceder a la imagen almacenada en ACR.
- El Deployment creó dos réplicas de la aplicación.
- Los dos pods se encuentran en estado `Running`.
- El Service de tipo LoadBalancer asignó una IP pública.
- La aplicación puede accederse mediante el puerto 80.
- GitHub Actions puede autenticarse con Azure mediante un Service Principal.
- Los secretos se mantienen fuera del código fuente.
- El despliegue puede ejecutarse automáticamente desde GitHub.

## Beneficios de la solución

- Automatización del proceso de despliegue.
- Reducción de errores manuales.
- Menor tiempo de implementación.
- Versionamiento de imágenes.
- Trazabilidad de cambios.
- Infraestructura reproducible.
- Alta disponibilidad mediante dos réplicas.
- Recuperación automática de pods.
- Protección de secretos.
- Monitoreo centralizado mediante Log Analytics.

## Estado del proyecto

- [x] Resource Group
- [x] Repositorio en GitHub
- [x] Aplicación Flask
- [x] Dockerfile
- [x] Infraestructura con Bicep
- [x] Azure Container Registry
- [x] Construcción de imagen en ACR
- [x] Azure Kubernetes Service
- [x] Azure Key Vault
- [x] Log Analytics Workspace
- [x] Azure App Service
- [x] Manifiestos de Kubernetes
- [x] Namespace de Kubernetes
- [x] Deployment con dos réplicas
- [x] Service de tipo LoadBalancer
- [x] Service Principal
- [x] GitHub Secrets
- [x] Pipeline con GitHub Actions
- [x] Despliegue automatizado
- [x] Verificación de pods y servicios
- [ ] Ambiente de QA
- [ ] Ambiente de producción
- [ ] Estrategia automática de rollback

## Autor

Proyecto desarrollado como práctica de implementación DevOps utilizando GitHub Actions, Docker, Bicep, Kubernetes y Microsoft Azure.
