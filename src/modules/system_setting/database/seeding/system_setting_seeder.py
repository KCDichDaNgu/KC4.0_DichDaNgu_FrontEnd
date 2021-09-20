from core.seeder.base import BaseSeeder
from uuid import uuid4
from datetime import datetime

class SystemSettingSeeder(BaseSeeder):

    def __init__(self, db_client, collection_name, mongodb_uri = None, database_name = None) -> None:
        super().__init__(db_client, mongodb_uri, database_name)  

        self.collection_name = collection_name

        self.coll_connection = self.db[collection_name]

    async def run(self, session=None):

        saved_sys_setting = await self.coll_connection.find_one({}, session=session)

        if not saved_sys_setting:
            result = await self.coll_connection.insert_one({
                '_id': uuid4(),
                'max_user_text_translation_per_day': 0,
                'max_user_doc_translation_per_day': 0,
                'task_expired_duration': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            session=session)

            if result.inserted_id:
                print("System setting seeding successfully")

            else:
                raise Exception("System setting seeding fail")
