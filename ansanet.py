import os
import requests
from dotenv import load_dotenv
from engine.network_generator import NetworkGenerator

# Load environment variables from .env
load_dotenv()

class AnsaNetApp:
    def __init__(self):
        self.bot_name = "ANSANET Alert System"
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.gen = NetworkGenerator()

    def send_notification(self, message):
        """Sends notifications via Telegram Bot API with a professional identity."""
        if not self.token or not self.chat_id:
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        # Adicionamos o nome do sistema no cabeçalho da mensagem
        full_message = f"🤖 *{self.bot_name}*\n{message}"
        
        payload = {
            "chat_id": self.chat_id, 
            "text": full_message, 
            "parse_mode": "Markdown"
        }
        
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"[X] Telegram Alert Failed: {e}")

    def run(self):
        print(f"[*] Starting {self.bot_name}...")
        
        # 1. Generate the procedural network
        nodes = self.gen.generate_full_network()
        result = self.gen.save(nodes)
        
        # 2. Extract stats for the alert
        meta = result['network_metadata']
        srv_count = sum(1 for n in nodes if n['type'] == 'server')
        wks_count = sum(1 for n in nodes if n['type'] == 'workstation')
        inf_count = sum(1 for n in nodes if n['type'] == 'infra')

        # 3. Create the executive summary for Telegram
        status_report = (
            f"✅ *Deployment Successful*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *ID:* `{meta['id']}`\n"
            f"🌐 *Domain:* `{meta['domain']}`\n"
            f"📊 *Asset Inventory:* {meta['total_nodes']} hosts\n\n"
            f"   • Servers: {srv_count}\n"
            f"   • Workstations: {wks_count}\n"
            f"   • Infrastructure: {inf_count}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🎮 *Status:* Simulation ready. Waiting for events..."
        )

        # 4. Finalize
        print(f"[+] Network {meta['id']} deployed and indexed.")
        self.send_notification(status_report)

if __name__ == "__main__":
    app = AnsaNetApp()
    app.run()