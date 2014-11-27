web: gunicorn pollsys.wsgi --bind 0.0.0.0:${PORT:-5001}
subscribe: python manage.py subscribe
# provide: python manage.py provide
syncdb: python manage.py syncdb --noinput
