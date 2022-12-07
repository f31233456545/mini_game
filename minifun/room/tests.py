from django.test import TestCase, Client 
from models import UserInfo, Room
import requests
import json 
import time 

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
        self.api_register()
        self.api_login()
        self.api_create_room()
        self.api_join_room()
        self.api_start_game()
        self.api_action()
        self.api_sit()
        self.api_stand()
        self.api_request_room_list()
        self.api_exit_room()

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

        print("    正常创建")
        response = self.client.get('/create_room/', QUERY_STRING="creator_name=lyc&room_name=test_room&game_kind=0&private=0")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    无房间名或创建用户名(数据丢失)")
        response = self.client.get('/create_room/', QUERY_STRING="creator_nam=lyc&room_nam=test_room&game_kind=0&private=0")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    无游戏类型(数据丢失)，game_kind默认设置为0")
        response = self.client.get('/create_room/', QUERY_STRING="creator_name=lyc&room_name=test_room&game_kin=0&private=0")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    不存在的用户创建房间")
        response = self.client.get('/create_room/', QUERY_STRING="creator_name=qwe&room_name=test_room&game_kind=0&private=0")
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

    def api_register(self):
        print("API register:")
        print("    正常注册")
        response = self.client.get('/register/', QUERY_STRING="username=lyc&password=123")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    注册已有用户名")
        response = self.client.get('/register/', QUERY_STRING="username=lyc&password=123")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

    def api_login(self):
        print("API login:")
        print("    正常登录")
        response = self.client.get('/login/', QUERY_STRING="username=lyc&password=123")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    登录不存在用户名")
        response = self.client.get('/login/', QUERY_STRING="username=qwe&password=123")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    密码错误")
        response = self.client.get('/login/', QUERY_STRING="username=lyc&password=1237")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

    def api_join_room(self):
        print("API join_room:")
        print("    正常加入房间")
        response = self.client.get('/join_room/', QUERY_STRING="room_id=3&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    无房间名或用户名(数据丢失)")
        response = self.client.get('/join_room/', QUERY_STRING="room_i=3&user_nam=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    未注册的玩家加入房间")
        response = self.client.get('/join_room/', QUERY_STRING="room_id=3&user_name=qwe")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    加入不存在的房间")
        response = self.client.get('/join_room/', QUERY_STRING="room_id=9&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    已在房间的用户加入房间")
        response = self.client.get('/join_room/', QUERY_STRING="room_id=3&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

    def api_exit_room(self):
        print("API exit_room:")
        print("    正常退出")
        response = self.client.get('/exit_room/', QUERY_STRING="room_id=3&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    传输过程中信息丢失")
        response = self.client.get('/exit_room/', QUERY_STRING="room_i=3&user_nam=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    不存在的用户退出")
        response = self.client.get('/exit_room/', QUERY_STRING="room_id=3&user_name=qwe")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    退出不存在的房间")
        response = self.client.get('/exit_room/', QUERY_STRING="room_id=9&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    不在房间内的用户退出(返回结果为房间不存在，因为最后一个玩家退出房间后房间会消失)")
        response = self.client.get('/exit_room/', QUERY_STRING="room_id=3&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')
        

    def api_sit(self):
        print("API sit:")
        print("    正常坐下")
        response = self.client.get('/sit/', QUERY_STRING="room_id=3&user_name=lyc&chip_cnt=500")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    房间不存在")
        response = self.client.get('/sit/', QUERY_STRING="room_id=9&user_name=lyc&chip_cnt=500")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    不在房间内的用户坐下")
        response = self.client.get('/sit/', QUERY_STRING="room_id=3&user_name=qwe&chip_cnt=500")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    坐下的人再坐下")
        response = self.client.get('/sit/', QUERY_STRING="room_id=3&user_name=lyc&chip_cnt=500")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

    def api_stand(self):
        print("API stand:")
        print("    正常站起")
        response = self.client.get('/stand/', QUERY_STRING="room_id=3&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    站起的房间不存在")
        response = self.client.get('/stand/', QUERY_STRING="room_id=9&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    未坐下的人站起")
        response = self.client.get('/stand/', QUERY_STRING="room_id=3&user_name=qwe")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

    def api_request_room_list(self):
        print("API request_room_list:")
        print("    正常请求")
        response = self.client.get('/request_room_list/', QUERY_STRING="game_kind=0&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')
        

    def api_request_game_info(self):
        print("API request_game_info:")
        print("    正常请求")
        response = self.client.get('/request_game_info/', QUERY_STRING="room_id=3&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("    请求不存在的房间的信息")
        response = self.client.get('/request_game_info/', QUERY_STRING="room_id=9&user_name=lyc")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

    def api_start_game(self):
        print("API start_game:")
        print("    人数少于二开始游戏")
        response = self.client.get('/start_game/', QUERY_STRING="room_id=3")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

    def api_action(self):
        print("API action:")
        print("    正常行动(无返回值)")
        response = self.client.get('/action/', QUERY_STRING="user_name=lyc&action_type=0&raise_num=0&room_id=3")
        response_text = response.content.decode("utf-8")
        print("    不存在的房间的请求")
        response = self.client.get('/action/', QUERY_STRING="user_name=lyc&action_type=0&raise_num=0&room_id=9")
        response_text = response.content.decode("utf-8")
        print("\033[36m" + str(response_text) + "\033[0m")
        print("    不在房间内玩家的行动(无返回值)")
        response = self.client.get('/action/', QUERY_STRING="user_name=lyc&action_type=0&raise_num=0&room_id=3")
        response_text = response.content.decode("utf-8")
        self.assertEqual(
            response.status_code,
            200,
            "Test Failed"
        )
        print('\033[32m  Pass\033[0m')

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

def performance_test(method, url, body_data=None, query_string=None, rest_query_string=None):
    my_url = host + url 
    if rest_query_string:
        my_url = my_url + str(rest_query_string)
    if query_string:
        my_url = my_url + "?" + query_string
    if method == "GET" and body_data:
        body_data = json.dumps(body_data)

    print("Test "+url[1:url.len():1])
    start_time = time.time()

    response_data = requests.request(method, my_url, data=body_data, headers=headers)

    end_time = time.time()
    span = end_time - start_time

    response_content = response_data.content.decode("utf-8")
    if response_content.find("True") or response_content.find("true"):
        print("\033[32m    Pass\033[0m")
    else:
        print("\031[32m    Fail\031[0m")
    print("Test Details:")
    print(response_content)
    print("Time Spent:\n", round(span, 4), 'sec')

performance_test("GET", "/register/", query_string="username=zky_test&password=123456")
performance_test("GET", "/login/", query_string="username=zky_test&password=123456")
performance_test("GET", "/create_room/", query_string="creator_name=zky_test&room_name=zky_room")
performance_test("GET", "/join_room/", query_string="user_name=zky_test&room_id=1")
performance_test("GET", "/request_game_info/", query_string="user_name=zky_test")

