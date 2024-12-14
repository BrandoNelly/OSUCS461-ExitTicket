# Classes and Router init made in collaboration with Daniel Lounsbury

import hashlib
import time
from typing import List
from OSUCS461.Config import MySQL as DatabaseConfig
from OSUCS461.ThirdParty.MySQL import MySQL
from Models import User, UserPost, ReadUser, ReadUserPost, PreviewUserPost  
DB = MySQL(**DatabaseConfig)

def timeandu(seed):
    timestamp = str(time.time())
    raw_uuid = f"{seed}-{timestamp}"
    uuid = hashlib.sha224(raw_uuid.encode('utf-8')).hexdigest()
    return timestamp, uuid
    
class UserLogic:
    @staticmethod
        
    def get_all_users() -> List[ReadUser]:
        query = "SELECT uuid, name, time_created FROM user"  
        results = DB.get_results(query)
        if not results:
            return []
        return [ReadUser(uuid=row['uuid'], name=row['name'], time_created=row['time_created']) for row in results]

    @staticmethod
    def get_by_uuid(uuid: str) -> ReadUser:
        query = f"SELECT uuid, name, time_created FROM user WHERE uuid = '{uuid}'"
        result = DB.get_row(query)
        if not result:
            raise ValueError(f"User with UUID {uuid} not found.")
        return ReadUser(uuid=result['uuid'], name=result['name'], time_created=result['time_created'])

    @staticmethod
    def create(name: str) -> ReadUser:
        timestamp, uuid = timeandu(name)
        query = f"INSERT INTO user (uuid, name, time_created) VALUES ('{uuid}', '{name}', '{timestamp}')"
        res = DB.query(query)
        if not res:
            raise ValueError('Post failed')
        return UserLogic.get_by_uuid(uuid)

    @staticmethod
    def save(user: User) -> ReadUser:
        query = f"UPDATE user SET name = '{user.name}' WHERE uuid = '{user.uuid}'"
        res = DB.query(query)
        if not res:
            raise ValueError('Post failed')
        return UserLogic.get_by_uuid(user.uuid)

    @staticmethod
    def delete(uuid: str) -> bool:
        query = f"DELETE FROM user WHERE uuid = '{uuid}'"
        return DB.query(query)

class PostLogic:
    @staticmethod
    def get_all() -> List[PreviewUserPost]:
        query = f"SELECT uuid, post_9char, time_created FROM user_post"
        results = DB.get_results(query)
        if not results:
            return []
        return [PreviewUserPost(uuid=row['uuid'], post_9char=row['post_9char'], time_created=row['time_created']) for row in results]
    
    @staticmethod
    def get_by_uuid(uuid: str) -> ReadUserPost:
        query = f"SELECT uuid, user_uuid, post_9char, text, time_created FROM user_post WHERE uuid = '{uuid}'"
        result = DB.get_row(query)
        if not result:
            return []
        return ReadUserPost(
            uuid=result['uuid'],
            user_uuid=result['user_uuid'],
            post_9char=result['post_9char'],
            text=result['text'],
            time_created=result['time_created'],
        )
    
    @staticmethod
    def get_by_user(uuid: str) -> List[PreviewUserPost]:
        query = f"SELECT uuid, post_9char, time_created FROM user_post WHERE user_uuid = '{uuid}'"
        results = DB.get_results(query)
        if not results or results == []:
            raise ValueError(f"Posts with user UUID {uuid} not found.")
        return [PreviewUserPost(uuid=row['uuid'], post_9char=row['post_9char'], time_created=row['time_created']) for row in results]
    
    @staticmethod
    def create(text: str, uuuid: str) -> ReadUserPost: 
            timestamp, uuid = timeandu(text)
            query = f"INSERT INTO user_post (uuid, user_uuid, post_9char, text, time_created) VALUES ('{uuid}', '{uuuid}', '{text[:9]}', '{text}', '{timestamp}')"
            res = DB.query(query)
            if not res:
                raise ValueError('Post failed')
            return PostLogic.get_by_uuid(uuid)
    
    @staticmethod
    def save(post: UserPost) -> ReadUserPost:
        query = f"UPDATE user_post SET user_uuid = '{post.user_uuid}', post_9char = '{post.post_9char}', text = '{post.text}', time_created = '{post.time_created}' WHERE uuid = '{post.uuid}'"
        res = DB.query(query)
        if not res:
            raise ValueError('Post save failed')
        return PostLogic.get_by_uuid(post.uuid)

    @staticmethod
    def delete(uuid: str) -> bool:
        query = f"DELETE FROM user_post WHERE uuid = '{uuid}'"
        return DB.query(query)
