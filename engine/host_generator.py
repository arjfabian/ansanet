import yaml
import random
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
        yaml_files = self.blueprints_path.glob("*.yml")
        
        for blueprint_file in yaml_files:
            try:
                with open(blueprint_file, 'r') as f:
                    data = yaml.safe_load(f)
                    
                if not isinstance(data, dict):
                    continue
                
                if 'metadata' not in data or 'type' not in data['metadata']:
                    print(f"[!] Warning: {blueprint_file.name} missing 'metadata.type', skipping")
                    continue
                
                b_type = data['metadata']['type']
                if b_type not in self.catalog:
                    print(f"[!] Warning: {blueprint_file.name} has invalid type '{b_type}', skipping")
                    continue
                
                self.catalog[b_type].append(blueprint_file.name)
                
            except Exception as e:
                print(f"[!] Error parsing {blueprint_file.name}: {e}")
                continue

        total_blueprints = sum(len(b) for b in self.catalog.values())
        if total_blueprints == 0:
            raise RuntimeError(f"[X] CRITICAL: No valid blueprints found in {self.blueprints_path}")
        else:
            for host_type, blueprints in self.catalog.items():
                if not blueprints:
                    print(f"[!] WARNING: No blueprints found for type '{host_type}'")

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