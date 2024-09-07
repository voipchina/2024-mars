import os
import json
from glob import glob
# Directory containing the JSON files
json_dir = '/root/autodl-tmp/2024_mars/train/json'

# Image directory
image_dir = '/root/autodl-tmp/2024_mars/train/jpg'

# Image size
image_width = 1920
image_height = 1080

category_cn_ids = {
    '机动车违停': 1,
    '非机动车违停': 2,
    '违法经营': 3,
    '垃圾桶满溢': 4,
}
# Category IDs and labels
category_ids = {
    1: 'motor',
    2: 'nonmotor',
    3: 'occupation',
    4: 'garbagecan'
}

# Initialize COCO annotation dictionary
coco_annotation = {
    'info': {},
    'licenses': [],
    'images': [],
    'annotations': [],
    'categories': []
}

# Iterate over the JSON files
for json_path in sorted(glob(os.path.join(json_dir, '*.json'))):
    with open(json_path, 'r') as f:
        data = json.load(f)
    image_id = len(coco_annotation['images']) + 1
    json_basename = os.path.basename(json_path)
    for i, anno in enumerate(data):
        category_id = category_cn_ids[anno['category']]
        image_filename = os.path.join(image_dir, f'{json_basename}_{i+1}.jpg')
        coco_annotation['images'].append({
            'id': image_id,
            'file_name': image_filename,
            'width': image_width,
            'height': image_height
        })

        coco_annotation['annotations'].append({
            'id': len(coco_annotation['annotations']) + 1,
            'image_id': image_id,
            'category_id': category_id,
            'category_label': category_ids.get(category_id),
            'bbox': anno['bbox'],
            'iscrowd': 0
        })

# Add categories to COCO annotation
for category_id, category_label in category_ids.items():
    coco_annotation['categories'].append({
        'id': category_id,
        'name': category_label,
        'supercategory': ''
    })

# Save COCO annotation as JSON file
output_path = '/root/ws/2024-mars/src/coco_annotation.json'
with open(output_path, 'w') as f:
    json.dump(coco_annotation, f)
