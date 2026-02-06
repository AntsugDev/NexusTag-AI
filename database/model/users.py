from .model_general import ModelGeneral
import hashlib
from utility.utility import ExceptionRequest

class User(ModelGeneral):
    def __init__(self):
        self.table = "users"
        

    def hash_string(self,input_string, algorithm='sha256'):
        hash_func = getattr(hashlib, algorithm)()
        hash_func.update(input_string.encode('utf-8'))
        return hash_func.hexdigest()

    def verify_string(self,input_string, hash_to_check, algorithm='sha256'):
        new_hash = self.hash_string(input_string, algorithm)
        return new_hash == hash_to_check   

    def get_by_username(self, username):
        try:
            count =  self.count_search({"username": username})
            return int(count) > 0
        except Exception as e:
            raise e
      

    def register(self, username, password):
        try:
            if not self.get_by_username(username):
             hashed_password = self.hash_string(password)
             result =  self.insert({"username": username, "password": hashed_password})   
             return result
            else:
                raise ValueError("Username already exists")
        except Exception as e:
            raise e

    def login(self, username, password):
        try:    
            user = self.search({"username": username})
           
            if not user:
                raise ValueError("User not found")
            convert = dict(user)
            if not self.verify_string(password, convert['password']):
                raise ValueError("Incorrect password")  
            return convert;
        except Exception as e:
            raise e

    def update_password(self, id, password):
        try:    
            user = self.search({"id": id})
            if not user:
                raise ValueError("User not found")
            hashed_password = self.hash_string(password)
            return self.update({"password": hashed_password}, id)          
        except Exception as e:
            raise e