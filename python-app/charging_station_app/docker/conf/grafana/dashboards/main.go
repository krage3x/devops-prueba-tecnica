package main

import (
	"encoding/json"
	"log"
	"os"

	"github.com/grafana/grafana-foundation-sdk/go/cog"
	"github.com/grafana/grafana-foundation-sdk/go/dashboard"
)

type VariableBuilder struct {
	variable dashboard.VariableModel
}

func (b *VariableBuilder) Build() (dashboard.VariableModel, error) {
	return b.variable, nil
}

func NewQueryVariable(name, label, query string, datasource *dashboard.DataSourceRef) *VariableBuilder {
	variable := dashboard.VariableModel{
		Type:       "query",
		Name:       name,
		Label:      &label,
		Datasource: datasource,
		Query:      &dashboard.StringOrMap{String: &query},
		Refresh:    cog.ToPtr(dashboard.VariableRefreshOnTimeRangeChanged),
		Sort:       cog.ToPtr(dashboard.VariableSortAlphabeticalAsc),
		Multi:      cog.ToPtr(true),
		IncludeAll: cog.ToPtr(true),
		AllValue:   cog.ToPtr(".*"),
	}
	return &VariableBuilder{variable: variable}
}

func main() {
	promRef := dashboard.DataSourceRef{
		Type: cog.ToPtr("Prometheus"),
		Uid:  cog.ToPtr("Prometheus"),
	}
	appVarBuilder := NewQueryVariable("app", "App", "label_values(up, app)", &promRef)
	environmentVar := NewQueryVariable("environment", "Environment", "label_values(up, environment)", &promRef)

	builder := dashboard.NewDashboardBuilder("FastAPI Dashboards").
		WithVariable(appVarBuilder).
		WithVariable(environmentVar)

	dashboardObj, err := builder.Build()
	if err != nil {
		log.Fatalf("failed to build dashboard: %v", err)
	}

	// Convert dashboard a map para poder inyectar panel Prometheus
	dbJSON, _ := json.Marshal(dashboardObj)
	var dashboardMap map[string]interface{}
	json.Unmarshal(dbJSON, &dashboardMap)

	// Primer panel
	panel := NewPrometheusPanel(
		"HTTP Requests",
		`sum(rate(http_requests_total{app=~"$app", environment=~"$environment"}[$__range])) by (endpoint, method)`,
		&promRef,
		0, 0, 24, 9,
	)
	totalRequestsBarGauge := NewPrometheusBarGaugePanel(
		"Total Requests",
		`sum(http_requests_total{app=~"$app", environment=~"$environment"}) by (endpoint, method, http_status)`,
		&promRef,
		0, 10, 12, 6,
	)
	latencyHistogramPanel := NewPrometheusHistogramPanel(
		"Request Latency Histogram",
		"http_request_duration_seconds",
		&promRef,
		0, 15, 24, 9,
	)

	// Segundo panel
	// Panel Table para totales por endpoint, method y code

	// Añadir ambos paneles
	if dashboardMap["panels"] == nil {
		dashboardMap["panels"] = []interface{}{panel, totalRequestsBarGauge, latencyHistogramPanel}
	} else {
		panels := dashboardMap["panels"].([]interface{})
		dashboardMap["panels"] = append(panels, panel, totalRequestsBarGauge, latencyHistogramPanel)
	}

	finalJSON, _ := json.MarshalIndent(dashboardMap, "", "  ")
	os.WriteFile("dashboard.json", finalJSON, 0644)
	log.Println("Dashboard JSON creado con paneles Prometheus listo para importar")
}
