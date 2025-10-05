WORKDIR ?= .

.PHONY: all postgres redis app clean

all: postgres redis app

postgres:
	@echo "Levantando Postgres desde $(WORKDIR)/charts/postgres..."
	helm install postgres $(WORKDIR)/postgres -n infra --create-namespace -f $(WORKDIR)/postgres/values.yml

redis:
	@echo "Levantando Redis desde $(WORKDIR)/charts/redis..."
	helm install redis $(WORKDIR)/redis -n infra -f $(WORKDIR)/redis/values.yml

app:
	@echo "Levantando app desde $(WORKDIR)/charts/app..."
	helm install charging-station-app $(WORKDIR)/charging-station-app -n core --create-namespace -f $(WORKDIR)/charging-station-app/values.yml

clean:
	@echo "Limpiando recursos..."
	helm uninstall charging-station-app -n core || true
	helm uninstall redis -n infra || true
	helm uninstall postgres -n infra || true