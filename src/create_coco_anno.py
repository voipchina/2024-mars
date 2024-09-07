import os
import json
from glob import glob
from tqdm import tqdm
coco_ds_root = '/root/autodl-tmp/2024_mars/coco'
json_dir = '/root/autodl-tmp/2024_mars/train/json'
image_dir = '/root/autodl-tmp/2024_mars/train/jpg'
coco_test_dir = f'{coco_ds_root}/labels/train2017'

# Image size
image_width = 1920
image_height = 1080

category_cn_ids = {
    '机动车违停': 0,
    '非机动车违停': 1,
    '违法经营': 2,
    '垃圾桶满溢': 3,
}
# Category IDs and labels
category_ids = {
    0: 'motor',
    1: 'nonmotor',
    2: 'occupation',
    3: 'garbagecan'
}

def generate_file_list():
    train_files = sorted(glob('/root/autodl-tmp/2024_mars/coco/images/train2017/*.jpg'))
    with open(f'{coco_ds_root}/train2017.txt', 'w') as f:
        for line in train_files:
            f.write(f"{line}\n")
    val_files = [f for i, f in enumerate(train_files) if i%100 == 0]
    with open(f'{coco_ds_root}/val2017.txt', 'w') as f:
        for line in val_files:
            f.write(f"{line}\n")

def generate_test_file_list():
    test_files = sorted(glob('/root/autodl-tmp/2024_mars/coco/images/test2017/*.jpg'))
    with open(f'{coco_ds_root}/test2017.txt', 'w') as f:
        for line in test_files:
            f.write(f"{line}\n")

def generate_train_labels():
    pbar = tqdm(range(52))
    for video_idx in pbar:
        with open(f'{json_dir}/{video_idx}.json', 'r') as f:
            data = json.load(f)
        for i, anno in enumerate(data):
            category_id = category_cn_ids[anno['category']]
            frame_id = anno['frame_id']
            txt_basename = f'{video_idx:03d}_{frame_id-1:04d}.txt'
            txt_fullname = os.path.join(coco_test_dir, txt_basename)
            with open(txt_fullname, 'a+') as f:
                f.write(f'{category_id} {(anno["bbox"][0]+anno["bbox"][2])/2/image_width:.04f} {(anno["bbox"][1]+anno["bbox"][3])/2/image_height:.04f} '
                        f'{(anno["bbox"][2]-anno["bbox"][0])/image_width:.04f} {(anno["bbox"][3]-anno["bbox"][1])/image_height:.04f}\n')

if __name__ == '__main__':
    # generate_train_labels()
    # generate_file_list()
    generate_test_file_list()
