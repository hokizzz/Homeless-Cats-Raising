
import cv2
import numpy as np
import os
import json
import time


class ImageComparer:
    def __init__(self, folder_path, face_cascade_path):
        self.folder_path = folder_path
        self.feature_data_file = "features_data.json"
        # 读取猫脸检测的分类器
        self.face_detector = cv2.CascadeClassifier(face_cascade_path)
        self.features_data = {}

        # 如果features_data.json存在，加载特征描述子
        if os.path.exists(self.feature_data_file):
            with open(self.feature_data_file, 'r') as f:
                self.features_data = json.load(f)
        # print(self.features_data)
        self.names = {}
        self.load_names()
        self.detection_name = None
        self.run_flage = True

    def load_names(self):
        """Load names from the photos directory."""
        image_paths = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path)]
        for image_path in image_paths:
            name = str(os.path.split(image_path)[1].split('.', 2)[1])
            self.names[image_path.split('/')[-1]] = name

    # 使用ORB检测图像的特征点和描述子
    def detect_orb_features(self, image):
        # image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create()  # 创建ORB检测器
        keypoints, descriptors = orb.detectAndCompute(gray, None)  # 检测特征点并计算描述子
        return keypoints, descriptors

    # 将特征描述子保存到JSON文件
    def save_features_to_json(self, image_name, descriptors):
        if descriptors is not None:
            # 保存描述子到字典
            descriptors_list = descriptors.tolist()  # 转为可JSON序列化的格式
            self.features_data[image_name] = descriptors_list
            # 保存到JSON文件
            with open(self.feature_data_file, 'w') as f:
                json.dump(self.features_data, f)

    # 比较两张图像的ORB特征匹配
    def compare_orb_features(self, descriptors1, descriptors2):
        # 创建BFMatcher对象，使用汉明距离进行匹配
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        matches = sorted(matches, key=lambda x: x.distance)  # 按匹配距离排序
        return matches

    # 主函数：比对目标图像与文件夹中的所有图像
    def compare_images_with_orb(self, image):
        # target_image_path = 'catface.jpg'
        # 先检测目标图像的ORB特征
        target_keypoints, target_descriptors = self.detect_orb_features(image)
        similarities = []
        # 遍历文件夹中的每一张图片，加载并比较特征
        for image_name in os.listdir(self.folder_path):
            image_path = os.path.join(self.folder_path, image_name)
            if os.path.isfile(image_path):
                # 如果特征已经计算过，直接加载
                if image_name in self.features_data:
                    descriptors = np.uint8(self.features_data[image_name])
                else:
                    # 否则重新计算特征
                    image = cv2.imread(image_path)
                    keypoints, descriptors = self.detect_orb_features(image)
                    if descriptors is not None:
                        self.save_features_to_json(image_name, descriptors)
                if descriptors is not None:
                    matches = self.compare_orb_features(target_descriptors, descriptors)
                    similarity = len(matches)  # 匹配数作为相似度度量
                    similarities.append((image_name, similarity))
        # 按匹配数排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        for image_name, similarity in similarities:
            print(f"图像: {image_name}, 相似度（匹配数）: {similarity}")
            if similarity > 16:
                self.detection_name = self.names[image_name]
                break
        #         return True, self.names[image_name]
        # return False, None

    def cut_off_cat_face(self, img):
        # 将图片转换为灰度图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 检测猫脸
        faces = self.face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        # 如果检测到猫脸
        if len(faces) > 0:
            for i, (x, y, w, h) in enumerate(faces):
                # 截取猫脸区域
                cat_face = img[y:y + h, x:x + w]
                return True, cat_face
        else:
            print('未检测到猫脸')
            return False, img
    def run_face(self, img):
        self.run_flage = False
        flage, image = self.cut_off_cat_face(img)
        if flage:
            self.compare_images_with_orb(image)
            print(self.detection_name)
        self.run_flage = True
    
if __name__ == "__main__":
    target_image = "/home/msi-nb/catface-master/catface1/Orange.jpg"  # 目标图像路径
    face_cascade_path = "/home/msi-nb/catface-master/data/haarcascades/haarcascade_frontalcatface_extended.xml"
    photos_path = "/home/msi-nb/catface-master/data/photos/"
    comparer = ImageComparer(photos_path, face_cascade_path)
    img = cv2.imread(target_image)
    comparer.run_face(img)
