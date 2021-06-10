# down frontend & backend & redis

    sudo docker-compose down

# down nginx

    sudo docker-compose -f ./micro-services/docker-compose.yml down

# remove all networks

    sudo docker network rm micro-services_nginx
    sudo docker network rm render-app-backend_general
