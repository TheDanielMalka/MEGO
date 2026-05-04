#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(os.environ.get('DATABASE_URL', 'postgresql://mego:mego@db:5432/mego'))
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
  sleep 1
done

echo "PostgreSQL is up – initializing database..."
python -c "from database import init_db; init_db()"

echo "Starting Gunicorn..."
exec gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 2 \
  --threads 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  "app:app"
