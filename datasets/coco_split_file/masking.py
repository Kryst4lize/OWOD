import json
import random 

def masking_json(input_json, output_json, categories, num_images= 15000):
    with open(input_json, 'r') as f:
        data = json.load(f)

    # Create a mapping from category id to category name
    category_name_to_id = {cat['name']: cat['id'] for cat in data['categories']}
    category_id_to_name = {cat['id']: cat['name'] for cat in data['categories']}

    # Filter out category IDs based on the provided category names
    selected_category_ids = set(category_name_to_id[cat] for cat in categories if cat in category_name_to_id)

    unknown_category_id = max(category_name_to_id.values()) + 1
    new_categories = [{'id': category_name_to_id[cat], 'name': cat} for cat in categories if cat in category_name_to_id]
    new_categories.append({'id': unknown_category_id, 'name': 'unknown'})

    new_coco_dataset = {
        'info': data.get('info', {}),
        'licenses': data.get('licenses', []),
        'images': [],
        'annotations': [],
        'categories': new_categories  # Add 'unknown' category
    }

    # Track image ids that should be included
    image_ids = set()

    # Collect image ids that have at least one annotation in the selected categories
    for ann in data['annotations']:
        if ann['category_id'] in selected_category_ids:
            image_ids.add(ann['image_id'])

    # Filter annotations based on collected image ids and change unspecified categories to 'unknown'
    for ann in data['annotations']:
        if ann['image_id'] in image_ids:
            if ann['category_id'] not in selected_category_ids:
                ann['category_id'] = unknown_category_id
            new_coco_dataset['annotations'].append(ann)

    # Filter images based on collected image ids
    new_coco_dataset['images'] = [img for img in data['images'] if img['id'] in image_ids]

    # Write the new JSON data to the output file
    with open(output_json, 'w') as f:
        json.dump(new_coco_dataset, f, indent=4)

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