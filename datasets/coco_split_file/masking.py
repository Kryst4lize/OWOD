import json
import random 
from collections import defaultdict

def process_coco_categories(input_json, output_json, class_list):
    import json

    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)

    # Flatten the list of class names into a single list and map 
    new_category_mapping = {}
    current_id = 0

    for task_classes in class_list:
        for category in task_classes:
            new_category_mapping[category] = current_id
            current_id += 1

    # Reverse Mapping (To trace annotation category id to new category id)
    old_to_new_category_mapping = {}

    # Update the categories 
    for category in coco_data['categories']:
        category_name = category['name']
        if category_name in new_category_mapping:
            old_to_new_category_mapping[category['id']] = new_category_mapping[category_name]
            category['id'] = new_category_mapping[category_name]

    # Update the category ids in the annotations
    for annotation in coco_data['annotations']:
        old_category_id = annotation['category_id']
        # Map the old category to the new one
        if old_category_id in old_to_new_category_mapping:
            annotation['category_id'] = old_to_new_category_mapping[old_category_id]

    with open(output_json, 'w') as f:
        json.dump(coco_data, f)

def process_coco_annotations_task(input_json, output_json, image_file, class_set, class_set_2):
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
        # Flatten class_set_2
    class_set_2 = [item for sublist in class_set_2 for item in sublist]
    class_set_lower = {cls.lower() for cls in class_set}  | {cls.lower() for cls in class_set_2}
    filtered_categories = [cat for cat in coco_data['categories'] if cat['name'].lower() in class_set_lower]
    
    
    category_ids = {cat['id'] for cat in filtered_categories}
    
    # Filter annotations to only keep those belonging to the specified classes
    filtered_annotations = [ann for ann in filtered_annotations if ann['category_id'] in category_ids]

    # TODO: Not remove all categories id in COCO. Instead, keep it 
    filtered_categories = [cat for cat in coco_data['categories']]    
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


def process_coco_annotations_task_val_new(input_json, output_json, image_file, class_set):
    # Load input COCO annotations file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)
    
    # Load all image files and combine them into a single set
    combined_image_set = set()
    for image_file in image_file:
        with open(image_file, 'r') as f:
            image_list = json.load(f)
            combined_image_set.update(image_list)  # Add images to the set
    
    # Create a set of image file names for quick lookup
    image_set = set(combined_image_set)
    
    # Filter images in the COCO data to only keep the ones in image_set
    filtered_images = [img for img in coco_data['images'] if img['file_name'] in image_set]
    image_ids = {img['id'] for img in filtered_images}
    
    # Filter annotations to only keep those corresponding to the selected images
    filtered_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] in image_ids]
    
    # Initialize a combined category set
    combined_class_set = set()
    
    # Convert all class sets to lowercase and combine them
    for class_set in class_set:
        combined_class_set.update({cls.lower() for cls in class_set})
    filtered_categories = [cat for cat in coco_data['categories'] if cat['name'].lower() in combined_class_set]
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
    
    # TODO: Not remove all categories. Instead, keep it 
    filtered_categories = [cat for cat in coco_data['categories']]
    unknown_category_id = max(cat['id'] for cat in coco_data['categories']) + 1
    filtered_categories.append({
        'id': unknown_category_id,
        'name': 'unknown',
        'supercategory': 'unknown'
    })
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
    
    # TODO: Not remove all categories. Instead, keep it 
    filtered_categories = [cat for cat in coco_data['categories']]
    unknown_category_id = max(cat['id'] for cat in coco_data['categories']) + 1
    filtered_categories.append({
        'id': unknown_category_id,
        'name': 'unknown',
        'supercategory': 'unknown'
    })
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

def process_coco_annotations_adding(input_json_1, input_json_2, output_json, class_set_1, class_set_2, max_images, image_list):
    # Load the processed coco data (input_json_1) and original coco data (input_json_2)
    with open(input_json_1, 'r') as f:
        processed_coco_data = json.load(f)
    with open(input_json_2, 'r') as f:
        coco_data = json.load(f)

    # Load the list of images to be preserved from image_list
    with open(image_list, 'r') as f:
        image_list_data = json.load(f)
    image_list_ids = {img.split('.')[0] for img in image_list_data}  # Set of image IDs to preserve

    # Class sets to IDs mappings
    category_mapping = {cat['name']: cat['id'] for cat in coco_data['categories']}
    class_set_1_ids = {category_mapping[cat] for cat in class_set_1 if cat in category_mapping}
    class_set_2_ids = {category_mapping[cat] for cls in class_set_2 for cat in cls if cat in category_mapping}

    # Dictionaries for counting instances
    selected_class_set_2_instances = defaultdict(int)
    image_ratings = defaultdict(lambda: {'class_set_count': 0, 'total_count': 0})
    image_annotations = defaultdict(list)

    # Collect all annotations and build image annotations
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        if category_id in class_set_2_ids:
            image_ratings[image_id]['class_set_count'] += 1
        image_ratings[image_id]['total_count'] += 1
        image_annotations[image_id].append(annotation)

    # Calculate Rating 2 for each image
    for counts in image_ratings.values():
        counts['rating_2'] = counts['class_set_count'] / counts['total_count'] if counts['total_count'] > 0 else 0

    # Sort images by Rating 2
    sorted_images_by_rating_2 = sorted(image_ratings.items(), key=lambda x: (x[1]['rating_2'], x[1]['class_set_count']), reverse=True)

    # Start selecting images based on class_set_2 instance requirements
    selected_images = []
    selected_image_ids = set()
    processed_image_ids = {img['id'] for img in processed_coco_data['images']}  # Already processed images

    for image_id, counts in sorted_images_by_rating_2:
        if image_id not in processed_image_ids and image_id not in image_list_ids and counts['rating_2'] > 0:
            # Check if the image contains any class from class_set_2 that still needs instances
            has_necessary_class = False
            for annotation in image_annotations[image_id]:
                if annotation['category_id'] in class_set_2_ids and selected_class_set_2_instances[annotation['category_id']] < 50:
                    has_necessary_class = True
                    break
            
            # Skip the image if it only contains fully satisfied classes
            if not has_necessary_class:
                continue

            # Add the image to selected images
            selected_images.append((image_id, counts))
            selected_image_ids.add(image_id)

            # Update the instance count for class_set_2
            for annotation in image_annotations[image_id]:
                if annotation['category_id'] in class_set_2_ids:
                    selected_class_set_2_instances[annotation['category_id']] += 1

            # Stop when all classes in class_set_2 have at least 50 instances or max_images is reached
            if all(instances >= 50 for instances in selected_class_set_2_instances.values()) or len(selected_image_ids) >= max_images:
                break

    # Create the final processed COCO annotation by merging with the selected images
    new_annotations = []
    new_images = []
    
    # Add existing images and annotations from input_json_1 (processed coco)
    for image in processed_coco_data['images']:
        new_images.append(image)
    for annotation in processed_coco_data['annotations']:
        new_annotations.append(annotation)

    # Add selected images and their annotations from input_json_2
    for image in coco_data['images']:
        if image['id'] in selected_image_ids:
            new_images.append(image)
    for annotation in coco_data['annotations']:
        if annotation['image_id'] in selected_image_ids and annotation['category_id'] in class_set_2_ids:
            new_annotations.append(annotation)

    # Write the output to a new COCO JSON file
    output_data = {
        'images': new_images,
        'annotations': new_annotations,
        'categories': coco_data['categories']
    }
    with open(output_json, 'w') as f:
        json.dump(output_data, f)

    print(f"Successfully added {len(selected_image_ids)} images with at least 50 instances per category in class_set_2.")