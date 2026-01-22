import yaml
import random
import json
from pathlib import Path

from engine.host_generator import HostGenerator 

BASE_DIR = Path(__file__).resolve().parent
PATH_NETWORK_PARAMETERS_YAML = BASE_DIR / "parameters" / "network.yml"

class NetworkGenerator:
    def __init__(self, config_path=PATH_NETWORK_PARAMETERS_YAML):
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)['network']
                self.rules = self.config['generation_rules']
        except FileNotFoundError:
            print(f"[X] Error: Configuration file not found at {config_path}")
            raise

    def _validate_rules(self):
        assert self.rules['host_types']['servers_min'] <= self.rules['host_types']['servers_max']
        assert self.rules['host_types']['infra_min'] < self.rules['host_types']['infra_max']
        assert (self.rules['host_types']['servers_max'] + 
                self.rules['host_types']['infra_max']) < self.rules['hosts_min']

    def _generate_hostname(self, node_type, idx):
        prefixes = {"server": "SERV", "infra": "INFR", "workstation": "WKST"}
        depts = ["FIN", "HR", "ENG", "IT", "SALES"]
        return f"{prefixes[node_type]}-{random.choice(depts)}-{idx:02d}"

    def generate_full_network(self):
        """Generate a topology and return each host with random unique IPs."""
        self._validate_rules()
        nodes = []
        host_gen = HostGenerator()
        
        total_hosts = random.randint(self.rules['hosts_min'], self.rules['hosts_max'])
        
        """IP ASSIGNMENT LOGIC"""
        # For a simple random IP assignment, we take the whole 2-254 range and
        # shuffle it. The next random IP will be retrieved using pop().
        # TODO: In future versions, calculate valid IP ranges according to the
        # parameters in parameters/network.yml.
        ip_pool = [str(i) for i in range(2, 255)]
        random.shuffle(ip_pool)

        num_servers = random.randint(self.rules['host_types']['servers_min'], self.rules['host_types']['servers_max'])
        num_infra = random.randint(self.rules['host_types']['infra_min'], self.rules['host_types']['infra_max'])
        num_workstations = total_hosts - (num_servers + num_infra)

        assignment_pool = (['server'] * num_servers + ['infra'] * num_infra + ['workstation'] * num_workstations)
        random.shuffle(assignment_pool)

        for idx, node_type in enumerate(assignment_pool, start=1):
            host_octet = ip_pool.pop()
            
            base_node = {
                "id": f"node-{idx}",
                "ip": f"{self.config['base_ip']}.{host_octet}",
                "hostname": self._generate_hostname(node_type, idx),
                "type": node_type,
                "status": "online"
            }
            
            host_details = host_gen.generate_host(node_type)
            full_node = {**base_node, **host_details}
            nodes.append(full_node)
            
        return nodes

    def save(self, nodes):
        output_file = BASE_DIR / "network_map.json"
        
        # In order to sort by IP, we must convert each each one to int using
        # split(). (e.g. "192.168.1.17" becomes ['192', '168', '1', '17'])
        nodes.sort(key=lambda x: [int(octet) for octet in x['ip'].split('.')])

        output = {
            "network_metadata": {
                "id": self.config['id'],
                "domain": self.config['domain'],
                "total_nodes": len(nodes),
                "generated_at": str(Path(__file__).stat().st_mtime)
            },
            "nodes": nodes
        }
        with open(output_file, "w") as f:
            json.dump(output, f, indent=4)
        return output

if __name__ == "__main__":
    gen = NetworkGenerator()
    try:
        # Generate the full network
        network_nodes = gen.generate_full_network()
        result = gen.save(network_nodes)
        
        # Display a summary of the generated network
        print(f"\n[!] NETWORK GENERATED: {result['network_metadata']['id']}")
        print(f"[!] TOTAL HOSTS: {result['network_metadata']['total_nodes']}")
        print("-" * 85)
        print(f"{'HOSTNAME':<15} | {'IP':<15} | {'TYPE':<12} | {'BLUEPRINT':<25}")
        print("-" * 85)
        for node in result['nodes']:
            print(f"{node['hostname']:<15} | {node['ip']:<15} | {node['type']:<12} | {node['blueprint_orig']:<25}")
        print("-" * 85)
        print(f"[+] Full state saved to: network_map.json")
        
    except Exception as e:
        print(f"[X] Error during generation: {e}")