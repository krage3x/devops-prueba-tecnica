# Prueba Técnica – DevOps

¡Hola!  
Gracias por participar en nuestro proceso. Esta prueba está pensada para que podamos ver cómo trabajas en el día a día como **DevOps**, más allá de la teoría.  

No buscamos que lo hagas todo perfecto ni que te pases horas afinando detalles. Lo que más valoramos es **cómo te organizas, cómo explicas tus decisiones y hasta dónde eres capaz de llegar con los conocimientos que tienes**.  

---

## ¿Qué pedimos?

La prueba se divide en varias partes. Hay apartados **obligatorios** (lo mínimo para considerarla bien resuelta) y otros **opcionales** (para quienes quieran ir un paso más allá).  

### 1. Contenedores y Kubernetes (obligatorio)
- Crea un `Dockerfile` para una aplicación sencilla (puede ser en **FastAPI** o **NodeJS**).  
- Haz un `docker-compose.yml` que levante:  
  - La aplicación  
  - Una base de datos **PostgreSQL**  
  - Un **Redis** como caché
- Dentro de la aplicación, debes crear un funcionamiento de un sistema de estaciones de carga de vehiculos electricos, no te compliques la vida, crear estacion, eliminar estacion, cambiar estado de estación, de disponible, ocupada...
- Un paso más sería tener en cuenta que cada estación tiene puntos de carga, y cada punto de carga conectores, en base de modificaciones de estos conectores, calcular estado del punto de carga y de la estación (más complejo, y opcional)
- Exponer metricas especiales del servicio en formato prometheus y proteger el endpoint.
- Prepara los manifiestos de Kubernetes para desplegar la aplicación (`Deployment`, `Service`, `ConfigMap/Secret`).  

> No es necesario montar un clúster en cloud; puedes usar `kind`, `k3d` o `minikube`.  
> En tus notas de ejecución debe quedar claro cómo construirlo y modificarlo.  

---

### 2. Automatización (obligatorio)
- Escribe un **playbook de Ansible** que instale dependencias básicas en un servidor Linux (ej.: `docker`, `kubectl`, `helm`).  
  - Escribe un **playbook de Ansible** que instale dependencias básicas en un servidor Linux (ej.: `docker`, `kubectl`, `helm`).  
  > Puedes probarlo en `localhost` o en una máquina virtual con Vagrant (¿o como pruebas tu los playbooks?;).  
- Añade un script sencillo en **Bash o Python** que compruebe el estado de los contenedores de tu aplicación.  

---

### 3. CI/CD (obligatorio + opcional)
- **Obligatorio:** Configura un **workflow en GitHub Actions** que construya y publique la imagen Docker (en Docker Hub o GitHub Container Registry).  
- **Opcional:** Integra con **ArgoCD** para desplegar automáticamente los manifiestos en Kubernetes.  

---

### 4. Monitorización y Alertas (obligatorio + opcional)
- **Obligatorio:**  
  - Levanta **Prometheus** y **Grafana** (con Compose o Helm).  
  - Expón  **varias métricas personalizadas** de tu aplicación y muestra cómo la visualizarías en un dashboard.   
  - Configura **Alertmanager** con Prometheus para que salte distintas alertas (ej.: si el endpoint `/healthz` no responde).  

---

## ¿Qué esperamos como entrega?

Dentro del repositorio deberán incluirse:  

- `Dockerfile`  
- `docker-compose.yml`  
- Carpeta `k8s/` con los manifiestos de Kubernetes  
- Carpeta `ansible/` con el playbook  
- Script `healthcheck.sh` o `healthcheck.py`  
- Workflow en `.github/workflows/ci.yml`  
- Carpeta `monitoring/` con la configuración de Prometheus/Grafana (y Alertmanager si lo implementas)  

Además:  
- Un **README** con instrucciones claras de cómo levantar cada parte.  
- (Opcional) Capturas de pantalla de Grafana o de una alerta funcionando.  
- El historial de commits completo (nos interesa ver tu proceso paso a paso).  

---

## Criterios de evaluación

- Que todo arranque y funcione en lo básico  
- La estructura de los archivos y buenas prácticas  
- El nivel de automatización en CI/CD  
- La calidad y utilidad de la monitorización y alertas  
- Lo claro y completo del README  
- Cómo explicas tus decisiones y qué mejoras propones  

Los apartados opcionales son valorados, pero **no son requisito**.  

---

## ⏱ Tiempo estimado

La parte obligatoria debería llevar entre **6 y 8 horas** aproximadamente.  
Dispondrás de **3-5 días hábiles** para completarla.  
Si existe fin de semana entre medias, no te preocupes, el lunes puedes entregarlo.

---

## 📦 Entrega

1. Sube el proyecto a un repositorio privado en GitHub o GitLab.  
2. Invítanos con este usuario:  
   - `carlos.cordoba@wenea.com`  
3. Si algo no lo pudiste terminar o lo dejarías como mejora, explícalo en el README.  

---

## Sobre el uso de IA

No queremos que la prueba se resuelva copiando directamente con IA.  

