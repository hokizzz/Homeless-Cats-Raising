
import RPi.GPIO as GPIO
import time

class Hx711():
    def setup(self):
        self.SCK = 17  # BCM 引脚 17，时钟
        self.DT = 27  # BCM 引脚 27，数据
        self.flag = 1  # 用于首次读数校准
        self.initweight = 0  # 毛皮
        self.weight = 0  # 测重
        self.delay = 0.09  # 延迟时间
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by BCM 编码
        GPIO.setup(self.SCK, GPIO.OUT)  # Set pin's mode is output
        GPIO.setup(self.DT, GPIO.IN)
        GPIO.setup(self.DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start(self):
        GPIO.output(self.SCK, 0)
        if GPIO.input(self.SCK):
            time.sleep(self.delay)
        value = 0
        while GPIO.input(self.DT):
            time.sleep(self.delay)
        
        for i in range(24):
            GPIO.output(self.SCK, 1)
            if (0 == GPIO.input(self.SCK)):
                time.sleep(self.delay)
            value = value << 1  # 左移一位，相当于乘2，二进制转十进制
            GPIO.output(self.SCK, 0)
            if GPIO.input(self.SCK):
                time.sleep(self.delay)
            if GPIO.input(self.DT) == 1:
                value += 1
        GPIO.output(self.SCK, 1)
        GPIO.output(self.SCK, 0)
        value = int(value / 460)  # 根据传感器特性值调整
        if self.flag == 1:  # 第一次读数为毛皮
            self.flag = 0
            self.initweight = value  # 初始值
        else:
            self.weight = abs(value - self.initweight)  # 当前值减毛皮得测量到的重量

if __name__ == '__main__':
    send = Hx711()
    send.setup()
    while True:
        send.start()
        print(send.weight)

