import json
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
destination_path = '../json_coco_file/T1_instances_train2017_split.json'
T1_COCO_CLASS_NAMES = [
    "airplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
    "chair", "cow", "dining table", "dog", "horse", "motorcycle", "person",
    "potted plant", "sheep", "couch", "train", "tv"
]

filter_annotations(annotation_path, destination_path, T1_COCO_CLASS_NAMES)