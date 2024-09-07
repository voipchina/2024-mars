import sys
YOLOv10_PATH = '/root/autodl-tmp/github/yolov10'
sys.path.append(YOLOv10_PATH)
import os
from ultralytics import YOLOv10

# model = YOLOv10(f'{YOLOv10_PATH}/weights/yolov10s.pt')
# model.train(data='train.yaml', epochs=40, batch=64, imgsz=640)
model = YOLOv10("/root/autodl-tmp/github/yolov10/runs/detect/train/weights/last.pt")
model.train(resume=True)
model.save('yolov10s_mars.pt')
os.system("/usr/bin/shutdown")
