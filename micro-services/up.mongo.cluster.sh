# mongo cluster

    # create cluster networks

        docker network create router-server_mongo-router
        docker network create config-servers_mongo-config-and-shards

    # run mongo config node
        docker-compose -f ./mongodb/config-servers/docker-compose.yml up -d

    # run mongo shard node
        docker-compose -f ./mongodb/shard-servers/docker-compose.yml up -d

# ps sequence
    docker-compose -f ./mongodb/config-servers/docker-compose.yml ps
    docker-compose -f ./mongodb/shard-servers/docker-compose.yml ps

sleep 5

# configuration
    # config config node
        mongo mongodb://localhost:50000 --eval "rs.initiate( \
            { \
                _id: 'cfgrs', \
                configsvr: true, \
                members: [ \
                    { _id : 0, host : 'mongo-config-server-00:27017' }, \
                    { _id : 1, host : 'mongo-config-server-01:27017' }, \
                    { _id : 2, host : 'mongo-config-server-02:27017' }  \
                ] \
            } \
        )"
        sleep 20
        mongo mongodb://localhost:50000 --eval "rs.status()"


    # config shard node
        mongo mongodb://localhost:60000 --eval "rs.initiate( \
            { \
                _id: 'shard-00-rs', \
                members: [ \
                    { _id : 0, host : 'mongo-shard-00-server-00:27017' }, \
                    { _id : 1, host : 'mongo-shard-00-server-01:27017' }, \
                    { _id : 2, host : 'mongo-shard-00-server-02:27017' }  \
                ] \
            } \
        )"
        sleep 20
        mongo mongodb://localhost:60000 --eval "rs.status()"

# run mongo cluser router
    docker-compose -f ./mongodb/router-server/docker-compose.yml up -d

# ps sequence
    docker-compose -f ./mongodb/router-server/docker-compose.yml ps

# configuration
    # config router
        sleep 5
        mongo mongodb://localhost:59999 --eval "sh.addShard('shard-00-rs/mongo-shard-00-server-00,mongo-shard-00-server-01,mongo-shard-00-server-02')"
        mongo mongodb://localhost:59999 --eval "sh.status()"
    
    # config database / table / sharding (for database / table init)
        # mongo mongodb://localhost:59999 --eval "sh.enableSharding('render-app')"
        # mongo mongodb://localhost:59999 --eval "sh.shardCollection('render-app.meta-data', key = { 'PK': 1, 'SK': 1 })"
