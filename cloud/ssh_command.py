import paramiko

def run_ssh_command(host, username, key_path, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, key_filename=key_path)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        client.close()
        return {"host": host, "status": "success", "output": output}
    except Exception as e:
        return {"host": host, "status": "error", "error": str(e)}
