import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': "祝福你{}".format(code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        import json
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == '__main__':
    yun_pian = YunPian("762780cc339432238f4b35c0cfdb7bfa")
    yun_pian.send_sms('万事如意', "15018225867")