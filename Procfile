web: gunicorn licitflow.wsgi:application --chdir licitflow --workers 2 --timeout 60 --log-file -
release: python licitflow/manage.py migrate