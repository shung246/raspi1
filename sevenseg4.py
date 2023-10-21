#!/usr/bin/env python

import sys
import argparse
import RPi.GPIO as GPIO
import time             # timeライブラリの読み込み
import spidev           # spidevライブラリの読み込み

#MSB first(Q7->Q0) / 1で点灯(カソードコモン)
segM1 = [
        0x3f,   #0
        0x06,   #1
        0x5b,   #2
        0x4f,   #3
        0x66,   #4
        0x6d,   #5
        0x7d,   #6
        0x07,   #7
        0x7f,   #8
        0x6f,   #9
        0x00    #empty
        ]

segM0h = [0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0x88,0x83,0xc6,0xa1,0x86,0x8e]

#MSB first(Q7->Q0 : DP->A) / 0で点灯(アノードコモン)
segM0 = {
        '0':0xc0,   #0
        '1':0xf9,   #1
        '2':0xa4,   #2
        '3':0xb0,   #3
        '4':0x99,   #4
        '5':0x92,   #5
        '6':0x82,   #6
        '7':0xf8,   #7
        '8':0x80,   #8
        '9':0x90,   #9
        ' ':0xff,   #empty
        '-':0xbf,   #-
        'H':0x89    #H (humidity用)
        }

digit1 = 21           # digit 1の制御ピン
digit2 = 20           # digit 2の制御ピン
digit3 = 16           # digit 3の制御ピン
digit4 = 12           # digit 4の制御ピン
delay = 0.0015        # 7seg ledのアクティブ時間

def get_number_wo_dp(number):
    return number.replace('.','')

def get_number_list(number):

    dp = number.find('.')
    if dp != -1:
        dp = len(number) - dp - 1

    number2 = list(number.replace('.','').rjust(4))

    if dp == 3:
        num1 = segM0[number2[-4]] & 0x7F #小数点をつける
    else:
        num1 = segM0[number2[-4]]
    if dp == 2:
        num2 = segM0[number2[-3]] & 0x7F #小数点をつける
    else:
        num2 = segM0[number2[-3]]
    if dp == 1:
        num3 = segM0[number2[-2]] & 0x7F #小数点をつける
    else:
        num3 = segM0[number2[-2]]
    num4 = segM0[number2[-1]]
 
    return num1, num2, num3, num4


def display_number_to_7seg(number, seconds=0):

    num1, num2, num3, num4 = get_number_list(number)

    spi = spidev.SpiDev()     # spidevのインスタンス化

    spi.open(0,0)             # CE0を指定
    spi.max_speed_hz = 500000 # 転送速度を500kHzに設定
    spi.mode = 0b00           # SPIモード0

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(digit1, GPIO.OUT)
    GPIO.setup(digit2, GPIO.OUT)
    GPIO.setup(digit3, GPIO.OUT)
    GPIO.setup(digit4, GPIO.OUT)

    try:
        start_time = time.time()

        while True:
            GPIO.output(digit1, 1)  # digit1をHIGH
            spi.xfer([num1])        # 7セグLEDの全消灯
            time.sleep(delay)       # digit1のアクティブ時間の生成
            spi.xfer2([0xFF])       # 7セグLEDの全消灯
            GPIO.output(digit1, 0)  # digit1をLOW

            GPIO.output(digit2, 1)  # digit2をHIGH
            spi.xfer([num2])        # 数字の2に対応するデータの送出
            time.sleep(delay)       # digit2のアクティブ期間の生成
            spi.xfer2([0xFF])       # 7セグLEDの全消灯
            GPIO.output(digit2, 0)  # digit2をLOW

            GPIO.output(digit3, 1)  # digit3をHIGH
            spi.xfer([num3])        # 数字の3に対応するデータの送出
            time.sleep(delay)       # digit3のアクティブ時間の生成
            spi.xfer2([0xFF])       # 7セグLEDの全消灯
            GPIO.output(digit3, 0)  # digit3をLOW

            GPIO.output(digit4, 1)  # digit4をHIGH
            spi.xfer([num4])        # 数字の4に対応するデータの送出
            time.sleep(delay)       # digit4のアクティブ時間の生成
            spi.xfer2([0xFF])       # 7セグLEDの全消灯
            GPIO.output(digit4, 0)  # digit4をLOW

            if (seconds != 0) and (time.time() - start_time > seconds):
                break

    except KeyboardInterrupt:
        spi.close()             # SPI通信を終了
        GPIO.cleanup()
        raise

    spi.close()             # SPI通信を終了
    GPIO.cleanup()


def main(argv):

    parser = argparse.ArgumentParser(description='LEDに数値を表示します')
    parser.add_argument('-n', help='指定した数値を表示します')
    parser.add_argument('-s', help='指定した秒数の間表示します')
    args = parser.parse_args()

    if args.n:
        number = args.n
        if len(get_number_wo_dp(args.n)) > 4:
            print('4桁以下の数字を入力してください。処理を中断します。')
            return
    else:
        number = '8765'
    
    if args.s:
        seconds = float(args.s)
    else:
        seconds = 0

    try:
        display_number_to_7seg(number, seconds)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    sys.exit(main(sys.argv))
