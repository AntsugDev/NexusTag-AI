import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.users import Users

try:
    user = Users()

    # print(f"user insert ...")
    # last_id = user.insert({
    #     "username": "JohnDoe2",
    #     "password": "password2"
    # })

    # print("update ...")
    # last_id = user.updateById(data={
    #     "username": "JohnDoe",
    #     "password": "password1"
    # }, id=1)
    # print(last_id)

    # print("delete ...")
    # last_id = user.deleteById(id=1)
    # print(last_id)

    print("delete all...")
    last_id = user.deleteAll()
    print(last_id)
    
    # last_id = 1
    # print(f"user find by id {last_id} ...")
    # response = user.findBy(where=[{"type": "AND", "column": "id", "operator": "=", "value": last_id}])
    # print(response)

    print("paginate ...")
    response = user.list()
    print(response)

except Exception as e:
    raise e
