import json
from datetime import date

from .mongo_db_client import MongoDbClient


class RequestParser():

    def parse_get(self, data: dict) -> dict:
        return json.loads(data['data'])


class MongoDbRequestManager():

    def __init__(self):
        self.client = MongoDbClient()
        self.parser = RequestParser()

    def get_render_info(self, uuid: str) -> dict:
        """
            `uuid` - id as render directory
        """
        data = self.client.get(
            params = {
                'SK': f'$DIR#{ uuid }'
            }
        )

        return self.parser.parse_get(
            data = data[-1]
        )

    def get_model_info(self, name: str, date: str = None) -> dict:
        """
            `name` - model name

            `date` - date of model init in db (yyyy-mm-dd)
        """
        params = {
            'PK': f'$MODEL#{ name }.blend'
        }
        if date != None:
            params = dict(
                params,
                **{
                    'SK': f'$DATE#{ date }'
                }
            )

        data = self.client.get(
            params = params
        )

        return self.parser.parse_get(
            data = data[-1]
        )

    def insert_render_info(self, info: dict, render_type: str, uuid: str):
        """
            `info` - render meta-data dict

            `render_type` - choice from:

                '$SINGLE_IMG$KEYFRAME#{ set_id }'   - for single image from blend file

                '$SINGLE_SET$KEYFRAME#{ set_id }'   - for single set from blend file

                '$ALL'                              - for all sets from blend file

                '$SINGLE_VECTOR_IMG'                - for single image as vector customize

                '$SINGLE_VECTOR_SET'                - for single set as vector customize

            `uuid` - id as render directory
        """
        return self.client.post_one(
            Item = {
                'PK': f'$RENDER${ render_type }'
                'SK': f'$DIR#{ uuid }'
                'data': json.dumps(info)
            } 
        )


    def insert_model_info(self, name: str):
        """
            `name` - model name
        """
        return self.client.post_one(
            Item = {
                'PK': f'$MODEL#{ name }.blend'
                'SK': f'$DATE#{ date.today() }'
                'data': json.dumps(
                    {
                        'path': f'./static/models/{ name }'
                    }
                )
            } 
        )