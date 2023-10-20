#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import smbus
from time import sleep
import math
import datetime
import json
import requests
from decimal import Decimal, ROUND_HALF_UP

def get_temperature_and_humidity():

    i2c = smbus.SMBus(1)
    address = 0x38

    trigger = [0xAC, 0x33, 0x00]

    dat = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    #初期チェック
    sleep(0.1)
    ret = i2c.read_byte_data(address, 0x71)

    if ret != 0x18:
        exit

    try:
        #測定開始
        sleep(0.01)
        i2c.write_i2c_block_data(address, 0x00, trigger)
        
        #データ読み取り
        sleep(0.08)
        dat = i2c.read_i2c_block_data(address, 0x00, 7)
        
        #データ格納
        hum = dat[1] << 12 | dat[2] << 4 | ((dat[3] & 0xF0) >> 4)
        tmp = ((dat[3] & 0x0F) << 16) | dat[4] << 8 | dat[5]
      
        #温度変換
        tmp = tmp / 2**20 * 200 - 50
        tmp = Decimal(str(tmp)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        
        #湿度変換  
        hum = hum / 2**20 * 100
        hum = Decimal(str(hum)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

        #print("Temperature: " + str(tmp) + "℃"")
        #print("Humidity: " + str(hum) + "％")
        
        #sleep(2) 

        #日時
        dt = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        return dt, tmp, hum

    except KeyboardInterrupt:
        raise


def main(argv):

    parser = argparse.ArgumentParser(description='リビングの温度を2秒間隔で確認します')
    parser.add_argument('--post', action='store_true', help='サーバに送信せずに温度をサーバに送信します')
    args = parser.parse_args()

    url = 'https://script.google.com/macros/s/AKfycbyysZpjmerkPeSYuWibTE-oAP9DLtW6nDIEQ9jJT8k5Nq4Q6M-gx5mjfPnOs64VA3Fw/exec';
    headers = {"Content-Type": "application/json"}

    try:
        while(True):

            timestamp, temperature, humidity = get_temperature_and_humidity()

            print ('%s   Temperature : %.1f℃     Humidity : %d％'%(timestamp,temperature,humidity))
            
            sendData = {
                "timestamp":timestamp,
                "temperature":temperature,
                "humidity":humidity
                }

            if args.post:
                r = requests.post(url,data=json.dumps(sendData,default=str))
                print(r.text)
                break

            sleep(2)

    except KeyboardInterrupt:
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
