#!/usr/bin/env python

import sys
from time import sleep
sys.dont_write_bytecode = True

import argparse
import RPi.GPIO as GPIO
from thermo_dht20 import get_temperature_and_humidity
from sevenseg4 import display_number_to_7seg

def main(argv):

    parser = argparse.ArgumentParser(description='リビングの温度と湿度を7セグLEDに表示します')
    parser.add_argument('-s', help='温度と湿度をそれぞれ指定した秒数の間表示します')
    parser.add_argument('--post', action='store_true', help='温度情報をサーバに送信します')
    args = parser.parse_args()

    if args.s:
        seconds = float(args.s)
    else:
        seconds = 2

    BTN_GPIO = 26

    while True:
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(BTN_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            switchStatus = GPIO.input(BTN_GPIO)

            if switchStatus == 1:
                print('button pushed')
                timestamp, temperature, humidity = get_temperature_and_humidity()
                display_number_to_7seg(str(temperature), seconds)
                display_number_to_7seg(str(humidity), seconds)

            sleep(0.2)

        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
