#!/bin/bash
# Run on VPS after upload. Usage: bash ~/vps-setup.sh

set -e

SOURCE_DIR="$HOME/dashboard"
APP_DIR="$HOME/embedded-exam-dashboard"
PORT=8059

if [ ! -f "$SOURCE_DIR/app.py" ]; then
  echo "ERROR: $SOURCE_DIR/app.py not found."
  echo "Upload first: scp -P 24059 -r dashboard emg59@157.173.101.159:~/"
  exit 1
fi

echo "==> Installing to $APP_DIR"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR"
cp -r "$SOURCE_DIR"/* "$APP_DIR/"

cd "$APP_DIR"

echo "==> Installing Python packages..."
python3 -m pip install --user -r requirements.txt

echo "==> Stopping old dashboard..."
pkill -f "$APP_DIR/app.py" 2>/dev/null || pkill -f "python3 app.py" 2>/dev/null || true
sleep 1

echo "==> Starting dashboard on port $PORT..."
nohup python3 app.py > dashboard.log 2>&1 &
sleep 3

echo ""
if curl -sf "http://127.0.0.1:$PORT/api/data" > /dev/null; then
  echo "SUCCESS — Dashboard is live!"
else
  echo "Setup finished — check logs if page does not load:"
  echo "  tail -f $APP_DIR/dashboard.log"
fi

echo ""
echo "Submit this link:"
echo "  http://157.173.101.159:$PORT"
echo "(Note: 8080 is already used by another student's process on this shared VPS, so this dashboard runs on $PORT instead.)"
echo ""
