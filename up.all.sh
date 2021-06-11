# create networks

    sudo docker network create micro-services_nginx
    sudo docker network create render-app-backend_general

# run frontend & backend & redis

    sudo docker-compose up -d
    sudo docker-compose ps

    # collect static for backend

        sudo docker exec -it render-app-backend python3 manage.py makemigrations --no-input
        sudo docker exec -it render-app-backend python3 manage.py migrate --no-input
        sudo docker exec -it render-app-backend python3 manage.py collectstatic --no-input

    # sleep for complete deploy all services

        # sleep 10

# run nginx

    sudo docker-compose -f ./micro-services/docker-compose.yml up -d
    sudo docker-compose -f ./micro-services/docker-compose.yml ps
