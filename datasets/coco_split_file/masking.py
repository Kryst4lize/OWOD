import json
import random 

def process_coco_categories(input_json, output_json, class_list):
    import json

    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)

    # Flatten the list of class names into a single list, and map them to new IDs
    new_category_mapping = {}
    current_id = 0

    for task_classes in class_list:
        for category in task_classes:
            new_category_mapping[category] = current_id
            current_id += 1

    # Update the categories in the COCO file
    for category in coco_data['categories']:
        category_name = category['name']
        if category_name in new_category_mapping:
            category['id'] = new_category_mapping[category_name]

    # Update the category ids in the annotations
    for annotation in coco_data['annotations']:
        old_category_id = annotation['category_id']
        category_name = next((cat['name'] for cat in coco_data['categories'] if cat['id'] == old_category_id), None)
        if category_name and category_name in new_category_mapping:
            annotation['category_id'] = new_category_mapping[category_name]

    # Save the modified COCO file
    with open(output_json, 'w') as f:
        json.dump(coco_data, f)

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

def process_coco_annotations_task_val(input_json, output_json, image_file, class_set):
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
    
    # Check if 'unknown' category already exists
    unknown_category = next((cat for cat in coco_data['categories'] if cat['name'].lower() == 'unknown'), None)
    if unknown_category:
        unknown_category_id = unknown_category['id']
    else:
        # Assign a new ID for 'unknown' category
        unknown_category_id = max(cat['id'] for cat in coco_data['categories']) + 1
        filtered_categories.append({
            'id': unknown_category_id,
            'name': 'unknown',
            'supercategory': 'unknown'
        })
    
    # Update annotations: change category to 'unknown' if it doesn't belong to the specified classes
    for ann in filtered_annotations:
        if ann['category_id'] not in category_ids:
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