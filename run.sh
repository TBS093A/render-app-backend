sudo docker run -p 6379:6379 -d redis:5
python manage.py runserver 9090
exit $?