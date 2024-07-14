import json
import random 

def process_coco_annotations_task(input_json, output_json, image_file, class_set):
    # Load input COCO annotations file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)
    
    # Load image file
    with open(image_file, 'r') as f:
        image_list = json.load(f)
    
    # Create a set of image file names for quick lookup
    image_set = set(image_list)
    
    # Filter images in the COCO data to only keep the ones in image_set
    filtered_images = [img for img in coco_data['images'] if img['file_name'] in image_set]
    image_ids = {img['id'] for img in filtered_images}
    
    # Filter annotations to only keep those corresponding to the selected images
    filtered_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] in image_ids]
    
    # Create a set of category IDs for the classes in class_set
    class_set_lower = {cls.lower() for cls in class_set}
    filtered_categories = [cat for cat in coco_data['categories'] if cat['name'].lower() in class_set_lower]
    category_ids = {cat['id'] for cat in filtered_categories}
    
    # Filter annotations to only keep those belonging to the specified classes
    filtered_annotations = [ann for ann in filtered_annotations if ann['category_id'] in category_ids]
    
    # Construct the output COCO data structure
    filtered_coco_data = {
        'images': filtered_images,
        'annotations': filtered_annotations,
        'categories': filtered_categories,
        'info': coco_data.get('info', {}),
        'licenses': coco_data.get('licenses', []),
    }
    
    # Save the filtered COCO data to the output file
    with open(output_json, 'w') as f:
        json.dump(filtered_coco_data, f, indent=4)
    
    return filtered_coco_data

def process_coco_annotations_unknown(input_json, output_json, image_file):
    # Load input COCO annotations file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)
    
    # Load image file
    with open(image_file, 'r') as f:
        image_list = json.load(f)
    
    # Create a set of image file names for quick lookup
    image_set = set(image_list)
    
    # Filter images in the COCO data to only keep the ones in image_set
    filtered_images = [img for img in coco_data['images'] if img['file_name'] in image_set]
    image_ids = {img['id'] for img in filtered_images}
    
    # Filter annotations to only keep those corresponding to the selected images
    filtered_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] in image_ids]
    
    # Create a new category called 'unknown'
    unknown_category = {'id': 1, 'name': 'unknown', 'supercategory': ''}
    filtered_categories = [unknown_category]
    unknown_category_id = unknown_category['id']
    
    # Change all category_id in annotations to the 'unknown' category
    for ann in filtered_annotations:
        ann['category_id'] = unknown_category_id
    
    # Construct the output COCO data structure
    filtered_coco_data = {
        'images': filtered_images,
        'annotations': filtered_annotations,
        'categories': filtered_categories,
        'info': coco_data.get('info', {}),
        'licenses': coco_data.get('licenses', []),
    }
    
    # Save the filtered COCO data to the output file
    with open(output_json, 'w') as f:
        json.dump(filtered_coco_data, f, indent=4)
    
    return filtered_coco_data

def compress_coco_json(input_json):
    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)
    
    # Minify the JSON content by dumping it without any indentation or extra spaces
    with open(input_json, 'w') as f:
        json.dump(coco_data, f, separators=(',', ':'))