import os
import sys
import paramiko
from scp import SCPClient

HOST = "157.173.101.159"
PORT = 24059
USER = "emg59"
PASSWORD = os.environ["VPS_PASSWORD"]

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_DIR = os.path.join(PROJECT_ROOT, "dashboard")
SETUP_SCRIPT = os.path.join(PROJECT_ROOT, "deploy", "vps-setup.sh")


def run(ssh, cmd):
    print(f"$ {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    exit_status = stdout.channel.recv_exit_status()
    if out:
        print(out)
    if err:
        print(err, file=sys.stderr)
    return exit_status


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=20)

    print("==> Removing stale ~/dashboard on VPS ...")
    run(ssh, "rm -rf ~/dashboard")

    print("==> Connected. Uploading dashboard/ ...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(DASHBOARD_DIR, recursive=True, remote_path="dashboard")
        scp.put(SETUP_SCRIPT, remote_path="vps-setup.sh")

    print("==> Upload complete. Running setup script on VPS ...")
    status = run(ssh, "chmod +x ~/vps-setup.sh && cd ~ && bash vps-setup.sh")

    ssh.close()
    sys.exit(status)


if __name__ == "__main__":
    main()
