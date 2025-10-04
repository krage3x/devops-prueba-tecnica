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

	dbJSON, _ := json.Marshal(dashboardObj)
	var dashboardMap map[string]interface{}
	json.Unmarshal(dbJSON, &dashboardMap)

	httpRequestsPanel := NewPrometheusPanel(
		"HTTP Requests",
		`sum(rate(http_requests_total{app=~"$app", environment=~"$environment"}[$__range])) by (endpoint, method)`,
		&promRef,
		0, 0, 24, 9,
	)

	latencyPercentiles := NewLatencyPercentilesPanel(
		"Percentiles per endpoints",
		"http_request_duration_seconds",
		&promRef,
		12, 22, 12, 8,
	)
	errorsTimeSeries := NewPrometheusPanel(
		"Requests per error code",
		`sum(rate(http_requests_total{app=~"$app", environment=~"$environment", http_status=~"4..|5.."}[5m])) by (http_status)`,
		&promRef,
		0, 12, 24, 6,
	)
	errorsTimeSeries.Options = map[string]any{
		"legend": map[string]any{
			"displayMode": "list",
			"placement":   "bottom",
			"showLegend":  true,
		},
		"tooltip": map[string]any{
			"mode": "all",
		},
		"stacking": map[string]any{
			"mode": "normal",
		},
		"fieldConfig": map[string]any{
			"defaults": map[string]any{
				"unit": "short",
			},
		},
	}

	topErrorsBarChart := NewPrometheusTopErrorsBarChart(
		"Top 10 Endpoints with errors",
		&promRef,
		0, 18, 24, 6,
	)

	panels := []interface{}{
		httpRequestsPanel,
		latencyPercentiles,
		errorsTimeSeries,
		topErrorsBarChart,
	}

	if dashboardMap["panels"] == nil {
		dashboardMap["panels"] = panels
	} else {
		existing := dashboardMap["panels"].([]interface{})
		dashboardMap["panels"] = append(existing, panels...)
	}

	finalJSON, _ := json.MarshalIndent(dashboardMap, "", "  ")
	os.WriteFile("dashboard.json", finalJSON, 0644)
	log.Println("Dashboard JSON actualizado con paneles de errores y latencias listo para importar")
}
