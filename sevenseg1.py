#必要なモジュールをインポート
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys
import argparse

#ポート番号の定義
#7セグで使用するポートをまとめて定義
seg_pin = [
 #A(7), B(6), C(4), D(2), E(1), F(9), G(10), DP(5)
    16,   20,   13,   27,   17,   18,    23,   19] #変数"seg_pin"にリストを格納
 #左下 E(1), D(2), GND, C(4), DP(5), B(6), A(7), GND, F(9), G(10) 左上(反時計回り)
 #       17,   27,        13,    19,   20,   16,        18,   23]

#7セグで各数字を表示するためのポート
seg_1 = [
 #B(6), C(4)
    20,   13]

seg_2 = [
 #A(7), B(6),  D(2), E(1),  G(10)
    16,   20,    27,   17,     23]

seg_3 = [
  #A, B,  C,  D,  G,
  16, 20, 13, 27, 23]

seg_4 = [
 # B(6), C(4), F(9), G(10)
     20,   13,   18,    23]

seg_5 = [
 #A(7), C(4), D(2), F(9), G(10)
    16,   13,   27,   18,    23]

seg_6 = [
 #A(7), C(4), D(2), E(1), F(9), G(10)
    16,   13,   27,   17,   18,    23]

seg_7 = [
 #A(7), B(6), C(4)
    16,   20,   13]

seg_8 = [
 #A(7), B(6), C(4), D(2), E(1), F(9), G(10)
    16,   20,   13,   27,   17,   18,    23]

seg_9 = [
 #A(7), B(6), C(4),  D(2), F(9), G(10)
    16,   20,   13,   27,    18,    23]

seg_0 = [
 #A(7), B(6), C(4), D(2), E(1), F(9)
    16,   20,   13,   27,   17,   18]

seg_dp = [
 #DP()
    19]

num_seg = { '1':seg_1,
            '2':seg_2, 
            '3':seg_3, 
            '4':seg_4, 
            '5':seg_5, 
            '6':seg_6, 
            '7':seg_7, 
            '8':seg_8, 
            '9':seg_9, 
            '0':seg_0,
            'dp':seg_dp }

def ledOn(seg, sec):

   #GPIOの電圧を制御
   GPIO.output(seg, GPIO.LOW)      #GPIOの出力をlow(0v)にする
   time.sleep(sec)                 #sec秒間待つ
   GPIO.output(seg, GPIO.HIGH)     #GPIOの出力をhigh(3.3v)にする


def main(argv):

    #コマンドライン引数の設定       
    parser = argparse.ArgumentParser(description='7セグメントledの点灯表示。1〜9,0,小数点を順番に点灯します。')
    parser.add_argument('-n', help='指定した数字のみ表示します。')
    parser.add_argument('-c','--check','-t', '--test',  action='store_true', help='各セグメントを順番にすべて点灯します。')
    args = parser.parse_args()

    #GPIOの設定
    GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.bcm"に設定
    GPIO.setup(seg_pin, GPIO.OUT)       #GPIO(8ヶ)を出力モードに設定

    if args.check:
        for seg in seg_pin:
            ledOn(seg, 0.5)

    elif args.n in num_seg:
        seg = num_seg[args.n]
        ledOn(seg, 1.5)

    else:
        for seg in [seg_1, seg_2, seg_3, seg_4, seg_5, seg_6, seg_7, seg_8, seg_9, seg_0, seg_dp]:
            ledOn(seg, 0.5)

    #GPIOをクリーンアップ
    GPIO.cleanup()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
