package main

import (
	"fmt"

	"github.com/grafana/grafana-foundation-sdk/go/dashboard"
)

// PrometheusTarget representa un target en Prometheus.
type PrometheusTarget struct {
	Expr   string `json:"expr"`
	RefID  string `json:"refId"`
	Legend string `json:"legendFormat,omitempty"`
}

// PrometheusPanel representa un panel de tipo timeseries o stat para Prometheus.
type PrometheusPanel struct {
	Type       string                   `json:"type"`
	Title      string                   `json:"title"`
	Datasource *dashboard.DataSourceRef `json:"datasource"`
	GridPos    map[string]int           `json:"gridPos,omitempty"`
	Targets    []PrometheusTarget       `json:"targets"`
	Options    map[string]any           `json:"options,omitempty"`
}

// NewPrometheusPanel crea un panel de tipo timeseries con Prometheus y leyenda como tabla debajo del gráfico.
func NewPrometheusPanel(title, expr string, datasource *dashboard.DataSourceRef, x, y, w, h int) PrometheusPanel {
	return PrometheusPanel{
		Type:       "timeseries",
		Title:      title,
		Datasource: datasource,
		GridPos: map[string]int{
			"x": x, "y": y, "w": w, "h": h,
		},
		Targets: []PrometheusTarget{
			{
				Expr:  expr,
				RefID: "A",
			},
		},
		Options: map[string]any{
			"legend": map[string]any{
				"displayMode": "table",  // leyenda como tabla
				"placement":   "bottom", // debajo del gráfico
				"showLegend":  true,
			},
		},
	}
}

func NewPrometheusTopErrorsBarChart(
	title string,
	datasource *dashboard.DataSourceRef,
	x, y, w, h int,
) PrometheusPanel {
	return PrometheusPanel{
		Type:       "barchart",
		Title:      title,
		Datasource: datasource,
		GridPos:    map[string]int{"x": x, "y": y, "w": w, "h": h},
		Targets: []PrometheusTarget{
			{
				Expr:   `topk(10, sum(rate(http_requests_total{app=~"$app", environment=~"$environment", http_status=~"4..|5.."}[5m])) by (endpoint, http_status))`,
				RefID:  "A",
				Legend: "{{endpoint}} - {{http_status}}",
			},
		},
		Options: map[string]any{
			"orientation": "vertical",
			"stacking":    "none",
			"showValue":   true,
			"tooltip":     map[string]any{"mode": "single"},
			"legend": map[string]any{
				"displayMode": "list",
				"placement":   "bottom",
				"showLegend":  true,
			},
			"yaxis": map[string]any{"format": "short", "min": 0},
			"xaxis": map[string]any{"show": true},
		},
	}
}

func NewLatencyPercentilesPanel(
	title, metric string,
	datasource *dashboard.DataSourceRef,
	x, y, w, h int,
) PrometheusPanel {
	return PrometheusPanel{
		Type:       "timeseries",
		Title:      title,
		Datasource: datasource,
		GridPos:    map[string]int{"x": x, "y": y, "w": w, "h": h},
		Targets: []PrometheusTarget{
			{
				Expr: fmt.Sprintf(`
histogram_quantile(0.5, sum(rate(%s_bucket{app=~"$app", environment=~"$environment"}[5m])) by (le, endpoint, method))
`, metric),
				RefID:  "A",
				Legend: "{{endpoint}} - {{method}} - p50",
			},
			{
				Expr: fmt.Sprintf(`
histogram_quantile(0.9, sum(rate(%s_bucket{app=~"$app", environment=~"$environment"}[5m])) by (le, endpoint, method))
`, metric),
				RefID:  "B",
				Legend: "{{endpoint}} - {{method}} - p90",
			},
			{
				Expr: fmt.Sprintf(`
histogram_quantile(0.99, sum(rate(%s_bucket{app=~"$app", environment=~"$environment"}[5m])) by (le, endpoint, method))
`, metric),
				RefID:  "C",
				Legend: "{{endpoint}} - {{method}} - p99",
			},
		},
		Options: map[string]any{
			"tooltip": map[string]any{"mode": "single"},
			"legend": map[string]any{
				"displayMode": "table",
				"placement":   "right",
				"showLegend":  true,
			},
		},
	}
}
