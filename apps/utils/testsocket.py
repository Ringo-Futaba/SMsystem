import os
import sys
import json
from django_redis import get_redis_connection

# 模拟socket端

class SocketService:
    def __init__(self):
        sys.path.extend([os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))])  # 项目根路径
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SMsystem.settings")

        self.con = get_redis_connection("default")

        # print("------服务初始化或有设备连上来了----")
        # self.send_equipment_info()

        p = self.con.pubsub()
        # 订阅web_service端的消息
        p.subscribe("web_service")
        for msg in p.listen():
            print(msg)
            # 如果不是用户发送的消息 则忽略
            if msg["type"] != "message":
                continue
            # 数据解码
            """
            w_data格式：

            {
                "type": "register",
                "addr": "addr",
                "t_id": t_id,
                "socket_code": socket_code
               }

            """
            w_data = msg['data'].decode('utf-8')
            w_data = json.loads(w_data)

            # 根据数据类型采取不同措施
            if w_data["type"] == "register":  # 终端注册
                self.return_register_result(w_data)

    def return_register_result(self, w_data):
        """返回注册结果"""
        print("正在验证数据")
        print("终端->" + w_data["t_id"] + "正在进行注册...")
        print("注册结果")
        # 成功code返回1, 失败返回0
        s_data = {"type": "register_result",
                  "code": 1,
                  "t_id": w_data["t_id"],
                  "t_data": {"serial": "asdasdas1d515",
                 "mac": "ASD-VF51-VF",
                 "status": 1,
                 "heartbeat_utc": 1234567890,
                 "addr": "192.168.1.26",
                 "t_type": "设备型号",
                 "disk": "50%",
                 "cpu":"50%",
                 "memory":"50%"},
                  # "socket_code": w_data["socket_code"]
                  }
        s_data = json.dumps(s_data)
        # 返回注册成功的消息给web_service
        self.con.publish("socket_service", s_data)

    # socket端会维护一个设备在线列表 当有设备连接上来的时候更新这个列表 并将其推送到redis的socket_service频道
    # 这边这个方法模拟这个场景 监听设备端 当有设备连上来的时候触发该函数
    def send_equipment_info(self):
        """发送连接设备列表"""
        time = 1234567890
        data = {
            "msg_type": "link_list",
            "type": "link",
            "online": [
                {"serial": "asdasdas1d515", "mac": "ASD-VF51-VF", "time": time,
                 "status": 1, "addr": "192.168.1.26", "t_type": "设备型号", "tags": [1], "disk": "50%", "cpu": "50%",
                 "memory": "50%"},
                {"serial": "asdasdasdasd1", "mac": "ASD-151-152", "time": time,
                 "status": 1, "addr": "192.168.1.27", "t_type": "设备型号", "tags": [1, 2], "disk": "50%", "cpu": "50%",
                 "memory": "50%"},
            ],
            "offline": [
                {"serial": "zcxdfgfd12fdg", "mac": "SADZXCS-45-15", "time": time,
                 "status": 1, "addr": "192.168.1.28", "t_type": "设备型号", "tags": [], "disk": "50%", "cpu": "50%",
                 "memory": "50%"},
                {"serial": "nhghjkjjjkj26", "mac": "SADA2-15-12",
                 "time": time, "status": 1, "addr": "192.168.1.29", "t_type": "设备型号", "tags": [3], "disk": "50%",
                 "cpu": "50%", "memory": "50%"},
            ],
            "noauth": [
                {"serial": "qweweretert23", "mac": "ASDASD-215-12", "time": time, "status": 1, "addr": "192.168.1.56"},
                {"serial": "werwer15werwe", "mac": "AS-25-ASDA", "time": time, "status": 1, "addr": "192.168.1.57"},
            ]
        }
        data = json.dumps(data)
        self.con.publish("socket_service", data)

    def send_alarm_msg(self):
        """发送连接设备列表"""
        # time = 1234567890
        data = {'type': 'alarm',
                'serial': 'asdasdas1d515',
                'msg': 'T111101102130012',
                'alarm_time': 1618665678,
                'level': 3,
                'alarm_type': 2,
                'msg_len': 18}
        data = json.dumps(data)
        self.con.publish("socket_service", data)

if __name__ == '__main__':
    t = SocketService()
#     content = """2021-04-16^21:41:14 INFO root session accepted login on /admin/my_internet_settings/my_base_setting_out for root from 172.16.5.50
#
# 2021-04-16^21:51:22 INFO root gmswan gmswan start successfully,configuration is right 172.16.1.254,rightsubnet 172.16.10.0/24,leftsubnet 172.16.5.0/24,ca ca,container D825B001A7DF
# 202 383 info sll
#
# 20234444   info
# 2021-04-17^12:13:58 INFO root sslvpn sslvpn deactivated successfully
# 2021-04-17^12:14:08 INFO root sslvpn sslvpn enabled successfully
# 2021-04-17^12:14:39 INFO root sslvpn sslvpn enabled successfully
# 2021-04-17^12:22:49 INFO root gmswan gmswan start successfully,configuration is right 172.16.1.254,rightsubnet 172.16.10.0/24,leftsubnet 172.16.5.0/24,ca ca,container D825B001A749
# 2021-04-17^12:22:59 INFO root gmswan gmswan stop successfully
# 2021-04-17^13:57:43 INFO root session accepted login on /admin/my_certificate_management/my_container for root from 172.16.1.50
# """
#     data = {'serial': 'T1111011021300201', 'type': 'log', 'log_index': 23, 'log_name_len': 8, 'log_name': 'web.log', 'log_len': 63, 'log': content, 'path': '/root/uspm-platform/protocol_implementation/log/web.log'}
#     del data["type"]
#     log_content = data.get("log")
#     data["log_path"] = data.pop("path")
#
#     content = log_content.strip()
#     content_list = content.split("\n")  # 可能会有多条日志换行上来
#     for i in content_list:
#         i_list = i.split(" ", 3)
#         if len(i_list) < 4:
#             continue
#         if not i_list[3].strip('\00'):
#             continue
#         if not i_list[3].strip():
#             continue
#         if not i_list[0].strip():
#             continue
#         if not i_list[1].strip():
#             continue
#         if not i_list[2].strip():
#             continue
#         # if "" in i_list[:-1]:
#         #     continue
#         try:
#             data["log_time"] = i_list[0]
#             data["log_type"] = i_list[1]
#             data["log_user"] = i_list[2]
#             data["short_log"] = i_list[3]
#             print(1)
#         except Exception as e:
#             print("--------解析socket端发送的log内容时出错---------", e)
#             continue
        #
        # try:
        #     models.TerminalLog.objects.create(**data)
        # except Exception as e:
        #     print("---------log入库失败----------", e)

    # client = redis.StrictRedis(host='127.0.0.1', port=6379, db=3)
    # client.publish("link", "python comes1")
