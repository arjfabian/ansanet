import os
import requests
import socket
import json
import signal
import sys
from pathlib import Path
from dotenv import load_dotenv
from engine.network_generator import NetworkGenerator

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

class AnsaNetApp:
    def __init__(self):
        self.bot_name = "ANSANET Alert System"
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.gen = NetworkGenerator()
        self.map_file = BASE_DIR / "engine" / "network_map.json"
        # TODO: Change generic name to have several network configs, e.g.
        # network_map_a48f4a.json
        
        # Capture signal for graceful exit
        signal.signal(signal.SIGINT, self.handle_exit_signal)

    def send_notification(self, message):
        if not self.token or not self.chat_id:
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        full_message = f"🤖 *{self.bot_name}*\n{message}"
        payload = {"chat_id": self.chat_id, "text": full_message, "parse_mode": "Markdown"}
        try:
            requests.post(url, json=payload, timeout=5)
        except:
            pass

    def send_farewell(self):
        """Reusable termiation message"""
        farewell_msg = (
            "🏁 *SIMULATION TERMINATED*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "👋 Thanks for playing ANSANET!\n"
            "📊 Session ended successfully.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        self.send_notification(farewell_msg)

    def handle_exit_signal(self, sig, frame):
        # Calls sys.exit only.
        # The 'finally' block in run_server will take care of the rest
        sys.exit(0)

    def run_server(self, host='127.0.0.1', port=9999):
        try:
            # 1. Generate the Network
            nodes = self.gen.generate_full_network()
            result = self.gen.save(nodes)
            
            meta = result['network_metadata']
            welcome_report = (
                f"✅ *Deployment Successful*\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🆔 *ID:* `{meta['id']}`\n"
                f"📊 *Asset Inventory:* {meta['total_nodes']} hosts\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🎮 *Status:* Listening on {host}:{port}..."
            )
            self.send_notification(welcome_report)
            print(f"[*] Server live on {host}:{port}. Press CTRL+C to stop.")

            # 2. Socket Listener
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((host, port))
                s.listen()
                
                while True:
                    conn, addr = s.accept()
                    with conn:
                        self.send_notification(f"⚠️ *INTRUSION DETECTED*\nNew connection from: `{addr[0]}:{addr[1]}`")
                        
                        if self.map_file.exists():
                            with open(self.map_file, "r") as f:
                                map_data = f.read()
                            conn.sendall(map_data.encode('utf-8'))
                            print(f"[!] Data sent to {addr}")
                        else:
                            print(f"[X] Error: {self.map_file} not found during sync.")
        
        except Exception as e:
            print(f"[X] Critical Server Error: {e}")
            # Optional: Notify critical error via Telegram
            self.send_notification(f"❌ *CRITICAL ERROR*: `{e}`")
        
        finally:
            self.send_farewell()
            print("[!] ANSANET Shutdown complete.")

if __name__ == "__main__":
    app = AnsaNetApp()
    app.run_server()