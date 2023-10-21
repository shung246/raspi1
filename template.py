#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from gpiozero import MCP3204
from time import sleep
import datetime
import math
import json
import requests
from decimal import Decimal, ROUND_HALF_UP

def main(argv):

    parser = argparse.ArgumentParser(description='リビングの温度をサーバに送信します')
    parser.add_argument('--nopost', action='store_true', help='サーバに送信せずに温度を2秒間隔で確認します')
    args = parser.parse_args()

    try:
        while(True):


            if not args.nopost:
                r = requests.post(url,data=json.dumps(sendData,default=str))
                print(r.text)
                break

            sleep(2)

    except KeyboardInterrupt:
        #GPIO.cleanup()
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
