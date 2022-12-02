from django.test import TestCase, Client 
from .models import UserInfo, Room
import requests
import json 

host = "http://127.0.0.1:8000"
headers = {'content-Type': 'application/json', 'Accept': '*/*'}

class APITestCase(TestCase):
    def setUp(self):
        u = UserInfo(username="adam", password=123)
        u.save()
        r = Room(room_id=1, room_name="adam_room", private=False,
             game_kind=0, creator_name="adam", creator=u, 
             player_num=0, viewer_num=0, max_num=13)
        r.save()
        print("Set up")
        
    def tearDown(self):
        for u in UserInfo.objects.all():
            u.delete()
        for r in Room.objects.all():
            r.delete()
        print("Tear Down")

    def test_contents(self):
        self.models_UserInfo()
        self.models_Room()
        self.api_create_room()

    def models_UserInfo(self):
        print("Model UserInfo:")
        u = UserInfo.objects.filter(username="adam")[0]
        Room(room_id=2, room_name="adam_room_2", private=False,
             game_kind=0, creator_name="adam", creator=u, 
             player_num=0, viewer_num=0, max_num=13).save()
        self.assertEqual(
            Room.objects.filter(room_id=2).count(),
            1,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

    def models_Room(self):
        print("Model Room:")
        UserInfo(username="eva", password=123).save()
        self.assertEqual(
            UserInfo.objects.filter(username="eva").count(),
            1,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

    def api_create_room(self):
        print("API create_room:")
        flag = False
        response = self.client.get('/create_room/', QUERY_STRING="creator_name=adam&room_name=test_room&game_kind=0&private=0")
        response_text = response.content.decode("utf-8")
        if response_text.find('"succeed": true') != -1:
            flag = True
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        if flag == True:
            print('\033[32m  Pass\033[0m')
        else:
            print('\033[31m  Fail\033[0m')


    
# Test without using Django TestCase
def api_test(method, url, body_data=None, query_string=None, rest_query_string=None):
    my_url = host + url 
    if rest_query_string:
        my_url = my_url + str(rest_query_string)
    if query_string:
        my_url = my_url + "?" + query_string
    if method == "GET" and body_data:
        body_data = json.dumps(body_data)
    response_data = requests.request(method, my_url, data=body_data, headers=headers)
    response_content = response_data.content.decode("utf-8")
    if response_content.find("True") or response_content.find("true"):
        print("Test passed.")
    else:
        print("Test failed.")
    print("Test Details:")
    print(response_content)

# Example
#api_test("GET", "/create_room/", query_string="username=zky&password=123")

