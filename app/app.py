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
                    <td>{{ zona.ocupacion }}</td>

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
            } catch (error) {
                showMessage(error.message, "error");
            } finally {
                button.disabled = false;
                button.textContent = "Actualizar";
            }
        }
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


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )