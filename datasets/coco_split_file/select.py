import json
import argparse
from collections import defaultdict

def filter_and_select_images(input_json, output_json, min_max_images, categories):
    with open(input_json, 'r') as f:
        coco_data = json.load(f)

    # Create a mapping from category id to category name and vice versa
    category_name_to_id = {cat['name']: cat['id'] for cat in coco_data['categories']}
    category_id_to_name = {cat['id']: cat['name'] for cat in coco_data['categories']}
    unknown_category_id = max(category_name_to_id.values()) + 1

    # Filter out category IDs based on the provided category names
    selected_category_ids = set(category_name_to_id[cat] for cat in categories if cat in category_name_to_id)

    # Initialize counters for total instances in each class
    total_instances = defaultdict(int)
    for ann in coco_data['annotations']:
        total_instances[category_id_to_name.get(ann['category_id'], 'unknown')] += 1

    print("Total instances in each class:")
    for category, count in total_instances.items():
        print(f"Category: {category}, Count: {count}")

    # Criteria 1: Filter images based on the percentage of 'unknown' instances
    image_annotations = defaultdict(list)
    for ann in coco_data['annotations']:
        image_annotations[ann['image_id']].append(ann)

    def calculate_rating(annotations):
        total_instances = len(annotations)
        unknown_instances = sum(1 for ann in annotations if ann['category_id'] == unknown_category_id)
        rating = (1 - unknown_instances / total_instances) * 100
        return rating

    selected_images = []
    for image in coco_data['images']:
        if image['id'] in image_annotations:
            rating = calculate_rating(image_annotations[image['id']])
            if rating >= 80:  # Rating >= 20% of specified categories
                selected_images.append((image, rating))

    new_coco_data = {
        'info': coco_data.get('info', {}),
        'licenses': coco_data.get('licenses', []),
        'images': [],
        'annotations': [],
        'categories': coco_data['categories']
    }
    # Criteria 2: Ensure total instances of each class >= 50% of total instances in annotation file
    def count_instances(images):
        instance_count = defaultdict(int)
        for image, _ in images:
            for ann in image_annotations[image['id']]:
                instance_count[category_id_to_name.get(ann['category_id'], 'unknown')] += 1
        return instance_count

    def meets_criteria(instance_count):
        for category in categories:
            if instance_count[category] < 0.5 * total_instances[category]:
                return False
        return True

    selected_images.sort(key=lambda x: x[1], reverse=True)  # Sort images by rating in descending order

    filtered_images = []
    instance_count = count_instances(filtered_images)
    for image, rating in selected_images:
        if len(filtered_images) >= min_max_images[1]:
            break
        filtered_images.append((image, rating))
        instance_count = count_instances(filtered_images)
        if meets_criteria(instance_count):
            break
    
    # Add more images if criteria 2 is not met
    if not meets_criteria(instance_count):
        for image, rating in selected_images:
            if len(filtered_images) >= min_max_images[1]:
                break
            if (image, rating) not in filtered_images:
                filtered_images.append((image, rating))
                instance_count = count_instances(filtered_images)
                if meets_criteria(instance_count):
                    break
    # Prepare the new dataset
    final_images = [img for img, _ in filtered_images]
    final_image_ids = {img['id'] for img in final_images}
    new_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] in final_image_ids]

    new_coco_data = {
        'info': coco_data.get('info', {}),
        'licenses': coco_data.get('licenses', []),
        'images': final_images,
        'annotations': new_annotations,
        'categories': coco_data['categories']
        }

    # Write the new JSON data to the output file
    with open(output_json, 'w') as f:
        json.dump(new_coco_data, f, indent=4)
