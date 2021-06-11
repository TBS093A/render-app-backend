sudo docker run -p 6379:6379 -d redis:5
# python manage.py runserver 9090
daphne -b 0.0.0.0 -p 9090 work.asgi:application
exit $?