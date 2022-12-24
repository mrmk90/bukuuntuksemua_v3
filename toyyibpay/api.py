import requests

'''
Rujukan: https://toyyibpay.com/apireference/
'''


class ToyyibPay:
    SECRET_KEY = '7sjb0jk5-3udm-yi8b-qalr-cf77wbepu23z'
    ROOT_URL = 'https://toyyibpay.com/'
    CATEGORY_CODE = 'rqwpdrns'

    BILL_RETURN_URL = 'https://mart.boca.my/payment-result'
    BILL_CALLBACK_URL = 'https://mart.boca.my/payment-callback'

    def create_bill(self, data):
        # Add Data
        data['userSecretKey'] = self.SECRET_KEY
        data['categoryCode'] = self.CATEGORY_CODE
        data['billReturnUrl'] = self.BILL_RETURN_URL
        data['billCallbackUrl'] = self.BILL_CALLBACK_URL
        url = self.ROOT_URL + 'index.php/api/createBill'
        r = requests.post(url=url, data=data)

        # TODO: r.status_code checking
        return r.json()[0]

    def get_bank(self):
        r = requests.get(url=self.ROOT_URL + 'index.php/api/getBank')
        print(r.json())

    def get_bank_fpx(self):
        r = requests.get(url=self.ROOT_URL + 'index.php/api/getBankFPX')
        print(r.json())

    def get_package(self):
        r = requests.get(url=self.ROOT_URL + 'index.php/api/getPackage')
        print(r.json())

    def get_all_user(self):
        data = {
            'userSecretKey': self.SECRET_KEY,
            'partnerType': 'OEM'
        }
        r = requests.post(url=self.ROOT_URL + 'admin/api/getAllUser', data=data)
        print(r.json())

    def get_category_code(self):
        data = {
            'userSecretKey': self.SECRET_KEY,
            'categoryCode': 'rqwpdrns'
        }
        r = requests.post(url=self.ROOT_URL + 'index.php/api/getCategoryDetails', data=data)
        print(r.json())
