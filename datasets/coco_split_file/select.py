import json
import argparse
from collections import defaultdict

def filter_and_select_images(input_json, output_json,categories, min_max_images= [20000, 50000]):
    with open(input_json, 'r') as f:
        coco_data = json.load(f)

    # Create a mapping from category id to category name and vice versa
    category_name_to_id = {cat['name']: cat['id'] for cat in coco_data['categories']}
    category_id_to_name = {cat['id']: cat['name'] for cat in coco_data['categories']}
    unknown_category_id = max(category_name_to_id.values())

    # Filter out category IDs based on the provided category names
    selected_category_ids = set(category_name_to_id[cat] for cat in categories if cat in category_name_to_id)

    # Initialize counters for total instances in each class
    total_instances = defaultdict(int)
    for ann in coco_data['annotations']:
        total_instances[category_id_to_name.get(ann['category_id'])] += 1

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
    unselected_images = []
    for image in coco_data['images']:
        if image['id'] in image_annotations:
            rating = calculate_rating(image_annotations[image['id']])
            if rating >= 80:  # Rating >= 20% of specified categories
                selected_images.append((image, rating))
            else :
                unselected_images.append((image, rating))

    # Sort images by rating in descending order
    selected_images.sort(key=lambda x: x[1], reverse=True)
    unselected_images.sort(key=lambda x: x[1], reverse=True)
                
    # Sort images based on rating and write to file
    with open("image_ratings.txt", "w") as rating_file:
        rating_file.write("Ratings of selected images (sorted):\n")
        for image, rating in selected_images:
            rating_file.write(f"Image ID: {image['id']}, Rating: {rating}%\n")

    with open("image_unratings.txt", "w") as unrating_file:
        unrating_file.write("Ratings of selected images (sorted):\n")
        for image, rating in unselected_images:
            unrating_file.write(f"Image ID: {image['id']}, Rating: {rating}%\n")

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

    

    filtered_images = []
    instance_count = count_instances(filtered_images)
    for image, rating in selected_images:
        if len(filtered_images) >= 50000:
            print("Maximum number of images reached")
            break
        filtered_images.append((image, rating))
        instance_count = count_instances(filtered_images)
        if meets_criteria(instance_count):
            print("Criteria 2 met")
            break
    
    # Add more images if criteria 2 is not met
    if len(filtered_images) < 25000 or not meets_criteria(instance_count):
        for image, rating in unselected_images:
            if len(filtered_images) >= 25000 and meets_criteria(instance_count):
                print("Min number of images reached when adding unselected images")
                break
            filtered_images.append((image, rating))
            instance_count = count_instances(filtered_images)
            if len(filtered_images) < 50000:
                print("Criteria 2 not met")
                break

    # Ensure at least the minimum number of images is selected
    while len(filtered_images) < 25000 and unselected_images:
        image, rating = unselected_images.pop(0)
        filtered_images.append((image, rating))

    # Prepare the new dataset
    final_images = [img for img, _ in filtered_images]
    final_image_ids = {img['id'] for img in final_images}
    new_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] in final_image_ids]

    new_coco_data = {
        'info': coco_data.get('info', {}),
        'licenses': coco_data.get('licenses', []),
        'images': final_images,
        'annotations': new_annotations,
        'categories': [{'id': category_name_to_id[cat], 'name': cat} for cat in categories if cat in category_name_to_id]
        }
    
    # Count the total instances in each class after filtering
    new_total_instances = defaultdict(int)
    for ann in new_coco_data['annotations']:
        new_total_instances[category_id_to_name.get(ann['category_id'])] += 1

    print("Total instances in each class:")
    for category, count in new_total_instances.items():
        print(f"Category: {category}, Count: {count}")

    # Write the new JSON data to the output file
    with open(output_json, 'w') as f:
        json.dump(new_coco_data, f, indent=4)
