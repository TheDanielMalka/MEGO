#!/bin/bash
# ──────────────────────────────────────────────────────────────────────────────
# EC2 User-Data / Startup Script – MEGO HR
#
# Paste this into EC2 → Advanced Details → User data when launching the instance.
# It runs once on first boot as root.
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail
exec > >(tee /var/log/mego-startup.log) 2>&1
echo "=== MEGO Startup: $(date) ==="

# ── 1. System packages ────────────────────────────────────────────────────────
apt-get update -y
apt-get install -y \
  ca-certificates curl gnupg git

# ── 2. Install Docker ─────────────────────────────────────────────────────────
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

systemctl enable docker
systemctl start docker
usermod -aG docker ubuntu

# ── 3. Clone repository ───────────────────────────────────────────────────────
mkdir -p /opt/mego
cd /opt/mego

# If already cloned, just pull. Otherwise clone fresh.
if [ -d ".git" ]; then
  git pull origin main
else
  git clone https://github.com/thedanielmalka/mego.git .
fi

cd Final-Project

# ── 4. Create .env from EC2 Parameter Store or hardcoded secrets ─────────────
# NOTE: Replace the values below with your actual secrets.
# Better: use AWS SSM Parameter Store and fetch them:
#   aws ssm get-parameter --name /mego/POSTGRES_PASSWORD --with-decryption --query 'Parameter.Value' --output text
cat > .env <<'ENVEOF'
POSTGRES_DB=mego
POSTGRES_USER=mego
POSTGRES_PASSWORD=REPLACE_WITH_STRONG_PASSWORD
SECRET_KEY=REPLACE_WITH_LONG_RANDOM_STRING
DATABASE_URL=postgresql://mego:REPLACE_WITH_STRONG_PASSWORD@db:5432/mego
ENVEOF

# ── 5. Pull images & start stack ─────────────────────────────────────────────
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d

# ── 6. Systemd service for auto-restart on reboot ────────────────────────────
cat > /etc/systemd/system/mego.service <<'SVCEOF'
[Unit]
Description=MEGO HR Docker Compose Stack
After=docker.service network-online.target
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/mego/Final-Project
ExecStart=/usr/bin/docker compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker compose -f docker-compose.prod.yml down
TimeoutStartSec=300

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable mego.service

echo "=== MEGO Startup complete: $(date) ==="
echo "App should be running on port 80"
docker compose -f docker-compose.prod.yml ps
