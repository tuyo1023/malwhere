#!/bin/bash
echo "Hello anomaly_log_injection"

cat > /tmp/auth.log.tampered <<'EOF'
Server listening on 0.0.0.0 port 22. (modified)
Server listening on :: port 22. (modified)
EOF

mv /tmp/auth.log.tampered /var/log/auth.log

