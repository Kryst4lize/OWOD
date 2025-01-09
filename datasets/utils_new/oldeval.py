# This file to evaluation the old split file approach, and print the statistics of the split file.
import json
from collections import defaultdict

# This simplify function only split task based on the class (old previous work, only for evaluation old work, not for new work)
def process_coco_annotations_task(input_json, output_json, class_set):
    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)
    # Create a mapping of category IDs to names and identify relevant category IDs
    category_mapping = {cat['id']: cat['name'] for cat in coco_data['categories']}
    class_set_ids = {cat_id for cat_id, cat_name in category_mapping.items() if cat_name in class_set}
    # Collect image IDs that contain instances from the class_set
    selected_image_ids = set(
        annotation['image_id'] for annotation in coco_data['annotations'] if annotation['category_id'] in class_set_ids
    )
    # Get file names of the selected images
    selected_image_list = [
        image['file_name'] for image in coco_data['images'] if image['id'] in selected_image_ids
    ]
    # Save the selected image file names to the output JSON
    with open(output_json, 'w') as f:
        json.dump(selected_image_list, f, indent=4)

    return selected_image_list


