# Final Project

## 一、项目介绍：

这是一个集成了自动猫粮投喂、校园流浪猫识别与健康信息提示的简单的校园流浪猫管理系统，并且志工们可以通过网页进行猫咪图像与流浪状况的查询。

## 二、技术路线图：

![image](https://github.com/hokizzz/Homeless-Cats-Raising/blob/main/technical%20route.png)

## 三、环境搭建：

### （一）硬体组件

1\.Raspberry Pi 4B

2\.Pi Camera Rev 1.3

3\.Arduino ULN2003 Driver

4\.28BYJ-48 Stepper Motor

5\.HX711 load cell

### （二）软件环境

1\.Raspberry Os

2\.OpenCV 4.5.2

3\.Python 3.7.3

4\.ONNX Runtime 1.5.3

### （三）如何搭建

1\.软件环境

（1）Raspberry OS和OpenCV 4.5.2 

<https://blog.csdn.net/qq_51189182/article/details/129490325>

（2）ONNX Runtime 1.5.3

<https://blog.csdn.net/2402_83140078/article/details/139634182?spm=1001.2014.3001.5502>

2\.硬体组件

（1）Pi Camera Rev 1.3

<https://picamera.readthedocs.io/en/release-1.13/quickstart.html>

（2）Arduino ULN2003 Driver和28BYJ-48 Stepper Motor

<https://blog.csdn.net/m0_52909281/article/details/123149339>

![image](https://github.com/hokizzz/Homeless-Cats-Raising/blob/main/uln2003%20driver.jpg)

使用BCM编码

IN1 to PIN5   

IN2 to PIN6

IN3 to PIN13

IN4 to PIN19

（3）HX711 load cell

<https://blog.csdn.net/weixin_47082836/article/details/113199129?spm=1001.2014.3001.5502>

![image](https://github.com/hokizzz/Homeless-Cats-Raising/blob/main/hx711.jpg)

使用BCM编码:

DT to PIN27

SDK to PIN17

（4）外观制作

<https://www.bilibili.com/video/BV1Lw4m1k7vf/?spm_id_from=333.999.0.0&vd_source=8868d18b1f83107438eba5b3318225a9>

螺旋下料器：

![image](https://github.com/hokizzz/Homeless-Cats-Raising/blob/main/Spiral%20machine.jpg)

步进马达：

![image](https://github.com/hokizzz/Homeless-Cats-Raising/blob/main/StepMotor.jpg)

压力传感器：

![image](https://github.com/hokizzz/Homeless-Cats-Raising/blob/main/hx711%20module.jpg)

猫粮盒：

![image](https://github.com/hokizzz/Homeless-Cats-Raising/blob/main/Storage.jpg)

Pi Camera和Raspberry Pi：

![image](https://github.com/hokizzz/Homeless-Cats-Raising/blob/main/Pi%20Camera.jpg)

外型可以模块化生产，然后美美组装就ok了。

## 四、实际操作：

在开始之前，请把我的文件全部下载到你的Raspberry Pi中。

### （一）打开Flask网页

1\.在lx终端机上载入flask\_cat文件夹；

2\.输入
```
python3 app.py
```

3\.在浏览器中输入你的树莓派的IP地址:5000，进入网页。

### （二）运行face\_main.py

1\.在新窗口上载入你存储catface\_master文件夹的位置；

2\.输入
```
python3 face\_main.py
```

3\.在猫粮盒前展示猫脸图片；

4\.Pi Camera捕捉到猫脸信息，识别为猫咪后，步进马达开始工作，螺旋下料器旋转下料，压感器传输信息，达到阈值马达停止。

### （三）Flask网页更新

此时，你可以查看到猫咪的图片，进食情况，以及进食时间。对于识别到”other“类别的猫咪，在刷新网页之后，你会收到一份给猫咪绝育的提示。

## 五、模型训练：

这个项目使用到了yolov5-lite模型进行“是否为猫”的检测，所以你能够直接使用我的推理模型来检测是否有猫咪出没。当模型检测到猫咪存在后，系统会再进行“识别为哪知猫”的检测，你需要将你所已知的猫咪图像传输到data文件夹中的photos文件下，然后通过给予好的分类器，这样你就能够开始识别猫咪啦！

## 六、我的视频：

## 七、参考资料：

1\.Raspberry OS和OpenCV 4.5.2安装：

<https://blog.csdn.net/qq_51189182/article/details/129490325>

2\.ONNX Runtime 1.5.3下载：

<https://blog.csdn.net/2402_83140078/article/details/139634182?spm=1001.2014.3001.5502>

3\.Pi Camera Rev 1.3使用：

<https://picamera.readthedocs.io/en/release-1.13/quickstart.html>

4\.Arduino ULN2003 Driver和28BYJ-48 Stepper Motor控制：

<https://blog.csdn.net/m0_52909281/article/details/123149339>

5\.HX711 load cell控制：

<https://blog.csdn.net/weixin_47082836/article/details/113199129?spm=1001.2014.3001.5502>

6\.外形制作：

<https://www.bilibili.com/video/BV1Lw4m1k7vf/?spm_id_from=333.999.0.0&vd_source=8868d18b1f83107438eba5b3318225a9>

7\.Yolov5-Lite模型训练：

<https://sneak.blog.csdn.net/article/details/131374492?spm=1001.2014.3001.5502>

<https://blog.csdn.net/qq_52859223/article/details/123701798>

8\.猫脸识别：

<https://blog.csdn.net/qq_51118755/article/details/137698608?spm=1001.2014.3001.5502>

<https://blog.csdn.net/qq_51118755/article/details/137383678?spm=1001.2014.3001.5502>

9\.Flask网页：

<https://blog.csdn.net/huanghong6956/article/details/84967712>

<https://blog.csdn.net/weixin_43933781/article/details/139205373?spm=1001.2014.3001.5502>
