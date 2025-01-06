import schedule
import time
import datetime
from datetime import date
from api_helper import ShoonyaApiPy
import logging
import numpy as np
import pyotp

# enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

# start of our program
api = ShoonyaApiPy()

# credentials
user = 'FA33926'
pwd = 'Ankitsi101@6'
token = 'U67I4TFZO6LA66C5K56OG6ZG7YQGVH7W'

vc = 'FA33926_U'
app_key = 'aa185e6f6c985ab511ae2f462087320d'
imei = 'abc123'

def closest_value(input_list, input_value):
    arr = np.asarray(input_list)
    i = (np.abs(arr - input_value)).argmin()
    return arr[i]


def check_position():
    resp_body = api.get_positions()
    print (resp_body)
    length = len(resp_body)
    count = 0
    CEPrice = 0
    CEQty = 0
    PEPrice = 0
    PEQty = 0
    cetsym = ""
    petsym = ""
    cestrike = 0
    pestrike = 0
    while count < length:
        if (int(resp_body[count]['netqty']) < 0):
            if (("CE") in (resp_body[count]['dname'])):
                CEPrice = float(resp_body[count]['lp'])
                cetsym = (resp_body[count]['tsym'])
                cestrike = int(cetsym[-5:])
                CEQty = abs(int(resp_body[count]['netqty']))
            if (("PE") in (resp_body[count]['dname'])):
                PEPrice = float(resp_body[count]['lp'])
                petsym = (resp_body[count]['tsym'])
                pestrike = int(petsym[-5:])
                PEQty = abs(int(resp_body[count]['netqty']))
        count += 1
    if abs(float(CEPrice-PEPrice)) > float(CEPrice) and (cestrike !=pestrike):
        api.place_order(buy_or_sell='B', product_type='M',
                        exchange='NFO', tradingsymbol=cetsym,
                        quantity=CEQty, discloseqty=0, price_type='MKT', price=0,trigger_price=None,retention='DAY')
        # api.place_order(buy_or_sell='S', product_type='M',
        #                 exchange='NFO', tradingsymbol=str(cetsym.replace(str(cestrike),str(cestrike+200))),
        #                 quantity=CEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None, retention='DAY')
        i = cestrike
        cetsymblist = []
        cepricelist = []
        while i >= pestrike:
            searchtext =  cetsym.replace(cetsym[-5:], str(i))
            print("This is search ceestrike text" + searchtext )
            response = (api.searchscrip('NFO',searchtext))
            tokenID = response['values'][0]['token']
            response = api.get_quotes('NFO',tokenID)
            cetsymblist.append(response['tsym'])
            cepricelist.append(float(response['lp']))
            i -= 50
            cettradesymbol=cetsymblist[cepricelist.index(float(closest_value(cepricelist, float(PEPrice*0.80))))]
            cetradestrikeprice=int(cettradesymbol[-5:])
        api.place_order(buy_or_sell='S', product_type='M',
                        exchange='NFO', tradingsymbol=cettradesymbol,
                        quantity=CEQty, discloseqty=0, price_type='MKT', price=0,trigger_price=None,retention='DAY')
        # api.place_order(buy_or_sell='B', product_type='M',
        #                 exchange='NFO', tradingsymbol=cettradesymbol.replace(str(cetradestrikeprice),str(cetradestrikeprice+200)),
        #                 quantity=CEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None, retention='DAY')
    if abs(float(CEPrice-PEPrice)) > float(PEPrice) and (cestrike !=pestrike):
        api.place_order(buy_or_sell='B', product_type='M',
                        exchange='NFO', tradingsymbol=petsym,
                        quantity=PEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None, retention='DAY')
        # api.place_order(buy_or_sell='S', product_type='M',
        #                 exchange='NFO', tradingsymbol=cetsym.replace(str(petsym), str(petsym - 200)),
        #                 quantity=CEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None, retention='DAY')
        i = pestrike
        petsymblist = []
        pepricelist = []
        while i <= cestrike:
            searchtext = petsym.replace(petsym[-5:], str(i))
            print("This is search peestrike text" + petsym)
            response = (api.searchscrip('NFO', searchtext))
            tokenID = response['values'][0]['token']
            response = api.get_quotes('NFO', tokenID)
            petsymblist.append(response['tsym'])
            pepricelist.append(float(response['lp']))
            i += 50
        pettradesymbol = petsymblist[pepricelist.index(float(closest_value(pepricelist, float(CEPrice*0.80))))]
        petradestrikeprice = int(pettradesymbol[-5:])
        api.place_order(buy_or_sell='S', product_type='M',
                        exchange='NFO',
                        tradingsymbol=pettradesymbol,
                        quantity=PEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None, retention='DAY')
        # api.place_order(buy_or_sell='B', product_type='M',
        #                 exchange='NFO',
        #                 tradingsymbol=cettradesymbol.replace(str(petradestrikeprice), str(petradestrikeprice - 200)),
        #                 quantity=CEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None, retention='DAY')

    if abs(float(CEPrice - PEPrice)) > float(PEPrice) and (cestrike == pestrike):
        api.place_order(buy_or_sell='B', product_type='M',
                        exchange='NFO', tradingsymbol=petsym,
                        quantity=PEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                        retention='DAY')
        api.place_order(buy_or_sell='B', product_type='M',
                        exchange='NFO', tradingsymbol=cetsym,
                        quantity=CEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                        retention='DAY')
    if abs(float(CEPrice - PEPrice)) > float(CEPrice) and (cestrike == pestrike):
        api.place_order(buy_or_sell='B', product_type='M',
                        exchange='NFO', tradingsymbol=petsym,
                        quantity=PEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                        retention='DAY')
        api.place_order(buy_or_sell='B', product_type='M',
                        exchange='NFO', tradingsymbol=cetsym,
                        quantity=CEQty, discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                        retention='DAY')

def e2e():
    #Login to shoonya
    print(api.login(userid=user, password=pwd, twoFA=pyotp.TOTP(token).now(), vendor_code=vc, api_secret=app_key, imei=imei))
    check_position()


schedule.every(300).seconds.do(e2e)

while True:
    schedule.run_pending()
    time.sleep(1)
    if datetime.datetime.now().time() > datetime.datetime(2222, 5, 17, 11, 55, 00).time():
        break
