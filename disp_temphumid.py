#!/usr/bin/env python

import sys
from time import sleep
sys.dont_write_bytecode = True

import argparse
import json
import requests
from thermo_dht20 import get_temperature_and_humidity
from sevenseg4 import display_number_to_7seg

def main(argv):

    parser = argparse.ArgumentParser(description='リビングの温度と湿度を7セグLEDに表示します')
    parser.add_argument('-s', help='温度と湿度をそれぞれ指定した秒数の間表示します')
    parser.add_argument('--post', action='store_true', help='温度情報をサーバに送信します')
    args = parser.parse_args()

    url = 'https://script.google.com/macros/s/AKfycbyysZpjmerkPeSYuWibTE-oAP9DLtW6nDIEQ9jJT8k5Nq4Q6M-gx5mjfPnOs64VA3Fw/exec';
    headers = {"Content-Type": "application/json"}

    if args.s:
        seconds = float(args.s)
    else:
        seconds = 2

    try:
        #while True:
            timestamp, temperature, humidity = get_temperature_and_humidity()
            display_number_to_7seg(str(temperature), seconds)
            display_number_to_7seg(str(humidity), seconds)

            if args.post:
                sendData = {
                    "timestamp":timestamp,
                    "temperature":temperature,
                    "humidity":humidity
                    }
                r = requests.post(url,data=json.dumps(sendData,default=str))
                print(r.text)
                #break

            #sleep(2)
    except KeyboardInterrupt:
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
