import os
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "dev")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0-dev")

ZONAS = [
    {
        "nombre": "Oficinas",
        "ocupacion": "Ocupada",
        "iluminacion": 80,
        "estado": "Operativa"
    },
    {
        "nombre": "Sala de juntas",
        "ocupacion": "Desocupada",
        "iluminacion": 20,
        "estado": "Operativa"
    },
    {
        "nombre": "Almacén",
        "ocupacion": "Ocupada",
        "iluminacion": 100,
        "estado": "Operativa"
    },
    {
        "nombre": "Estacionamiento",
        "ocupacion": "Desocupado",
        "iluminacion": 40,
        "estado": "Mantenimiento"
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>DCS Simulator</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            margin: 0;
            padding: 30px;
        }

        .container {
            max-width: 1050px;
            margin: auto;
        }

        .header {
            background-color: #1f2937;
            color: white;
            padding: 25px;
            border-radius: 8px;
        }

        .cards {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .card {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            flex: 1;
            min-width: 180px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.10);
        }

        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
            background-color: white;
        }

        th, td {
            padding: 12px;
            border-bottom: 1px solid #dddddd;
            text-align: left;
        }

        th {
            background-color: #e5e7eb;
        }

        .online {
            color: green;
            font-weight: bold;
        }

        .environment {
            text-transform: uppercase;
            font-weight: bold;
        }

        .lighting-control {
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 260px;
        }

        .lighting-control input[type="range"] {
            width: 130px;
        }

        .lighting-value {
            display: inline-block;
            min-width: 42px;
            font-weight: bold;
        }

        .occupancy-control {
            display: flex;
            align-items: center;
            gap: 8px;
            min-width: 230px;
        }

        .occupancy-control select {
            padding: 7px;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            background-color: white;
        }

        .alerts-panel {
            margin-top: 25px;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.10);
        }

        .alerts-summary {
            font-weight: bold;
            margin-bottom: 12px;
        }

        .alert-item {
            margin-top: 10px;
            padding: 12px;
            border-radius: 6px;
            border-left: 5px solid #f59e0b;
            background-color: #fffbeb;
        }

        .alert-item.critical {
            border-left-color: #dc2626;
            background-color: #fef2f2;
        }

        .alert-item.warning {
            border-left-color: #f59e0b;
            background-color: #fffbeb;
        }

        .no-alerts {
            padding: 12px;
            border-radius: 6px;
            background-color: #dcfce7;
            color: #166534;
            font-weight: bold;
        }

        button {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 12px;
            cursor: pointer;
        }

        button:hover {
            background-color: #1d4ed8;
        }

        button:disabled {
            background-color: #9ca3af;
            cursor: not-allowed;
        }

        .message {
            display: none;
            margin-top: 20px;
            padding: 12px;
            border-radius: 6px;
            font-weight: bold;
        }

        .message.success {
            display: block;
            background-color: #dcfce7;
            color: #166534;
        }

        .message.error {
            display: block;
            background-color: #fee2e2;
            color: #991b1b;
        }

        .footer {
            margin-top: 20px;
            color: #555555;
            font-size: 14px;
        }
    </style>
</head>

