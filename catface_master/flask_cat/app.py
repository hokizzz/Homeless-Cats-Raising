import cv2
import numpy as np
from flask import Flask, render_template, request
from flask import send_from_directory, make_response,g
import base64
from utils.pagination import Pagination
from utils.read_image import get_image_info, dataframe_to_dict_list

app = Flask(__name__)
last_cats = 0
new_records_flag = False


@app.route('/')
def index():
    global last_cats, new_records_flag
    # Connect to the database
    # 示例用法
    directory = '/home/msi-nb/catface-master/recognition_result'  # 替换为你的文件夹路径

    # 获取图像信息和统计 `name=other` 的数量
    df_images, other_count = get_image_info(directory)

    # 将 Pandas DataFrame 转换为字典列表
    image_dict_list = dataframe_to_dict_list(df_images)[::-1]
    if last_cats == 0:
        last_cats = other_count
        new_records_flag = False
    elif last_cats < other_count:
        last_cats = other_count
        new_records_flag = True
    else:
        new_records_flag = False

    # Initialize pagination
    page_object = Pagination(request, image_dict_list)
    detected = []

    # Process each data item in the paginated queryset
    i = 1
    for data in page_object.page_queryset:
        # detected_image = data['data']
        # # # 如果detected_image不是bytes对象，将其转换为bytes对象
        # if not isinstance(detected_image, bytes):
        #     detected_image = detected_image.getvalue()
        # # 解码 base64 图像数据
        # img_data = base64.b64decode(detected_image)  # 假设 img 是 base64 编码的字符串
        # # 使用 numpy 将字节数据转换为数组
        # nparr = np.frombuffer(img_data, np.uint8)
        # # 使用 OpenCV 解码图像
        # img_decoded = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # _, buffer = cv2.imencode('.jpg', img_decoded)
        # image = base64.b64encode(buffer).decode('utf-8')
        # # # 检查图像是否为空
        # # if img_decoded is None or img_decoded.size == 0:
        # #     print("Error: Image is empty or invalid.")
        # # else:
        # #     # 保存图像
        # #     cv2.imwrite(f'cropped_image{i}.jpg', img_decoded)
        detected.append({
            'id': data['id'],
            'name': data['name'],
            'weight': data['weight'],
            'detected_image': data['data'],
            'location': '',
            'detection_time': data['time']
        })
    # Render the template with detected data and pagination
    return render_template('detected_data.html', detected=detected,
                           page_string=page_object.html(), new_records=new_records_flag)

@app.route('/static/<path:filename>')
def send_static_file(filename):
    response = make_response(send_from_directory('static', filename))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(host='172.20.10.5')
