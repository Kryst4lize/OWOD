import json
from collections import defaultdict

# If you want to print the statistics of the quality of the selected images, you can check process_coco_annotations_task3 function in experiment.py
def process_coco_annotations_task(input_json, output_json, min_images, max_images, class_set, list_json):
    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)

    # Load the list of images from task 1
    with open(list_json, 'r') as f:
        task_1_image_list = json.load(f)
    task_1_image_ids = {img.split('.')[0] for img in task_1_image_list}

    # Create dictionaries for category mapping and counting instances
    category_mapping = {cat['id']: cat['name'] for cat in coco_data['categories']}
    class_set_1_ids = {cat_id for cat_id, cat_name in category_mapping.items() if cat_name in class_set}

    # Initialize counters and image ratings
    image_ratings = defaultdict(lambda: {'class_set_count': 0, 'total_count': 0})
    class_set_1_total_instances = defaultdict(int)
    image_annotations = defaultdict(list)

    # Count instances per image and prepare image annotations
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        if category_id in class_set_1_ids:
            image_ratings[image_id]['class_set_count'] += 1
            class_set_1_total_instances[category_id] += 1
        image_ratings[image_id]['total_count'] += 1
        image_annotations[image_id].append(annotation)

    # Calculate Rating 1 for each image
    for counts in image_ratings.values():
        counts['rating_1'] = counts['class_set_count'] / counts['total_count'] if counts['total_count'] > 0 else 0

    # Sort images based on Rating 1
    sorted_images_by_rating_1 = sorted(image_ratings.items(), key=lambda x: (x[1]['rating_1'], x[1]['class_set_count']), reverse=True)

    # Select initial set of top images based on Rating 1
    selected_images = []
    for image_id, counts in sorted_images_by_rating_1:
        if image_id not in task_1_image_ids and counts['rating_1'] >= 0.6:
            selected_images.append((image_id, counts))
        if len(selected_images) >= min_images:
            break
    
    # If not enough images, keep adding based on total counts
    if len(selected_images) < min_images:
        for image_id, counts in sorted_images_by_rating_1[len(selected_images):]:
            if image_id not in task_1_image_ids:
                selected_images.append((image_id, counts))
            if len(selected_images) >= min_images:
                break
    
    selected_class_set_1_instances = defaultdict(int)
    selected_image_ids = set(image_id for image_id, _ in selected_images)

    for annotation in coco_data['annotations']:
        if annotation['image_id'] in selected_image_ids:
            if annotation['category_id'] in class_set_1_ids:
                selected_class_set_1_instances[annotation['category_id']] += 1

    # Ensure minimum percentage of instances for each category in class_set
    for category_id, total_instances in class_set_1_total_instances.items():
        required_instances = total_instances * 0.3
        while selected_class_set_1_instances[category_id] < required_instances and len(selected_image_ids) < max_images:
            for image_id, counts in sorted_images_by_rating_1:
                if image_id not in task_1_image_ids and image_id not in selected_image_ids and counts['class_set_count'] > 0:
                    category_instances_added = sum(1 for annotation in image_annotations[image_id] if annotation['category_id'] == category_id)
                    if category_instances_added > 0:
                        selected_image_ids.add(image_id)
                        selected_class_set_1_instances[category_id] += category_instances_added
                        if selected_class_set_1_instances[category_id] >= required_instances:
                            break

    # Add more images if still below max_images
    if len(selected_image_ids) < min_images:
        for image_id, counts in sorted_images_by_rating_1:
            if image_id not in task_1_image_ids and image_id not in selected_image_ids:
                selected_image_ids.add(image_id)
            if len(selected_image_ids) >= max_images:
                break

    # Prepare output and statistics
    output_image_list = [image['file_name'] for image in coco_data['images'] if image['id'] in selected_image_ids]

    # Print statistics
    
    """
    print("Category-wise Statistics:")
    total_selected_class_set_1_instances = sum(selected_class_set_1_instances.values())
    total_class_set_1_instances = sum(class_set_1_total_instances.values())
    total_selected_instances = sum(image_ratings[image_id]['total_count'] for image_id in selected_image_ids)

    for category_id, total_instances in class_set_1_total_instances.items():
        selected_instances = selected_class_set_1_instances[category_id]
        category_name = category_mapping[category_id]
        percentage = (selected_instances / total_instances) * 100 if total_instances > 0 else 0
        print(f"{category_name}: {selected_instances} / {total_instances} ({percentage:.2f}%)")

    percentage_chosen_class_set_1 = (total_selected_class_set_1_instances / total_class_set_1_instances) * 100 if total_class_set_1_instances > 0 else 0
    percentage_total_instances = (total_selected_class_set_1_instances / total_selected_instances) * 100 if total_selected_instances > 0 else 0

    print(f"Percentage of total instances of class_set chosen: {percentage_chosen_class_set_1:.2f}%")
    print(f"Percentage of total instances in the selected images list: {percentage_total_instances:.2f}%")
    """
    
    # Save output to JSON file
    with open(output_json, 'w') as f:
        json.dump(output_image_list, f, indent=4)

    return output_image_list

def get_unique_images(input_json ,output_json, list_json):
    # Read the COCO JSON file and extract the image file names
    with open(input_json , 'r') as f:
        coco_data = json.load(f)
    
    # Extract image file names from COCO JSON
    coco_images = {img['file_name'] for img in coco_data['images']}
    
    # Load images from the other JSON files
    images_in_other_jsons = set()
    for json_file in list_json:
        with open(json_file, 'r') as f:
            images = json.load(f)
            images_in_other_jsons.update(images)
    
    # Find images that are in COCO JSON but not in the other JSON files
    unique_images = coco_images - images_in_other_jsons
    
    # Convert to list and save to output JSON file
    unique_images_list = list(unique_images)
    with open(output_json, 'w') as f:
        json.dump(unique_images_list, f, indent=4)
    
    return unique_images_list