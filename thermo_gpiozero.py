#!/usr/bin/env python

import sys
import argparse
from gpiozero import MCP3204
from time import sleep
import math
import datetime
import json
import requests
from decimal import Decimal, ROUND_HALF_UP

def get_temperature_and_brightness():

    Vref = 3.29
    K0 = 273.16
    ThermoB = 3950.0

    #class　gpiozero.MCP3204(channel=0, differential=False, max_voltage=3.3, **spi_args)
    #channel : データを読み取るチャネル
    #differntial : Trueは差分モード
    #value : デバイスから読み取られた現在の値。0〜1の値にスケーリングされる

    adc0 = MCP3204(channel=0)
    adc1 = MCP3204(channel=1)

    #気温
    sumTemp = 0
    for i in range(5):
        value = adc0.value                   # 指定したピンのAD値を読む(0〜1)
        voltage = value * Vref               # ADC値を電圧に変換
        Rt = 10 * voltage / (Vref - voltage) # サーミスタの抵抗値を計算
        tempK = 1/(1/(K0 + 25) + math.log(Rt/10)/ThermoB)  # ケルビン温度を計算
        tempC = tempK - K0                   # セルシウス温度に変換

        sumTemp += tempC
        #print(i, tempC, sumTemp)

        #sleep(2)

    #気温は5回の平均を取る
    temperature = sumTemp / 5
    temperature = Decimal(str(temperature)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

    #print ('ADC Value0 : %f, Voltage0 : %.3f, Temperature : %.1f'%(value,voltage,temperature))


    #明るさ
    value1 = adc1.value          # 指定したピンのAD値を読む(0〜1)
    voltage1 = value1 * Vref     # ADC値を電圧に変換
    brightness = value1 * 100
    brightness = Decimal(str(brightness)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

    #print ('ADC Value1 : %f, Voltage1 : %.3f, Brightnese  : %d'%(value1,voltage1,brightness))


    #日時
    dt = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    return dt, temperature, brightness


def main(argv):

    parser = argparse.ArgumentParser(description='リビングの温度を2秒間隔で確認します')
    parser.add_argument('--post', action='store_true', help='サーバに送信せずに温度をサーバに送信します')
    args = parser.parse_args()

    url = 'https://script.google.com/macros/s/AKfycbyysZpjmerkPeSYuWibTE-oAP9DLtW6nDIEQ9jJT8k5Nq4Q6M-gx5mjfPnOs64VA3Fw/exec';
    headers = {"Content-Type": "application/json"}

    try:
        while(True):

            timestamp, temperature, brightness = get_temperature_and_brightness()

            print ('%s   Temperature : %.1f℃     Brightnese : %d％'%(timestamp,temperature,brightness))
            
            sendData = {
                "timestamp":timestamp,
                "temperature":temperature,
                "brightness":brightness
                }

            if args.post:
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
