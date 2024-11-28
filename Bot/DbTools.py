import requests


class UserData:
    def __init__(self):
        self.base_url = 'https://tiutour.ru/api/v1/'
        self.users_url = 'users/'

    def create_user(self, user_id, user_name):
        if user_name == None or user_name == "":
            user_name = user_id
        data = {
            'user_id': user_id,
            'user_name': user_name,
        }

        response = requests.post(self.base_url+self.users_url, json=data)

        status_code = response.status_code

        if status_code == 201:
            return True
        else:
            return False