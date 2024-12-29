import RPi.GPIO as GPIO
import time

class StepMotor:
    def __init__(self, motor_pins):
        self.motor_pins = motor_pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for pin in self.motor_pins:
            GPIO.setup(pin, GPIO.OUT)

        self.step_delay = 0.0017  # 控制步进电机的速度
        self.running = False     # 添加运行标志位

    def set_step(self, h1, h2, h3, h4):
        GPIO.output(self.motor_pins[0], h1)
        GPIO.output(self.motor_pins[1], h2)
        GPIO.output(self.motor_pins[2], h3)
        GPIO.output(self.motor_pins[3], h4)

    def step_motor(self):
        SEQUENCE = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1],
        ]

        self.running = True  # 设置运行状态
        while self.running:
            for step in SEQUENCE:
                if not self.running:  # 检查标志位，及时退出
                    break
                self.set_step(*step)
                time.sleep(self.step_delay)

    def stop_motor(self):
        self.running = False  # 设置停止状态
        self.set_step(0, 0, 0, 0)

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    motor_pins = [5, 6, 13, 19]  # 控制步进电机的引脚配置
    motor_controller = StepMotor(motor_pins)
    motor_controller.step_motor()
