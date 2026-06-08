class Connection:

    def get_user_info(self):

        return {
            "user_id": 1,
            "username": "putra",
            "line": "LINE_A"
        }


# import requests

# class Connection:

#     def get_user_info(self, token):

#         response = requests.get(
#             "http://laravel/api/user",
#             headers={
#                 "Authorization": f"Bearer {token}"
#             }
#         )

#         return response.json()