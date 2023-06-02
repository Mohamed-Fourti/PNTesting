import json
import paramiko


def create_ssh_session():
    with open('login_credentials.json', 'r') as f:
        data = json.load(f)
    username = data['username']
    keyfile = data['keyfile']
    ip_address = data['ip_address']
    ssh_key = paramiko.RSAKey.from_private_key_file(keyfile)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip_address, username=username, pkey=ssh_key)
    return ssh
