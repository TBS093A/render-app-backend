# sudo docker tag 26448532d156 render-app-backend
sudo docker run -b -p 6379 -d redis:5
sudo docker run -b -p 9090:9090 render-app-backend