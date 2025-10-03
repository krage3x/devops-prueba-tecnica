#!/bin/bash
set -e

echo "Printing dir"
ls -la / 
# Generate redis conf for password
cat <<EOF > /data/redis.conf
bind 0.0.0.0
protected-mode yes
port 6379
requirepass ${REDIS_PASSWORD}
EOF

exec redis-server /data/redis.conf