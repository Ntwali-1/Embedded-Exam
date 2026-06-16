import base64
import os
import paramiko

HOST = "157.173.101.159"
PORT = 24059
USER = "emg59"
PASSWORD = os.environ["VPS_PASSWORD"]

TEST_SCRIPT = (
    "import socket\n"
    "s = socket.socket()\n"
    "try:\n"
    "    s.bind(('0.0.0.0', 24059))\n"
    "    print('BIND_OK')\n"
    "except OSError as e:\n"
    "    print('BIND_FAILED:', e)\n"
)


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=20)

    encoded = base64.b64encode(TEST_SCRIPT.encode()).decode()
    cmd = f"echo {encoded} | base64 -d | python3"
    _, out, err = ssh.exec_command(cmd)
    print(out.read().decode())
    print(err.read().decode())
    ssh.close()


if __name__ == "__main__":
    main()
