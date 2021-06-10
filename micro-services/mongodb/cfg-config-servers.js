
// mongo mongodb://mongo-config-server-00:27017

rs.initiate(
    {
        _id: "cfgrs",
        configsvr: true,
        members: [
            { _id : 0, host : "mongo-config-server-00:27017" },
            { _id : 1, host : "mongo-config-server-01:27017" },
            { _id : 2, host : "mongo-config-server-02:27017" }
        ]
    }
)
  
rs.status()