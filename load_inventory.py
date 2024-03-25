import ansible_runner

# Commands
env_var = {'ANSIBLE_CONFIG': './ansible.cfg'}
docker_compose = 'docker compose up -d'
list_hosts = 'ansible all:localhost --list-hosts'
ping = 'ansible all:localhost -m ping'

# Execute docker compose
ansible_runner.run_command(envvars=env_var, executable_cmd=docker_compose)

# List hosts
ansible_runner.run_command(envvars=env_var, executable_cmd=list_hosts)

# Load inventory file
out, err = ansible_runner.get_inventory(action='list', inventories=['./hosts.yml'], response_format='json', envvars=env_var)

# Print names, IP addresses, and group names of all hosts
for host, host_info in out["_meta"]["hostvars"].items():
    hostname = host
    ip = host_info["ansible_host"]
    groups = list(out.keys())[2:]
    group_names = [group for group, group_info in out.items() if "hosts" in group_info and hostname in group_info["hosts"]]
    print(f"\nHostname: {hostname.ljust(25)} IP Address: {ip.ljust(15)} Groups: {', '.join(group_names)}")

# Output ping results
ansible_runner.run_command(envvars=env_var, executable_cmd=ping)
