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
func NewPrometheusHistogramPanel(title string, metric string, datasource *dashboard.DataSourceRef, x, y, w, h int) PrometheusPanel {
	return PrometheusPanel{
		Type:       "timeseries",
		Title:      title,
		Datasource: datasource,
		GridPos:    map[string]int{"x": x, "y": y, "w": w, "h": h},
		Targets: []PrometheusTarget{
			{
				Expr:   fmt.Sprintf(`rate(%s_bucket{app=~"$app", environment=~"$environment"}[5m])`, metric),
				RefID:  "A",
				Legend: "{{le}} {{method}} {{endpoint}}",
			},
		},
		Options: map[string]any{
			"tooltip": map[string]any{
				"mode": "single",
			},
			"legend": map[string]any{
				"displayMode": "list",
				"placement":   "bottom",
				"showLegend":  true,
			},
		},
	}
}
func NewPrometheusBarGaugePanel(title, expr string, datasource *dashboard.DataSourceRef, x, y, w, h int) PrometheusPanel {
	return PrometheusPanel{
		Type:       "bargauge",
		Title:      title,
		Datasource: datasource,
		GridPos:    map[string]int{"x": x, "y": y, "w": w, "h": h},
		Targets: []PrometheusTarget{
			{
				Expr:   expr,
				RefID:  "A",
				Legend: "{{endpoint}} {{method}} {{http_status}}", // aquí ponemos leyenda legible
			},
		},
		Options: map[string]any{
			"displayMode":  "lcd",
			"orientation":  "horizontal",
			"showUnfilled": true,
			"min":          0,
			"max":          100,
			"thresholds": map[string]any{
				"mode": "absolute",
				"steps": []any{
					map[string]any{"color": "green", "value": 0},
					map[string]any{"color": "yellow", "value": 50},
					map[string]any{"color": "red", "value": 80},
				},
			},
		},
	}
}
