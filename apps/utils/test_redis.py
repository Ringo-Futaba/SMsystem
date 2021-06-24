import os
import sys
import json
from django_redis import get_redis_connection

# 模拟socket端

class SocketService:
    def __init__(self):
        sys.path.extend([os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))])  # 项目根路径
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SMsystem.settings")

        con = get_redis_connection("default")
        p = con.pubsub()
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
                print("正在验证数据")
                print("终端->" + w_data["t_id"] + "正在进行注册...")
                print("注册结果")
                # 成功code返回1, 失败返回0
                s_data = {"type": "register_result",
                          "code": 1,
                          "t_id": w_data["t_id"],
                          "t_data": "设备信息",
                          "socket_code": w_data["socket_code"]
                          }
                s_data = json.dumps(s_data)
                # 返回注册成功的消息给web_service
                con.publish("socket_service", s_data)


if __name__ == '__main__':
    # t = SocketService()
    from docx import Document
    doc = Document(r"C:\Users\user\PycharmProjects\SMsystem\media\base.docx")
    t = doc.tables[0]
    print(t)
    print(doc)
    # client = redis.StrictRedis(host='127.0.0.1', port=6379, db=3)
    # client.publish("link", "python comes1")
