# mongo cluster
    # down mongo config node
        docker-compose -f ./micro-services/mongodb/config-servers/docker-compose.yml down

    # down mongo shard node
        docker-compose -f ./micro-services/mongodb/shard-servers/docker-compose.yml down

    # down mongo cluser router
        docker-compose -f ./micro-services/mongodb/router-server/docker-compose.yml down

# down render-app-frontend & render-app-backend & nginx
    docker-compose -f ./docker-compose.yml down