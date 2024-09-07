import sys
YOLOv10_PATH = '/root/autodl-tmp/github/yolov10'
sys.path.append(YOLOv10_PATH)
import os
import json
from ultralytics import YOLOv10
from glob import glob
from tqdm import tqdm

WS_ROOT = '/root/ws/2024-mars'
DATASET_ROOT = '/root/autodl-tmp/2024_mars/coco'

model = YOLOv10(f"{YOLOv10_PATH}/runs/detect/train/weights/last.pt")


category_cn_list = ['机动车违停', '非机动车违停', '违法经营', '垃圾桶满溢']
width = 1920
height = 1080
pbar = tqdm(range(1, 40))
for video_index in pbar:
    plotted = False
    video_json= []
    jpg_files = sorted(glob(f'{DATASET_ROOT}/images/test2017/test_{video_index:03d}_*.jpg'))
    for jpg_file in jpg_files:
        results = model.predict(source=jpg_file, verbose=False)
        assert len(results) == 1
        boxes = results[0].boxes.cpu()
        cls_list = boxes.cls.numpy().tolist()
        if len(cls_list) == 0:
            continue
        conf_list = boxes.conf.numpy().tolist()
        bbox_list = boxes.xyxy.numpy().tolist()
        str_split = os.path.basename(jpg_file).replace('.jpg', '').split('_')
        assert(len(str_split)) == 3, str_split
        frame_id = int(str_split[2])
        event_id = 1
        for cls, conf, bbox in zip(cls_list, conf_list, bbox_list):
            cls = int(cls)
            cat_name = category_cn_list[cls]
            x1 = int(bbox[0])
            y1 = int(bbox[1])
            x2 = int(bbox[2])
            y2 = int(bbox[3])
            video_json.append({
                "frame_id": frame_id,
                "event_id": event_id,
                "category": cat_name,
                "bbox": [x1, y1, x2, y2],
                "confidence": conf
            })
            event_id = event_id + 1
        # plot the first frame
        if not plotted:
            results[0].save(f'{WS_ROOT}/result_plot/{video_index}.jpg')
            plotted = True

    json_string = json.dumps(video_json, indent=4, ensure_ascii=False)
    json_file = f'test_{video_index}.json'
    with open(f'{WS_ROOT}/result/{json_file}', 'w', encoding='utf-8') as f:
        f.write(json_string)
    print(f'write to {len(video_json)} records to {json_file}')
