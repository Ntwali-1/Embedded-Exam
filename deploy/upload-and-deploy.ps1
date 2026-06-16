# Upload dashboard to VPS and run setup (you will be asked for SSH password twice)

$VPS_USER = "emg59"
$VPS_HOST = "157.173.101.159"
$VPS_PORT = "24059"
$PROJECT_ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "Uploading dashboard to VPS..." -ForegroundColor Cyan
scp -P $VPS_PORT -r "$PROJECT_ROOT\dashboard" "${VPS_USER}@${VPS_HOST}:~/"
scp -P $VPS_PORT "$PROJECT_ROOT\deploy\vps-setup.sh" "${VPS_USER}@${VPS_HOST}:~/"

Write-Host "`nRunning setup on VPS..." -ForegroundColor Cyan
ssh -p $VPS_PORT "${VPS_USER}@${VPS_HOST}" "chmod +x ~/vps-setup.sh && cd ~ && bash vps-setup.sh"

Write-Host "`nDone! Open in browser:" -ForegroundColor Green
Write-Host "  http://157.173.101.159:8059" -ForegroundColor Yellow
Write-Host "`nThen on your PC run: py pc\mqtt_client.py" -ForegroundColor Cyan
