#authentication credentials were not provided was being done because using oauth2 instead of bearer token
# # # transfer script
# import requests

# headers = {
#     "Authorization": "Token d6e8ad8b39f6e98795975bc2c422fef032df3b30",
    
    
# }


# url = "http://127.0.0.1:8000/api/transfer/567845687584/"

# data = {
    
#     "source_account":"567845687584",
#     "target_account":"123456789098",
#     "amount": 100
# }
# response = requests.post(url, headers=headers,json=data)

# if response.status_code == 200:
#     print("Balance:", response.json())
# # if (
# #     response.status_code != 204 and
# #     response.headers["content-type"].strip().startswith("application/json")
# # ):
# #     try:
# #         print(response.json()) 
# #     except ValueError:
# #         print('fail')
# else:
#     print('fail')

# # import requests
# # import json
# # # Token = "30f6d7b1ba35d1ced7cff718d73529bf632cd7e6"

# # headers = {
# #     "Authorization": "Token 30f6d7b1ba35d1ced7cff718d73529bf632cd7e6",  # Include the access token in the Authorization header
    
# # }



# # # Endpoint URL
# # withdraw_url = "http://127.0.0.1:8000/api/deposit/123456789098/"


# # # data = {
# # #     "amount": 40
# # # }

# # # Send POST request to the withdraw endpoint
# # response = (requests.get(withdraw_url,headers=headers))

# # # Check the response
# # if response.status_code == 200:
# #     print("Withdrawal successful!")
# #     print(response.json())
# # else:
# #     print('fail')


#transfer successful IsAuthenticated
# import requests

# url = "http://127.0.0.1:8000/api/transfer/123456789090/"
# headers = {
#     "Authorization": "token 1e6811be285b644af610ae7517a01b154d715331",
#     "Content-Type": "application/json"
# }
# data = {
#     "source_account": "123456789090",
#     "target_account": "567845687584",
#     "amount": "20.00"
# }

# response = requests.post(url, json=data, headers=headers)

# if response.status_code == 200:
#     print("Transfer successful.")
#     print("New Balance:", response.json().get("new_balance"))
# else:
#     print("Transfer failed.")
#     # print("Detail:", response.json().get("detail"))


#balance fetching correct request
# import requests

# url = "http://127.0.0.1:8000/api/balance/567845687584/"
# headers = {
#     "Authorization": "token 1e6811be285b644af610ae7517a01b154d715331",
#     "Content-Type": "application/json"
# }
# # data = {
# #     "source_account": "123456789090",
# #     "target_account": "567845687584",
# #     "amount": "20.00"
# # }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     # print("Transfer successful.")
#     print("New Balance:", response.json().get("balance"))
# else:
#     print("Transfer failed.")
#     # print("Detail:", response.json().get("detail"))

#working previous transactions list
# import requests

# url = "http://127.0.0.1:8000/api/transactions/567845687584/"
# headers = {
#     "Authorization": "token 1e6811be285b644af610ae7517a01b154d715331",
#     "Content-Type": "application/json"
# }
# # data = {
# #     "source_account": "123456789090",
# #     "target_account": "567845687584",
# #     "amount": "20.00"
# # }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     # print("Transfer successful.")
#     print(response.json())
# else:
#     print("Transfer failed.")
#     # print("Detail:", response.json().get("detail"))

#generate pdf of transactions for a given account

# import requests

# url = "http://127.0.0.1:8000/api/generate/"
# headers = {
#     "Authorization": "token 1e6811be285b644af610ae7517a01b154d715331",
#     "Content-Type": "application/json"
# }
# # data = {
# #     "source_account": "123456789090",
# #     "target_account": "567845687584",
# #     "amount": "20.00"
# # }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     # print("Transfer successful.")
#     print(response)
# else:
#     print("Transfer failed.")
#     # print("Detail:", response.json().get("detail"))


