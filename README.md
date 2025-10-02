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

#### Implementación

Se ha creado un rol de Ansible que:

- Instala paquetes genéricos del sistema.
- Registra automáticamente un GitHub Actions self-hosted runner en el repositorio [`krage3x/devops-prueba-tecnica`](https://github.com/krage3x/devops-prueba-tecnica).
- Se ha probado en una máquina virtual local para validar su correcto funcionamiento.
