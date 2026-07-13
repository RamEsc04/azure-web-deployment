import os
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string

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
            max-width: 950px;
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
                    <td>{{ zona.iluminacion }}%</td>
                    <td>{{ zona.estado }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="footer">
            <p>Aplicación de demostración para prácticas de despliegue DevOps.</p>
            <p>Health check disponible en <strong>/health</strong></p>
            <p>API de estado disponible en <strong>/api/status</strong></p>
        </div>

    </div>
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


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )