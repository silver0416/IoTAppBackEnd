from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client  # import 套件
import database


account_sid = "sid"  # 請填寫剛剛紀錄的 ACCOUNT SID

auth_token = "token"  # 請填寫剛剛紀錄的 AUTH TOKEN

service_sid = 's_sid'

# 建立 client instance
client = Client(account_sid, auth_token)

phone_number = '+886'  # 請填寫收驗證碼的手機號碼
client.verify.services(service_sid).verifications.create(to=phone_number, channel='sms')


# # handle twilio 可能引發的 exceptions
# phone_number = '+886xxxxxxxxx'
# verification_code = 'xxxxxx'  # 長度根據 service setting 的 CODE LENGTH
# try:
#     client.verify \
#           .services(service_sid) \
#           .verification_checks \
#           .create(to=phone_number, code=verification_code)
# # 核對無誤則不會發生 exception
# # service_sid 請填寫剛剛紀錄的 SERVICE_SID
# except TwilioRestException as e:
#     pass  # do something...
