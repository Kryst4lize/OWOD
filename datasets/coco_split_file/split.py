import json

T1_COCO_CLASS_NAMES = [
    "airplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
    "chair", "cow", "dining table", "dog", "horse", "motorcycle", "person",
    "potted plant", "sheep", "couch", "train", "tv"
]
T2_CLASS_NAMES = [
    "truck", "traffic light", "fire hydrant", "stop sign", "parking meter",
    "bench", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase",
    "microwave", "oven", "toaster", "sink", "refrigerator"
]
T3_CLASS_NAMES = [
    "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "hot dog", "pizza", "donut", "cake"
]
T4_CLASS_NAMES = [
    "bed", "toilet", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "book", "clock",
    "vase", "scissors", "teddy bear", "hair drier", "toothbrush",
    "wine glass", "cup", "fork", "knife", "spoon", "bowl"
]

def filter_annotations(annotation_path, destination_path, include_classes):
    # Load the original JSON file
    with open(annotation_path, 'r') as f:
        data = json.load(f)

    # Get the category IDs for the specified classes
    category_ids = {category['id']: category for category in data['categories'] if category['name'] in include_classes}
    filtered_annotations = [anno for anno in data['annotations'] if anno['category_id'] in category_ids]
    image_ids = {anno['image_id'] for anno in filtered_annotations}
    filtered_images = [img for img in data['images'] if img['id'] in image_ids]
    filtered_categories = [category for category_id, category in category_ids.items()]

    # Create the new JSON structure
    filtered_data = {
        'info': data.get('info', {}),
        'licenses': data.get('licenses', []),
        'images': filtered_images,
        'annotations': filtered_annotations,
        'categories': filtered_categories
    }

    # Save the filtered data to a new JSON file
    with open(destination_path, 'w') as f:
        json.dump(filtered_data, f, indent=4)

    print(f'Filtered JSON file created successfully at {destination_path}')

# Usage
annotation_path = '../annotations/instances_train2017.json'
destination_path = '../json_coco_file/'
spliting_file_name = ["T1_instances_train2017_split.json","T2_instances_train2017_split.json","T3_instances_train2017_split.json","T4_instances_train2017_split.json"]
Class = [T1_COCO_CLASS_NAMES,T2_CLASS_NAMES,T3_CLASS_NAMES,T4_CLASS_NAMES]


for i in range(4):
    filter_annotations(annotation_path, destination_path + spliting_file_name[i], Class[i])