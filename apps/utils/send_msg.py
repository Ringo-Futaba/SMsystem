"""
脚本作用：

由于圈志校友的一个乒乓球活动由于报名人数太少临时取消 需要以官方短信的形式通知已报名人员 故写此脚本

"""
import json


class SendMsg:

    def __init__(self):
        self.SMS_VERIFY_CODE_LENGHT = 4
        self.SMS_VERIFY_CODE_HOST = "http://smssh1.253.com"
        self.SMS_VERIFY_CODE_ACCOUNT = 'N4957387'
        self.SMS_VERIFY_CODE_ACCOUNT_PWD = 'zUvte7hiy'
        self.SMS_VERIFY_CODE_URI = '/msg/send/json'
        self.SMS_VERIFY_CODE_VARIABLE_URI = '/msg/variable/json'


    def grounp_send(self, phone_list:list):
        for i in phone_list:
            if type(i) != str:
                continue
            if not i.isdigit():
                continue
            data = {"content": "【圈志校友】您报名的“全企健身 携手共进”乒乓球比赛，因临时有活动，本周乒乓球赛延迟，具体比赛时间待通知，感谢您的支持，谢谢！", "phone": i}
            self.send_general_message(data)

    def send_general_message(self, data1):
        """发送普通短信(调第三方)
        data1 = {'content': content1, 'phone': instance.user.phone}

        """
        print("短信发送参数===>: ", data1)
        content = data1.get('content', ' ')
        phone = data1.get('phone', -1)
        from requests import post
        url = self.SMS_VERIFY_CODE_HOST + self.SMS_VERIFY_CODE_URI
        data = json.dumps({
            'account': self.SMS_VERIFY_CODE_ACCOUNT,
            'password': self.SMS_VERIFY_CODE_ACCOUNT_PWD,
            'msg': content,
            'phone': '{phone}'.format(phone=phone),
            'report': 'false',
        })
        print("url====>: ", url, "<===== data ====>: ", data)
        send_status = post(url, data=data)
        print("send_status: ====> ", send_status)
        print("send_status.text: ====> ", send_status.text)
        return send_status.text


if __name__ == "__main__":
    s = SendMsg()
    phone_list = ["18305964321", "15806090359", "13372722592", "13950438966", "13705962806", "18850351521", "13601266488"]
    s.grounp_send(phone_list)