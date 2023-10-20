#!/usr/bin/env python

import sys
from time import sleep
sys.dont_write_bytecode = True

import argparse
from thermo_gpiozero import get_temperature_and_brightness
from sevenseg4 import display_number_to_7seg

def main(argv):

    parser = argparse.ArgumentParser(description='リビングの温度を7セグLEDに表示します')
    parser.add_argument('-s', help='指定した秒数の間表示します')
    args = parser.parse_args()

    if args.s:
        seconds = float(args.s)
    else:
        seconds = 2

    try:
        #while(True):
            timestamp, temperature, brightness = get_temperature_and_brightness()
            display_number_to_7seg(str(temperature), seconds)

    except KeyboardInterrupt:
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
