#!/bin/bash

echo "Start service"

python scripts/migrate.py

# python scripts/load_data.py \
# fixtures/clinic/clinic.user.json \
# fixtures/clinic/clinic.doctor.json \
# fixtures/clinic/clinic.service.json \
# fixtures/clinic/clinic.timetable.json \
# fixtures/clinic/clinic.doctor_to_service.json

exec uvicorn backend.main:create_app --host=$BIND_IP --port=$BIND_PORT