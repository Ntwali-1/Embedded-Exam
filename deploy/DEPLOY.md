# VPS Deployment Guide

Deploy the temperature dashboard to your exam VPS.

## VPS connection details

| Setting | Value |
|---------|-------|
| Host | `157.173.101.159` |
| SSH user | `emg59` |
| SSH port | `24059` |
| Dashboard URL | **http://157.173.101.159:8059** |

### Connect manually

```bash
ssh -p 24059 emg59@157.173.101.159
```

Enter your VPS password when prompted.

---

## Option A — One-command deploy from Windows (recommended)

Open PowerShell in the project folder:

```powershell
cd C:\Users\mfura\Documents\learning\embedded-exam
powershell -ExecutionPolicy Bypass -File deploy\upload-and-deploy.ps1
```

You will be asked for your SSH password **twice** (upload + setup).

When done, open: **http://157.173.101.159:8059**

---

## Option B — Manual step-by-step

### Step 1: Connect to VPS

```bash
ssh -p 24059 emg59@157.173.101.159
```

### Step 2: On your PC — upload dashboard (new terminal)

```powershell
cd C:\Users\mfura\Documents\learning\embedded-exam
scp -P 24059 -r dashboard emg59@157.173.101.159:~/
scp -P 24059 deploy/vps-setup.sh emg59@157.173.101.159:~/
```

### Step 3: Back on VPS — install and start

```bash
chmod +x ~/vps-setup.sh
bash ~/vps-setup.sh
```

### Step 4: Verify

```bash
curl http://127.0.0.1:8059/api/data
```

You should see JSON with your name and topic.

---

## Run the full system (exam demo)

1. **VPS** — dashboard running (link above)
2. **PC** — Arduino connected, Serial Monitor **closed**
3. **PC** — run:

```powershell
py pc\mqtt_client.py
```

4. **Browser** — open http://157.173.101.159:8059 — temperature updates live

---

## Useful VPS commands

```bash
# View dashboard logs
tail -f ~/embedded-exam-dashboard/dashboard.log

# Restart dashboard
pkill -f "python3 app.py"
cd ~/embedded-exam-dashboard && nohup python3 app.py > dashboard.log 2>&1 &

# Check if dashboard is running
curl http://127.0.0.1:8059/api/data
```

---

## If dashboard link does not open in browser

Port 8059 may be blocked. On VPS try:

```bash
sudo ufw allow 8059/tcp
sudo ufw status
```

Or ask your instructor if port 8059 is allowed on the VPS firewall.

---

## What to submit

| Item | Value |
|------|-------|
| GitHub repo | (you push yourself) |
| Dashboard link | **http://157.173.101.159:8059** |
| MQTT topic | `sensor_rutaganira_yanis_ntwali` |
| MQTT broker | `broker.benax.rw` |
