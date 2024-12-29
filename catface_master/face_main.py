
import copy
import threading
import datetime
import time
import cv2
import os
from image import *
from test_face import *
from PH_711 import *
from uln2003 import StepMotor


class Cat_Face:
    def __init__(self):
        self.img = None
        self.weight = 0
        self.category = 'None'
        self.category_weight = 0
        self.flage = 0
        self.lebel = False
        self.Detecting_cats = True
        self.Detecting_face = False
        self.weight_last = 0
        self.face_time = time.time()
        self.weight_add_flag = True
        self.add_flag = True
        self.Detecting_face_count = 0

        # 初始化猫脸检测器和步进电机
        face_cascade_path = '/home/msi-nb/catface-master/data/haarcascades/haarcascade_frontalcatface_extended.xml'
        photos_path = '/home/msi-nb/catface-master/data/photos'
        self.comparer = ImageComparer(photos_path, face_cascade_path)

        self.cap = cv2.VideoCapture(0)  # 0表示默认摄像头

        model_pb_path = "v5lite-cat.onnx"
        so = ort.SessionOptions()
        self.net = ort.InferenceSession(model_pb_path, so)

        self.motor_pins = [5, 6, 13, 19]  # 定义步进电机的控制引脚
        self.step_motor = StepMotor(self.motor_pins)  # 创建步进电机实例

        self.send = Hx711()
        self.send.setup()  # 初始化HX711传感器

    def add_cat(self, img, label):
        self.add_flag = False

        # 启动步进电机
        print("Starting the stepper motor")
        # self.step_motor.step_motor()
        recognition_thread = threading.Thread(target=self.step_motor.step_motor)
        recognition_thread.start()

        # 使用HX711传感器实时读取重量，并根据重量判断是否停止电机
        weight_readings = []
        while True:
            try:
                self.send.start()           
                self.weight = self.send.weight  # 实时获取重量
                weight_readings.append(self.weight)
                print(self.weight)

                if len(weight_readings) > 10:
                    weight_readings.pop(0)  # 保持最近10次的重量数据
                    average_weight = sum(weight_readings) / len(weight_readings)

                    print(f"Average Weight = {average_weight}g")

                    if average_weight > 200:
                        print("Weight exceeded 200g, stopping motor.")
                        self.step_motor.stop_motor()  # 停止步进电机
                        break
                    else:
                        print("Weight below 200g, continuing monitoring...")

            except Exception as e:
                print(f"Debug Error: {e}")

            time.sleep(0.1)  # 添加延迟，防止过快循环
            
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        name_jpg = current_time + '_' + label + '_' + str(self.weight) + '.jpg'
        # 图像名称：时间_猫名_重量
        path = os.path.join('/home/msi-nb/catface-master/recognition_result', name_jpg)
        img = cv2.resize(img, [320, 320], interpolation=cv2.INTER_AREA)
        cv2.imwrite(path, img)
        # 添加猫信息
        print(f"Cat with label {label} added.")
        self.add_flag = True

    def receiveFrame(self):
        while True:
            ret, img = self.cap.read()
            if ret:
                self.flage += 1
                if self.Detecting_cats and self.flage > 10:
                    img0 = copy.copy(img)
                    flag_face = image_detection(img0, self.net)
                    self.flage = 0
                    if flag_face:
                        self.Detecting_face = True
                        self.Detecting_cats = False
                        # 检测到猫
                 
                elif self.Detecting_face and self.comparer.run_flage:
                    img1 = copy.copy(img)
                    self.Detecting_face_count += 1
                    recognition_thread = threading.Thread(target=self.comparer.run_face, args=(img1,))
                    recognition_thread.start()

                if self.Detecting_face_count == 100:
                    self.comparer.detection_name = 'other'
                    # 识别猫脸

                if self.comparer.detection_name is not None and self.add_flag:
                    self.Detecting_face_count = 0
                    self.Detecting_face = False
                    self.face_time = time.time()
                    rec_thread = threading.Thread(target=self.add_cat, args=(img1, self.comparer.detection_name))
                    rec_thread.start()
                    self.comparer.detection_name = None
                    # 开启电机和压感器

                if int(time.time() - self.face_time) > 200 and not self.Detecting_face:
                    self.Detecting_face = False
                    self.Detecting_cats = True
                    self.face_time = time.time()
                    # 200秒内不重复添加

            img = cv2.resize(img, [640, 640], interpolation=cv2.INTER_AREA)
            cv2.imshow('Result', img)
            if ord(' ') == cv2.waitKey(10):
                break


if __name__ == "__main__":
    Face = Cat_Face()
    recognition_thread = threading.Thread(target=Face.receiveFrame)
    recognition_thread.start()
