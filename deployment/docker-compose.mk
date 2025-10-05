
.PHONY: build up clean

DOCKER_IMAGE ?= charging-station-app
TAG ?= latest
DOCKERFILE_PATH ?= ../python-app/charging_station_app/docker/Dockerfile
DOCKER_CONTEXT ?= ../python-app/charging_station_app
ENV_FILES := ../python-app/charging_station_app/docker/.db-init.env \
             ../python-app/charging_station_app/docker/.postres.env \
             ../python-app/charging_station_app/docker/.app.env \
             ../python-app/charging_station_app/docker/.redis.env \
             ../python-app/charging_station_app/docker/.grafana.env

build:
	@echo "Construyendo imagen Docker $(DOCKER_IMAGE):$(TAG)..."
	docker build -t $(DOCKER_IMAGE):$(TAG) -f $(DOCKERFILE_PATH) $(DOCKER_CONTEXT)

up:
	@echo "Cargando variables de entorno..."
	@for env_file in $(ENV_FILES); do \
		if [ -f $$env_file ]; then \
			set -a; . $$env_file; set +a; \
		fi \
	done
	@echo "Levantando servicios con docker compose..."
	cd $(DOCKER_CONTEXT)/docker && docker compose up -d

clean:
	@echo "Deteniendo y eliminando contenedores..."
	cd $(DOCKER_CONTEXT)/docker && docker compose down
	@echo "Eliminando imagen Docker $(DOCKER_IMAGE):$(TAG)..."