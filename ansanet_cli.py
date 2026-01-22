import socket
import json
import sys

class AnsaNetCLI:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.world = None
        self.current_session_ip = "localhost"

    def connect(self):
        """Conecta ao servidor e sincroniza o estado da rede."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(f"[*] Establishing connection to ANSANET Core at {self.host}:{self.port}...")
                s.connect((self.host, self.port))
                
                # Recebe o JSON do mapa da rede
                # Usamos um buffer maior para garantir que o mapa completo seja recebido
                data = s.recv(65536) 
                if not data:
                    print("[X] Failed to receive network data.")
                    sys.exit(1)
                
                self.world = json.loads(data.decode())
                print(f"[+] Synced: {self.world['network_metadata']['id']} [STATUS: ACTIVE]")
        except ConnectionRefusedError:
            print("[X] Connection Refused: Is the ANSANET Server running?")
            sys.exit(1)
        except Exception as e:
            print(f"[X] Connection Error: {e}")
            sys.exit(1)

    def do_scan(self):
        """Simula um ping sweep na rede atual."""
        print(f"\nScanning network: {self.world['network_metadata']['domain']}")
        print("-" * 40)
        for node in self.world['nodes']:
            print(f"HOST: {node['ip']:<15} | STATUS: [UP] | OS: {node['os_name']}")
        print("-" * 40)

    def do_nmap(self, target_ip):
        """Simula a execução do Nmap em um host alvo."""
        target = next((n for n in self.world['nodes'] if n['ip'] == target_ip), None)
        
        if target:
            print(f"\nStarting Nmap 7.92 simulation at {target_ip}")
            print(f"Scanning {target['hostname']}...")
            print(f"PORT     STATE  SERVICE")
            for svc in target['emulated_services']:
                print(f"{svc['port']}/tcp  open   {svc['name']}")
            print("\nNmap done: 1 IP address (1 host up) scanned.")
        else:
            print(f"Note: Host {target_ip} does not respond to probes.")

    def run(self):
        self.connect()
        print("\nWelcome to the Interaction Layer. Type 'help' for commands.")
        
        while True:
            try:
                cmd_line = input(f"ansanet@{self.current_session_ip}$ ").strip().split()
                if not cmd_line: continue
                
                cmd = cmd_line[0].lower()
                args = cmd_line[1:]

                if cmd in ["exit", "quit"]:
                    print("Disconnecting from simulation...")
                    break
                elif cmd == "help":
                    print("\nCommands:\n - scan: List all active hosts\n - nmap <ip>: Scan host services\n - exit: Close connection\n")
                elif cmd == "scan":
                    self.do_scan()
                elif cmd == "nmap":
                    if args:
                        self.do_nmap(args[0])
                    else:
                        print("Usage: nmap <ip>")
                else:
                    print(f"sh: {cmd}: command not found")
            except KeyboardInterrupt:
                print("\nUse 'exit' to disconnect properly.")

if __name__ == "__main__":
    cli = AnsaNetCLI()
    cli.run()