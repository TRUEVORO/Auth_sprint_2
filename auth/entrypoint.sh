#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
done
echo "PostgreSQL started"

cd src || exit

if [ "$RUN_MODE" = "GRPC" ]
then
  python main_grpc.py
else
  gunicorn -c gunicorn/gunicorn.py -k gevent app:app
fi
