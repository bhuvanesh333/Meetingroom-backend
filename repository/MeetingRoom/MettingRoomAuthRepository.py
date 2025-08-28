from database.dataBase_Initializer import Meetingroom_auth_collection

class MeetingRoomAuthRepository:
    def __init__(self):
        self.meetingroom_auth_collection = Meetingroom_auth_collection 
    
    def _get_meetingroom_user_field(self,  field_name_value:dict):
        result = self.meetingroom_auth_collection.find_one(field_name_value)
        return result
    