<body>
    <div class="container">

        <div class="header">
            <h1>DCS Building Monitoring Simulator</h1>

            <p>
                Ambiente:
                <span class="environment">{{ environment }}</span>
            </p>

            <p>Versión: {{ version }}</p>
        </div>

        <div class="cards">
            <div class="card">
                <h3>Estado general</h3>
                <p class="online">Operativo</p>
            </div>

            <div class="card">
                <h3>Controladores</h3>
                <p>4 conectados</p>
            </div>

            <div class="card">
                <h3>Dispositivos</h3>
                <p>125 registrados</p>
            </div>

            <div class="card">
                <h3>Dispositivos offline</h3>
                <p>3 dispositivos</p>
            </div>
        </div>

        <h2>Zonas de iluminación</h2>

        <table>
            <thead>
                <tr>
                    <th>Zona</th>
                    <th>Ocupación</th>
                    <th>Iluminación</th>
                    <th>Estado</th>
                </tr>
            </thead>

            <tbody>
                {% for zona in zonas %}
                <tr>
                    <td>{{ zona.nombre }}</td>

                    <td>
                        <div class="occupancy-control">
                            <select id="occupancy-{{ loop.index }}">
                                <option
                                    value="Ocupada"
                                    {% if zona.ocupacion.lower().startswith("ocup") %}
                                    selected
                                    {% endif %}
                                >
                                    Ocupada
                                </option>

                                <option
                                    value="Desocupada"
                                    {% if zona.ocupacion.lower().startswith("desocup") %}
                                    selected
                                    {% endif %}
                                >
                                    Desocupada
                                </option>
                            </select>

                            <button
                                id="occupancy-button-{{ loop.index }}"
                                onclick='updateOccupancy(
                                    {{ zona.nombre | tojson }},
                                    "{{ loop.index }}"
                                )'
                            >
                                Cambiar
                            </button>
                        </div>
                    </td>

                    <td>
                        <div class="lighting-control">
                            <input
                                type="range"
                                min="0"
                                max="100"
                                value="{{ zona.iluminacion }}"
                                id="slider-{{ loop.index }}"
                                oninput="updateDisplayedValue(
                                    '{{ loop.index }}',
                                    this.value
                                )"
                            >

                            <span
                                class="lighting-value"
                                id="value-{{ loop.index }}"
                            >
                                {{ zona.iluminacion }}%
                            </span>

                            <button
                                id="button-{{ loop.index }}"
                                onclick='updateLighting(
                                    {{ zona.nombre | tojson }},
                                    "{{ loop.index }}"
                                )'
                            >
                                Actualizar
                            </button>
                        </div>
                    </td>

                    <td>{{ zona.estado }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div id="message" class="message"></div>

        <div class="alerts-panel">
            <h2>Alertas activas</h2>
            <div id="alerts-summary" class="alerts-summary">
                Consultando alertas...
            </div>
            <div id="alerts-list"></div>
        </div>

        <div class="footer">
            <p>
                Aplicación de demostración para prácticas de despliegue DevOps.
            </p>

            <p>
                Health check disponible en
                <strong>/health</strong>
            </p>

            <p>
                API de estado disponible en
                <strong>/api/status</strong>
            </p>

            <p>
                API de versión disponible en
                <strong>/api/version</strong>
            </p>

            <p>
                API de ocupación disponible en
                <strong>/api/zones/&lt;zona&gt;/occupancy</strong>
            </p>

            <p>
                API de alertas disponible en
                <strong>/api/alerts</strong>
            </p>
        </div>

    </div>

    <script>
        function updateDisplayedValue(index, value) {
            const valueElement = document.getElementById(
                `value-${index}`
            );

            valueElement.textContent = `${value}%`;
        }

        function showMessage(text, type) {
            const messageElement = document.getElementById("message");

            messageElement.textContent = text;
            messageElement.className = `message ${type}`;
        }

        async function updateOccupancy(zoneName, index) {
            const select = document.getElementById(
                `occupancy-${index}`
            );

            const button = document.getElementById(
                `occupancy-button-${index}`
            );

            button.disabled = true;
            button.textContent = "Actualizando...";

            try {
                const response = await fetch(
                    `/api/zones/${encodeURIComponent(zoneName)}/occupancy`,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            occupancy: select.value
                        })
                    }
                );

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.error || "No fue posible actualizar la ocupación"
                    );
                }

                showMessage(
                    `${data.zone} ahora está ${data.occupancy}`,
                    "success"
                );

                await loadAlerts();
            } catch (error) {
                showMessage(error.message, "error");
            } finally {
                button.disabled = false;
                button.textContent = "Cambiar";
            }
        }

        async function loadAlerts() {
            const summaryElement = document.getElementById(
                "alerts-summary"
            );

            const listElement = document.getElementById(
                "alerts-list"
            );

            summaryElement.textContent = "Consultando alertas...";
            listElement.innerHTML = "";

            try {
                const response = await fetch("/api/alerts");
                const data = await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.error || "No fue posible consultar las alertas"
                    );
                }

                summaryElement.textContent =
                    `Alertas activas: ${data.active_alerts}`;

                if (data.alerts.length === 0) {
                    listElement.innerHTML =
                        '<div class="no-alerts">No hay alertas activas.</div>';
                    return;
                }

                for (const alert of data.alerts) {
                    const alertElement = document.createElement("div");
                    alertElement.className =
                        `alert-item ${alert.severity}`;

                    alertElement.textContent =
                        `[${alert.severity.toUpperCase()}] ` +
                        `${alert.zone}: ${alert.message}`;

                    listElement.appendChild(alertElement);
                }
            } catch (error) {
                summaryElement.textContent =
                    "No fue posible cargar las alertas";
                listElement.innerHTML =
                    `<div class="alert-item critical">${error.message}</div>`;
            }
        }

        async function updateLighting(zoneName, index) {
            const slider = document.getElementById(
                `slider-${index}`
            );

            const button = document.getElementById(
                `button-${index}`
            );

            const lighting = Number(slider.value);

            button.disabled = true;
            button.textContent = "Actualizando...";

            try {
                const response = await fetch(
                    `/api/zones/${encodeURIComponent(zoneName)}/lighting`,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            lighting: lighting
                        })
                    }
                );

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.error || "No fue posible actualizar la zona"
                    );
                }

                showMessage(
                    `${data.zone} actualizada a ${data.lighting}%`,
                    "success"
                );

                await loadAlerts();
            } catch (error) {
                showMessage(error.message, "error");
            } finally {
                button.disabled = false;
                button.textContent = "Actualizar";
            }
        }

        document.addEventListener("DOMContentLoaded", loadAlerts);
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(
        HTML_TEMPLATE,
        environment=APP_ENV,
        version=APP_VERSION,
        zonas=ZONAS
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "environment": APP_ENV,
        "version": APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


@app.route("/api/status")
def api_status():
    return jsonify({
        "application": "DCS Building Monitoring Simulator",
        "environment": APP_ENV,
        "version": APP_VERSION,
        "system_status": "operational",
        "controllers_online": 4,
        "devices_total": 125,
        "devices_offline": 3,
        "zones": ZONAS
    }), 200


@app.route("/api/version")
def api_version():
    return jsonify({
        "application": "DCS Building Monitoring Simulator",
        "environment": APP_ENV,
        "version": APP_VERSION
    }), 200


@app.route(
    "/api/zones/<string:zone_name>/lighting",
    methods=["PUT"]
)
def update_zone_lighting(zone_name):
    data = request.get_json(silent=True)

    if not data or "lighting" not in data:
        return jsonify({
            "error": "El campo lighting es obligatorio"
        }), 400

    try:
        lighting = int(data["lighting"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "La iluminación debe ser un número entero"
        }), 400

    if lighting < 0 or lighting > 100:
        return jsonify({
            "error": "La iluminación debe estar entre 0 y 100"
        }), 400

    zone = next(
        (
            zone
            for zone in ZONAS
            if zone["nombre"].lower() == zone_name.lower()
        ),
        None
    )

    if zone is None:
        return jsonify({
            "error": "Zona no encontrada"
        }), 404

    zone["iluminacion"] = lighting

    return jsonify({
        "message": "Nivel de iluminación actualizado",
        "zone": zone["nombre"],
        "lighting": zone["iluminacion"],
        "environment": APP_ENV,
        "version": APP_VERSION
    }), 200


@app.route(
    "/api/zones/<string:zone_name>/occupancy",
    methods=["PUT"]
)
def update_zone_occupancy(zone_name):
    data = request.get_json(silent=True)

    if not data or "occupancy" not in data:
        return jsonify({
            "error": "El campo occupancy es obligatorio"
        }), 400

    occupancy = str(data["occupancy"]).strip().lower()

    valid_values = {
        "ocupada": "Ocupada",
        "ocupado": "Ocupada",
        "desocupada": "Desocupada",
        "desocupado": "Desocupada"
    }

    if occupancy not in valid_values:
        return jsonify({
            "error": "La ocupación debe ser Ocupada o Desocupada"
        }), 400

    zone = next(
        (
            zone
            for zone in ZONAS
            if zone["nombre"].lower() == zone_name.lower()
        ),
        None
    )

    if zone is None:
        return jsonify({
            "error": "Zona no encontrada"
        }), 404

    zone["ocupacion"] = valid_values[occupancy]

    return jsonify({
        "message": "Ocupación actualizada",
        "zone": zone["nombre"],
        "occupancy": zone["ocupacion"],
        "environment": APP_ENV,
        "version": APP_VERSION
    }), 200


@app.route("/api/alerts")
def get_active_alerts():
    alerts = []

    for index, zone in enumerate(ZONAS, start=1):
        zone_name = zone["nombre"]
        occupancy = zone["ocupacion"].lower()
        lighting = zone["iluminacion"]
        status = zone["estado"].lower()

        if status == "mantenimiento":
            alerts.append({
                "id": f"STATUS-{index}",
                "severity": "warning",
                "zone": zone_name,
                "type": "maintenance",
                "message": "La zona se encuentra en mantenimiento"
            })

        if status == "fuera de servicio":
            alerts.append({
                "id": f"STATUS-{index}",
                "severity": "critical",
                "zone": zone_name,
                "type": "service_failure",
                "message": "La zona se encuentra fuera de servicio"
            })

        if occupancy.startswith("desocup") and lighting > 50:
            alerts.append({
                "id": f"ENERGY-{index}",
                "severity": "warning",
                "zone": zone_name,
                "type": "energy_waste",
                "message": (
                    "La zona está desocupada y mantiene "
                    f"la iluminación en {lighting}%"
                )
            })

        if occupancy.startswith("ocup") and lighting < 20:
            alerts.append({
                "id": f"LIGHT-{index}",
                "severity": "warning",
                "zone": zone_name,
                "type": "low_lighting",
                "message": (
                    "La zona está ocupada y tiene un nivel "
                    f"de iluminación bajo: {lighting}%"
                )
            })

    return jsonify({
        "application": "DCS Building Monitoring Simulator",
        "environment": APP_ENV,
        "version": APP_VERSION,
        "active_alerts": len(alerts),
        "alerts": alerts,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )