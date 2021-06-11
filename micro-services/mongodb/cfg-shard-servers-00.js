
// mongo mongodb://mongo-shard-00-server-00:27017

rs.initiate(
    {
        _id: "shard1rs",
        members: [
            { _id : 0, host : "mongo-shard-00-server-00:27017" },
            { _id : 1, host : "mongo-shard-00-server-01:27017" },
            { _id : 2, host : "mongo-shard-00-server-02:27017" }
        ]
    }
)

rs.status()