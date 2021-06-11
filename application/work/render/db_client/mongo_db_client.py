import pymongo
from work.settings import (
    MONGO_DB_ADDRESS,
    MONGO_SHARD_DB_NAME,
    MONGO_SHARD_COLLECTION_NAME
)


class MongoDbClient():
    """
        MongoDb client class
        This configuration used a one table for cache / storage of products.
        
        PrimaryKey has been declare as two colums like - `PK`, `SK`, `DT`
        `PK` - is a group for products - sorting by PHRASE / LINK
        `SK` - is a subgroup identities single product in group defined by `PK`
        `DT` - is a unique value identities single product in time (PHRASE) or links (LINK)
        collection structure for documents saving as word phrase: 
        
            # By `product_id`:
            
                {
                    # Shard Key ( `PK` + `SK` + `DT` )
                        
                        'PK': '$PHRASE#{ product_phrase }$TYPE#PRODUCT_ID', 
                        'SK': '$PRODUCT_ID#{ product_id }',
                        'DT': '$DATE#{ date( yyyy-mm-dd ) }'
                    # Other Fields
                        ...
                }
            # By `asin`:
                {
                    # Shard Key ( `PK` + `SK` + `DT` )
                        
                        'PK': '$PHRASE#{ product_phrase }$TYPE#ASIN', 
                        'SK': '$ASIN#{ product_id }',
                        'DT': '$DATE#{ date( yyyy-mm-dd ) }'
                    # Other Fields
                        ...
                }
        collection structure for documents saving as link:
            # By `gtin`:
                {
                    # Shard Key ( `PK` + `SK` + `DT` )
                        
                            'PK': '$LINK$TYPE#GTIN', 
                            'SK': '$GTIN#{ product_gtin }',
                            'DT': '$PRODUCT_ID#{ product_id }'
                        # or
                            'PK': '$LINK$TYPE#GTIN', 
                            'SK': '$GTIN#{ product_gtin }',
                            'DT': '$SEMBOT_LINK'
                    # Other Fields
                        ...
                }
            # By `asin`:
                {
                    # Shard Key ( `PK` + `SK` + `DT` )
                        
                        'PK': '$LINK$TYPE#ASIN', 
                        'SK': '$ASIN#{ product_asin }',
                        'DT': <empty>
                    # Other Fields
                        ...
                }
            # By `mpn`:
                {
                    # Shard Key ( `PK` + `SK` + `DT` )
                        
                        'PK': '$LINK$TYPE#MPN', 
                        'SK': '$MPN#{ product_mpn }',
                        'DT': <empty>
                    # Other Fields
                        ...
                }
        
        init this shard collection in db:
            sh.shardCollection(
                "google-monitor.products", 
                { 
                    'PK': 1,
                    'SK': 1,
                    'DT': 1 
                }
            )
    """

    def __init__(self):
        mongo_client = pymongo.MongoClient(
            MONGO_DB_ADDRESS
        )
        self.database = mongo_client[MONGO_SHARD_DB_NAME]
        self.table = self.database[MONGO_SHARD_COLLECTION_NAME]

    def check_that_the_document_or_documents_exist(self, params: dict, operator: str = None) -> bool:
        """
            `params` - params for query. Query has been checked that the response is not empty ( length > 0 ) as boolean value
                # PHRASE
                
                    # `product_id`:
                
                        {
                            'PK': '$PHRASE#{ products_phrase }$TYPE#GTIN'
                        }
                    # `asin`:
                        {
                            'PK': '$PHRASE#{ products_phrase }$TYPE#ASIN'
                        }
                # LINK
                    # `product_id` / `gtin`:
                        # if `gtin` exist
                            { 
                                'PK': '$LINK$TYPE#GTIN', 
                                ‘SK’: ‘$GTIN#{ product_gtin }’ 
                            }
                        # else
                            {
                                'PK': '$LINK$TYPE#GTIN', 
                                ‘SK’: ‘$GTIN#UNKNOWN’ 
                                ‘DT’: ‘$PRODUCT_ID#{ product_id }’ 
                            }
                    
                    # `asin`
                        {
                            'PK': '$LINK$TYPE#ASIN', 
                            ‘SK’: ‘$ASIN#{ product_asin }’ 
                        }
                    # `mpn`
                        {
                            'PK': '$LINK$TYPE#MPN', 
                            ‘SK’: ‘$MPN#{ product_mpn }’ 
                        }
            `operator` - default value is `None`, choose one option from this list:
                `None` - does nothing - normal query
                `$in` - find all products for criterias in list (list in params value, must be)
                `$gt` - start cursor finding from element initialized as `$gt`
                & more on https://docs.mongodb.com/manual/reference/operator/
            returned values:
                `True` / `False`
        """
        try:
            return self.table.count_documents(
                self.__parse_params_to_query(
                    params = params,
                    operator = operator
                )
            ) > 0
        except Exception as error:
            print(error)

    def get(self, params: dict, operator: str = None) -> list:
        """
            `params` - for example:
                
                # list of all products by phrase:
                    
                    {
                        'PK': '$PHRASE#{ product_name }$TYPE#PRODUCT_ID'
                    }
                
                # one product from phrase:
                
                    {
                        'PK': '$PHRASE#{ product_name }$TYPE#PRODUCT_ID'
                        'SK': '$PRODUCT_ID#{ product_id }',
                    }
                
                # single product information:
                    {
                        'PK': '$PHRASE#{ product_name }$TYPE#PRODUCT_ID',
                        'SK': '$PRODUCT_ID#{ product_id }',
                        'DT': '$DATE#{ date( yyyy-mm-dd ) }'
                    }
                
                # many products from different phrases:
                
                    {
                        'SK': '$PRODUCT_ID#{ product_id }'
                    }
                
                # one product details
                
                    # `gtin` / `product_id`:
                        # if gtin exist:
                        
                            {
                                'PK': '$LINK$TYPE#GTIN',
                                'SK': '$GTIN#{ product_gtin }',
                            }
                        # else
                            {
                                'PK': '$LINK$TYPE#GTIN',
                                'DT': '$PRODUCT_ID#{ product_id }'
                            }
                    # `asin`:
                
                        {
                            'PK': '$LINK$TYPE#ASIN',
                            'SK': '$ASIN#{ product_asin }',
                        }
                
                    # `mpn`:
                
                        {
                            'PK': '$LINK$TYPE#MPN',
                            'SK': '$MPN#{ product_MPN }',
                        }
            
            `operator` - default value is `None`, choose one option from this list:
                `None` - does nothing - normal query
                `$in` - find all products for criterias in list (list in params value, must be)
                `$gt` - start cursor finding from element initialized as `$gt`
                & more on https://docs.mongodb.com/manual/reference/operator/
            returned value
            
                [
                    ... ,
                    { 
                        'PK': '$PHRASE#materace', 
                        'SK': '$GTIN#4017807387889$DATE#2021-04-02',
                        'DT': '$DATE#{ date( yyyy-mm-dd ) }',
                        'title': ... ,
                        'price': ... ,
                        'currency': ... ,
                        'domain': ... 
                    },
                    ...
                ]
        """
        try:
            all_phrase_products = self.table.find(
                self.__parse_params_to_query(
                    params = params,
                    operator = operator
                )
            )
            return all_phrase_products
        except Exception as error:
            print(error)

    def __parse_params_to_query(self, params: dict, operator: str = None) -> dict:
        """
            `operator` - default: `None`, from:
                `None` - does nothing - return `params`
                `$in` - find all products for criterias in list
                `$gt` - start cursor finding from element initialized as `$gt`
            `params` - dict, examples:
            
                # for `None` operator: (does nothing)
                    {
                        'PK': '$PHRASE#{ product_name }$TYPE#PRODUCT_ID'
                    }
                # for `$in` operator:
                
                    {
                        'SK': [
                            '$PRODUCT_ID#{ product_id_0 }',
                            '$PRODUCT_ID#{ product_id_1 }',
                            ...
                        ]
                    }
                # for `$gt` operator:
                    {
                        '_id': '6092a0685cde9f150e46e9af'
                    }
            returned value:
                # for `None` operator: (does nothing)
                    {
                        'PK': '$PHRASE#{ product_name }$TYPE#PRODUCT_ID'
                    }
            
                # for `$in` operator:
                    {
                        'SK': { 
                            '$in': [
                                '$PRODUCT_ID#{ product_id_0 }',
                                '$PRODUCT_ID#{ product_id_1 }',
                                ...
                            ] 
                        }
                    }
                # for `$gt` operator:
                    {
                        '_id': {
                            '$gt': '6092a0685cde9f150e46e9af'
                        }
                    }
        """
        if operator == None:
            return params
        elif operator != None:
            return { f'{ key }': { f'{ operator }': value } for key, value in params.items() }

    def get_with_pagination(self, params: dict, pagination: dict, operator: str = None) -> dict:
        """
            `params` - params dict, looks like:
                {
                    'PK': '$PHRASE#{ product_name }$TYPE#PRODUCT_ID'
                }
            `pagination` - dict with pagination details, looks like:
                {
                    'elements_per_page': ... ,
                    'page': ...
                }
            `operator` - default value is `None`, choose one option from this list:
                `None` - does nothing - normal query
                `$in` - find all products for criterias in list (list in params value, must be)
                `$gt` - start cursor finding from element initialized as `$gt`
                & more on https://docs.mongodb.com/manual/reference/operator/
            returned value:
                {
                    'list': [
                        ... ,
                        { 
                            'PK': '$PHRASE#{ product_name }$TYPE#PRODUCT_ID', 
                            'SK': '$PRODUCT_ID#{ product_id }',
                            'DT': '$DATE#{ date( yyyy-mm-dd ) }',
                            'title': ... ,
                            'price': ... ,
                            'currency': ... ,
                            'domain': ... 
                        },
                        ...
                    ],
                    'page': ... ,
                    'elements_per_page': ...
                }
            
        """
        try:
            return self.__paginate(
                    elements_per_page = pagination['elements_per_page'],
                    params = params,
                    params_operator = operator
                ) 
        except Exception as error:
            print(error)

    def __paginate(self, pagination: dict, params: dict, params_operator: str = None):
        """
            `pagination` - dict with pagination details, looks like:
                {
                    'elements_per_page': ... ,
                    'page': ...
                }
            `params` - params dict, looks like:
                {
                    'PK': '$PHRASE#{ product_name }$TYPE#PRODUCT_ID'
                }
            `params_operator` - mongodb operator looks like:
             
                '$in' / '$gt' / '$regex'
            returned values:
                {
                    'list': [
                        ... ,
                        <single_element> ,
                        ...
                    ],
                    'page': ... ,
                    'elements_per_page': ...
                }
                        
        """
        pagination_list = []
        last_id = None

        for page in range( 1, int(pagination['page']) + 1 ):       
            
            if last_id == None:
                
                cursor_object = self.table.find(
                    self.__parse_params_to_query(
                        params = params
                    )
                ).limit(int( pagination['elements_per_page'] ))
            
            else:

                cursor_object = self.table.find(
                    dict(
                        self.__parse_params_to_query(
                            params = params,
                            operator = params_operator
                        ),
                        **self.__parse_params_to_query(
                            params = { '_id': last_id },
                            operator = '$gt'
                        )
                    )
                ).limit(int( pagination['elements_per_page'] ))
            
            if page == int(pagination['page']):
                pagination_list = [ single_document for single_document in cursor_object ]
            
            last_id = cursor_object[-1]['_id']

        return dict(
                {
                    'list': pagination_list,
                },
                **pagination
            )

    def post(self, items: list):
        """
            insert many values from list.
            `items` - looks just like this:
                [
                    ... ,
                    { 
                        'PK': '$PHRASE#materace', 
                        'SK': '$GTIN#4017807387889$DATE#2021-04-02',
                        'title': ... ,
                        'price': ... ,
                        'currency': ... ,
                        'domain': ... ,
                        'details': ...
                    },
                    ...
                ]
        """
        try:
            return self.table.insert_many(
                items
            )
        except Exception as error:
            print(error)
    
    def post_one(self, item: dict):
        """
            insert one dict value.
            
            `item` - looks just like this:
                {
                    'PK': ... , 
                    'SK': ... ,
                    'title': ... ,
                    'price': ... ,
                    'currency': ... ,
                    'domain': ... ,
                    'details': ...
                }
        """
        try:
            return self.table.insert_one(
                item
            )
        except Exception as error:
            print(error)