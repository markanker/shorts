#!/bin/bash
python3 manage.py migrate
gunicorn -w 3 -b 0.0.0.0:8000 shorts.wsgi:application