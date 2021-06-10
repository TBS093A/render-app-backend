# init static file for google monitor django app

    mkdir ./application/static

# run mongo cluster

    ./micro-services/up.mongo.cluster.sh

# run render-app-frontend & render-app-backend & nginx
    # if cannot build use this:
        # docker-compose build --no-cache   

    docker-compose -f ./docker-compose.yml up -d
    docker-compose -f ./docker-compose.yml ps

# generate swagger static files (render-app-backend)

    docker exec -it render-app-backend python manage.py collectstatic --no-input
