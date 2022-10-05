from flask import Flask, render_template, request
import os
from random import random
import cv2
import sys
import tkinter
from tkinter import Frame, Tk, BOTH, Text, Menu, END
from tkinter.filedialog import Open, SaveAs

import numpy as np
import os.path
import cv2
import joblib
import sys
from sklearn.svm import LinearSVC

# Khởi tạo Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static"


detector = cv2.FaceDetectorYN.create(
    "face_detection_yunet_2022mar.onnx",
    "",
    (320, 320),
    0.9,
    0.3,
    5000
)
detector.setInputSize((320, 320))

recognizer = cv2.FaceRecognizerSF.create(
            "face_recognition_sface_2021dec.onnx","")

svc = joblib.load('svc.pkl')
# mydict = ['BanNinh','BanThanh','ThayDuc']
mydict = ['BanAnh','BanBao','BanDien','BanDuc','BanDuong','BanGiang','BanHoa','BanHung','BanKy','BanLoc',
    'BanNam','BanNinh','BanPhi','BanQuocDuong','BanQuyetThang','BanSang','BanThang','BanThanh','BanTin','BanToan','BanVan','ThayDuc']

# Hàm xử lý request
@app.route("/", methods=['GET', 'POST'])
def home_page():
    # Nếu là POST (gửi file)
    if request.method == "POST":
         try:
            # Lấy file gửi lên
            image = request.files['file']
            if image:
                # Lưu file
                path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                print("Save = ", path_to_save)
                image.save(path_to_save)

                # # Convert image to dest size tensor
                # frame = cv2.imread(path_to_save)

                # frame, ndet = yolov6_model.infer(frame, conf_thres=0.6, iou_thres=0.45)

                # if ndet!=0:
                #     cv2.imwrite(path_to_save, frame)

                #     # Trả về kết quả
                #     return render_template("index.html", user_image = image.filename , rand = str(random()),
                #                            msg="Tải file lên thành công", ndet = ndet)
                # else:
                #     return render_template('index.html', msg='Không nhận diện được vật thể')
                imgin = cv2.imread(path_to_save)
                width = 320
                height = 320 # keep original height
                dim = (width, height)
                # resize image
                imgin = cv2.resize(imgin, dim, interpolation = cv2.INTER_AREA)

                faces = detector.detect(imgin)
                face_align = recognizer.alignCrop(imgin, faces[1][0])
                face_feature = recognizer.feature(face_align)
                test_prediction = svc.predict(face_feature)

                result = mydict[test_prediction[0]]
                cv2.putText(imgin,result,(5,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255))

                cv2.imwrite(path_to_save, imgin)

                # Trả về kết quả
                return render_template("index.html", user_image = image.filename , rand = str(random()),
                                           msg="Tải file lên thành công")

                # cv2.namedWindow("ImageIn", cv2.WINDOW_AUTOSIZE)
                # cv2.imshow("ImageIn", imgin)

            else:
                # Nếu không có file thì yêu cầu tải file
                return render_template('index.html', msg='Hãy chọn file để tải lên')

         except Exception as ex:
            # Nếu lỗi thì thông báo
            print(ex)
            return render_template('index.html', msg='Không nhận diện được vật thể')

    else:
        # Nếu là GET thì hiển thị giao diện upload
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)