Sí valoramos la **transparencia**: si la usas en alguna parte, indícalo.  
Lo importante es tu criterio: que mejores lo que la IA te sugiera y no lo uses como un simple copiar/pegar.  

---

## Consejos finales

- Un **Makefile** puede ayudarte a documentar los pasos para levantar el sistema.  
- No pasa nada si algo no lo dominas: explica cómo lo resolverías.  
- Valoramos tu **claridad, proactividad y ganas de aprender**.  
- Y sobre todo… ¡disfrútalo! 🎉  

---

## Implementación
### 1. Contenedores y Kubernetes (obligatorio)

**Aplicación:**  
- Se ha desarrollado una aplicación sencilla en **FastAPI** para gestionar un sistema de estaciones de carga de vehículos eléctricos.  
- La aplicación incluye:  
  - **Estaciones de carga**  
  - **Puntos de carga** dentro de cada estación  
  - **Conectores** dentro de cada punto de carga, con su estado (disponible, ocupada, etc.)  

**Docker y métricas:**  
- Se ha creado un **Dockerfile** para la aplicación.  
- Se ha preparado un **docker-compose.yml** que levanta:  
  - La aplicación  
  - Una base de datos **PostgreSQL**  
  - **Redis** como caché  
  - **Prometheus** para pulling de metricas
  - **Grafana** Para visualizar dashboards
  - **Alertmanager** Para recibir alertas
- Se ha añadido la librería **Prometheus** para exponer métricas del servicio.  
- Se han creado **dashboards en Grafana** mostrando:  
  - Número total de requests por endpoint  
  - Latencias p90 por endpoint  
  - Histograma de latencias  
  - Errores 4xx y 5xx  

**Pendientes:**  
- Preparar los **manifiestos de Kubernetes** (`Deployment`, `Service`, `ConfigMap/Secret`) para desplegar la aplicación en un cluster (por ejemplo, usando `kind`, `k3d` o `minikube`).  

### 2. Automatización (obligatorio)

**Ansible:**  
- Se ha creado un **rol de Ansible** que:  
  - Instala paquetes genéricos del sistema (docker, kubectl, helm, etc.).  
  - Registra automáticamente un **GitHub Actions self-hosted runner** en el repositorio [`krage3x/devops-prueba-tecnica`](https://github.com/krage3x/devops-prueba-tecnica).  
- **Validación:**  
  - Se ha probado en una máquina virtual local para asegurar su correcto funcionamiento.  
- **Ejecución:**  
```bash
ansible-playbook -i inventory/hosts playbook.yml -vvvv --vault-password-file .vault_pass
```
### 3. CI/CD

**Integración Continua (CI):**  
- Se configuró un **workflow en GitHub Actions** que construye la imagen Docker de la aplicación FastAPI.  
- El workflow utiliza el **runner configurado previamente** en el repositorio.  
- La imagen resultante se publica automáticamente en un **registro privado** (Docker Hub o GitHub Container Registry).  
- La idea era que el workflow se disparara al recibir un push a `main` con una etiqueta o versión específica, pero **no se probó por falta de tiempo**.  

**Entrega Continua (CD):**  
- La integración con **ArgoCD** para despliegue automático en Kubernetes **no se implementó por tiempo**, pero el proyecto está preparado para añadirlo posteriormente.  

**Notas:**  
- Con este flujo, la imagen Docker se construye y actualiza automáticamente según el workflow definido.  
- Los manifiestos de Kubernetes pueden integrarse fácilmente con ArgoCD en el futuro para automatizar el despliegue.


### 4. Monitorización y Alertas

**Métricas personalizadas:**  
- Se añadieron métricas Prometheus en la aplicación FastAPI para exponer:  
  - Número de requests totales por endpoint.  
  - Latencias p90 por endpoint.  
  - Histograma de latencias.  
  - Errores 4xx y 5xx por endpoint y método.  

**Dashboards en Grafana:**  
- Se crearon paneles para visualizar:  
  - Total de requests por endpoint (bar chart).  
  - Latencias p90 y rangos de latencia (histogram/percentiles).  
  - Errores 4xx/5xx por endpoint y método.  
- Permiten identificar rápidamente endpoints críticos y su comportamiento.  

**Alertas con Prometheus + Alertmanager:**  
- Configuración de reglas genéricas de alerta:  
  - `HighLatencyP90`: dispara si la latencia p90 supera un umbral definido (por ejemplo, >3s).  
  - `High4xxErrorRate`: dispara si el ratio de errores 4xx supera un umbral (por ejemplo, 10%).  
- Las alertas se agrupan por `app`, `alertname` en Alertmanager, y se pueden enrutar a distintos receivers si se desea.  
- Alertmanager permite definir receivers genéricos o específicos para notificaciones (email, webhook, etc.).  

**Protección del endpoint `/metrics`:**  
- No se implementó autenticación o TLS por tiempo.  
- Si la comunicación es **interna en una red privada**, no es necesario proteger el endpoint `/metrics`.  
- Si se quiere exponer externamente, se recomienda usar un **proxy** que bloquee directamente el acceso a `/metrics` desde fuera de la red privada, evitando que se pueda consultar públicamente.