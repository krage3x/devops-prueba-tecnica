# Proyecto Prueba tecnica

Este README contiene toda la información necesaria para levantar el sistema, incluyendo explicación de los Makefiles y cómo lanzar un rol de Ansible.

---

## 1. Explicación de este README

Este archivo centraliza la documentación del proyecto. Aquí encontrarás:

- Cómo usar los Makefiles para levantar los servicios.
- Instrucciones para lanzar roles de Ansible.

El objetivo es que este README sea la guía principal para cualquier desarrollador o administrador que necesite desplegar o mantener el sistema.

---

## 2. Uso de Makefiles

El proyecto incluye varios Makefiles para facilitar el despliegue tanto en Kubernetes como en Docker.

### 2.1 Despliegue en Kubernetes (`k8s.mk`)

Todos los pasos de despliegue están pensados para ejecutarse desde la carpeta `deployments` del proyecto, asegurando que los paths relativos a los charts funcionen correctamente.

#### Variables

- `WORKDIR`: Directorio donde se encuentran los charts. Por defecto `.` (directorio actual).

#### Comandos disponibles

```bash
# Levantar todos los servicios
make -f k8s.mk all WORKDIR=../infra/k8s

# Levantar solo PostgreSQL
make -f k8s.mk postgres WORKDIR=../infra/k8s

# Levantar solo Redis
make -f k8s.mk redis WORKDIR=../infra/k8s

# Levantar solo la app
make -f k8s.mk app WORKDIR=../infra/k8s

# Limpiar/desinstalar todos los recursos
make -f k8s.mk clean WORKDIR=../infra/k8s
```

### 2.2 Despliegue docker-compose

Este Makefile permite construir la imagen Docker de la aplicación y levantar los servicios con Docker Compose desde la carpeta `deployment`, cargando automáticamente los archivos `.env`.

#### Variables

- `DOCKER_IMAGE`: Nombre de la imagen Docker. Por defecto `charging-station-app`.  
- `TAG`: Tag de la imagen. Por defecto `latest`.  
- `DOCKERFILE_PATH`: Ruta al Dockerfile. Por defecto `../python-app/charging_station_app/docker/Dockerfile`.  
- `DOCKER_CONTEXT`: Contexto de build de Docker. Por defecto `../python-app/charging_station_app`.  
- `ENV_FILES`: Archivos `.env` que se cargan antes de levantar los servicios.

#### Reglas disponibles

```bash
# Construir la imagen Docker
make -f docker-compose.mk build TAG=0.1.0

# Levantar servicios con Docker Compose
make -f docker-compose.mk up 

# Limpiar servicios e imagen Docker
make -f docker-compose.mk clean 
```


### 3. Provisión del Bastion con Ansible

Para la provisión del bastion se utiliza un **rol de Ansible** incluido dentro del repositorio.  

#### 3.1 Preparación

- Asegúrate de tener el archivo `.vault_pass` con la contraseña de Vault.  
- Este archivo permite acceder a las variables encriptadas dentro de `group_vars`, incluyendo el token de GitHub necesario para configurar el runner.

#### 3.2 Modificar la variable del token de GitHub

Antes de ejecutar el playbook, debes actualizar el token:

```bash
cd infra/ansible
# Edit vault pasword
ansible-vault edit --vault-password-file .vault_pass group_vars/all/vault.yml
# Launch playbook
ansible-playbook -i inventory/hosts --vault-password-file .vault_pass playbook.yml
```
