import yaml
import random
import glob
from pathlib import Path

# Path to the blueprints
BASE_DIR = Path(__file__).resolve().parent
BLUEPRINTS_PATH = BASE_DIR / "blueprints"

# Valid host types (hardcoded for now)
valid_host_types = [
    "server",
    "infra",
    "workstation"
]

# Fallback in case a blueprint is unavailable or invalid
fallback_blueprint = {
    "blueprint_orig": "generic-fallback.yml",
    "os_name": "Unknown OS",
    "emulated_services": [{"port": 0, "name": "icmp/ping"}],
    "file_tree": {"/": ["README.txt"]}
}

class HostGenerator:
    def __init__(self, blueprints_path=BLUEPRINTS_PATH):
        self.blueprints_path = blueprints_path
        self.catalog = { host_type: [] for host_type in valid_host_types}
        self._index_blueprints()

    def _index_blueprints(self):
        yaml_files = glob.glob(str(self.blueprints_path / "*.yml"))
        for file_path in yaml_files:
            try:
                with open(file_path, 'r') as f:
                    data = yaml.safe_load(f)
                    # SKIP THE FILE if it's empty or not a valid dictionary
                    if not isinstance(data, dict):
                        continue
                    
                    b_type = data.get('metadata', {}).get('type')
                    if b_type in self.catalog:
                        self.catalog[b_type].append(Path(file_path).name)
            except Exception:
                # SKIP THE FILE in case of parsing errors
                continue

    def generate_host(self, node_type):
        """Selects a blueprint and returns the host's initial structure."""
        available = self.catalog.get(node_type, [])
        
        # Return the fallback blueprint
        if not available:
            return fallback_blueprint
        
        selected_blueprint_name = random.choice(available)
        blueprint_file = self.blueprints_path / selected_blueprint_name
        
        with open(blueprint_file, 'r') as f:
            blueprint_data = yaml.safe_load(f)
            
        # Return JSON with the blueprint structure (simulating the "filling")
        return {
            "blueprint_orig": selected_blueprint_name,
            "os_name": blueprint_data.get('metadata', {}).get('name'),
            "emulated_services": blueprint_data.get('emulation', {}).get('services', []),
            "file_tree": blueprint_data.get('emulation', {}).get('file_tree', {})
        }

if __name__ == "__main__":
    # --- STANDALONE TEST ---
    print(f"[*] Initializing HostGenerator at {BLUEPRINTS_PATH}")
    hg = HostGenerator()
    
    # Test generation for each type
    for t in valid_host_types:
        print(f"\n[+] Testing generation for type: {t}")
        host_data = hg.generate_host(t)
        import json
        print(json.dumps(host_data, indent=4))