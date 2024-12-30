#!/usr/bin/env python3
import json
import subprocess

def get_docker_hosts():
    result = subprocess.run(["docker", "ps", "--format", "{{.ID}} {{.Names}} {{.Ports}}"], stdout=subprocess.PIPE)
    hosts = {}
    for line in result.stdout.decode().splitlines():
        container_id, name, ports = line.split(maxsplit=2)
        ssh_port = ports.split("->")[0].split(":")[-1]
        hosts[name] = {
            "ansible_host": "127.0.0.1",
            "ansible_port": ssh_port,
            "ansible_user": "root"
        }
    return hosts

def generate_inventory():
    hosts = get_docker_hosts()
    inventory = {
        "all": {
            "hosts": list(hosts.keys())
        },
        "_meta": {
            "hostvars": hosts
        }
    }
    return inventory

def main():
    print(json.dumps(generate_inventory()))

if __name__ == "__main__":
    main()

