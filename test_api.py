from api_helper import ShoonyaApiPy
import logging
 
#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
api = ShoonyaApiPy()

#credentials
user    = 'FA27007'
pwd     = '117@Asmita'
factor2 = 'CQNPK6666B'
vc      = 'FA27007_U'
app_key = '567fc7c2406aa17c1ddc65e22ed5d823'
imei    = 'abc123'

#make the api call
ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
print(ret)
ret = api.get_option_chain('NFO','NIFTY20JAN22C18500',18000,10)
ret = api.get_quotes('NFO','48702')
ret = api.searchscrip('NFO', 'Nifty 20Jan CE 18400')
ret = api.get_positions()
ret = api.get_order_book()
print(ret)
ret = api.exit_order('22011800204296',"M")


print(ret)

