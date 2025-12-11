from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from database.dataBase_Initializer import user_sessions_collection
from pymongo.errors import PyMongoError

from schema.commonSchema import user_Session



class ClusterUserSessionsRepository:

    def __init__(self):
        self.user_sessions_collection = user_sessions_collection

    def _is_session_empty(self):
        try:
            is_not_empty = True if self.user_sessions_collection.count_documents({}) == 0 else False
            return is_not_empty
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def _get_user_session(self,user_id):
        try:
            result = self.user_sessions_collection.find_one({"user_id":user_id})
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def _create_user_session(self,user_id,session_token):
        try:
            userSession = user_Session(user_id=user_id,
                                       session_token=session_token,
                                       is_active=True,
                                       expire_at=datetime.now(timezone.utc)+timedelta(hours=1,days=2), # set by common config FIXME
                                       last_accessed=datetime.now(timezone.utc)).model_dump()
            
            result = self.user_sessions_collection.insert_one(userSession)
            return result.inserted_id
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    def _update_user_session(self,user_id,session_token,is_active:bool):
        try:
            expire_at = datetime.now(timezone.utc)
            if is_active:
                expire_at = datetime.now(timezone.utc)+timedelta(hours=1,days=2)
            userSession = user_Session(user_id=user_id,
                                       session_token=session_token,
                                       is_active=is_active,
                                       expire_at=expire_at, # set by common config FIXME
                                       last_accessed=datetime.now(timezone.utc)).model_dump()
            
            result = self.user_sessions_collection.update_one(
                                                {"user_id": user_id},
                                                {"$set": userSession},
                                                upsert=True   # optional, if you want insert when not exists
                                            )
            return result
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")