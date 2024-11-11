import requests


BASE = "http://127.0.0.1:8010/"
# response= requests.get(BASE+'helloworld')
# print(response.json())
# response= requests.post(BASE+'helloworld')
# print(response.json())
# response= requests.get(BASE+'helloworld/jim/21')
# response= requests.get(BASE+'helloworld/jim')

# data = [{"likes":12, "name" :"soe" , "views" : 12322},
#         {"likes":10, "name" :"sdoe" , "views" : 1223},
#         {"likes":104, "name" :"ssdoe" , "views" : 1323}]

# for i in range(len(data)):
#     response = requests.put(BASE + 'video/' + str(i) , json= data[i])
#     print(response.json())
# input()
# response= requests.delete(BASE+'video/1')
# print(response)
# input()
# response= requests.get(BASE + 'video/0')
# print(response)

response= requests.patch(BASE + 'video/0' , json={"likes": 20})
print(response)