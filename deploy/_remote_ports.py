import os
import sys
import paramiko

HOST = "157.173.101.159"
PORT = 24059
USER = "emg59"
PASSWORD = os.environ["VPS_PASSWORD"]


def run(ssh, cmd):
    print(f"$ {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    status = stdout.channel.recv_exit_status()
    if out:
        print(out)
    if err:
        print(err, file=sys.stderr)
    print(f"(exit {status})\n")


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=20)

    run(ssh, "ss -ltn | sort -t: -k2 -n")
    run(ssh, "id")

    ssh.close()


if __name__ == "__main__":
    main()
