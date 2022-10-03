import cv2
import time
import os
from config.path import *

def main():
    list_video_name = list_people
    for v in list_video_name :
        path_video_name=path_project +'/'+'video/'+v+'.mp4'
        cap = cv2.VideoCapture(f'{path_video_name}')
        # Resolution 640*480
        time.sleep(3)

        if cap is None or not cap.isOpened():
            print('Khong the mo file video')
            return
        cv2.namedWindow('Image', cv2.WINDOW_AUTOSIZE)
        n = 1
        dem = 0

        # create folder include file image 
        # Directory
        directory = f"{v}"
                
        parent_dir = path_image
        # Path
        path = os.path.join(parent_dir, directory)
  
        os.mkdir(path)

        while True:
            [success, img] = cap.read()
            ch = cv2.waitKey(30)
            if success:
                #img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                # imgROI = img[40:(40+480), :]  # Tao ra anh 480x480   # video  640*480

                # imgROI = cv2.resize(imgROI, (360, 360))              # video  640*480
                imgROI = cv2.resize(img, (320, 320))  # video vuong
                cv2.imshow('Image', imgROI)
            else:
                break
            if n % 4 == 0:
                filename = v+'_%04d.bmp' % (dem)
                path=path_image+'/'+v
                cv2.imwrite(os.path.join(path ,filename),imgROI)
                dem = dem + 1
            n = n + 1
    return


if __name__ == "__main__":
    main()
