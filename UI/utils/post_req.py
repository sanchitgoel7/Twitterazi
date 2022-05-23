import requests 
import json 

def get_endpoint():
    url = 'http://127.0.0.1:8080/'
    health = 'health/'
    form = 'main_bot/'
    return url, health, form 

def post_req (url, form, usernames):
    form_data = json.dumps({
        'usernames': usernames
    })
    response = requests.request("POST", url+form, data = form_data)
    #print("the response is" + str(response))

    return response.text