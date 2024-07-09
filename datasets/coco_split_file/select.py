import json
import argparse
from collections import defaultdict

def process_coco_annotations_task1(input_json, output_json, min_images, max_images, class_set_1):
    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)

    # Create dictionaries for category mapping and counting instances
    category_mapping = {cat['id']: cat['name'] for cat in coco_data['categories']}
    class_set_1_ids = {cat_id for cat_id, cat_name in category_mapping.items() if cat_name in class_set_1}

    # Initialize counters and image ratings
    image_ratings = defaultdict(lambda: {'class_set_1_count': 0, 'total_count': 0})
    class_set_1_total_instances = defaultdict(int)
    image_annotations = defaultdict(list)

    # Count instances per image and prepare image annotations
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        if category_id in class_set_1_ids:
            image_ratings[image_id]['class_set_1_count'] += 1
            class_set_1_total_instances[category_id] += 1
        image_ratings[image_id]['total_count'] += 1
        image_annotations[image_id].append(annotation)

    # Calculate rating for each image
    for counts in image_ratings.values():
        counts['rating'] = counts['class_set_1_count'] / counts['total_count'] if counts['total_count'] > 0 else 0

    # Sort images based on rating
    sorted_images = sorted(image_ratings.items(), key=lambda x: (x[1]['rating'], x[1]['class_set_1_count']), reverse=True)

    # Select initial set of top images
    selected_images = sorted_images[:min_images]

    # Prepare to track the selected instances
    selected_class_set_1_instances = defaultdict(int)
    selected_image_ids = set()

    for image_id, _ in selected_images:
         selected_image_ids.add(image_id)

    for annotation in coco_data['annotations']:
        if annotation['image_id'] in selected_image_ids and annotation['category_id'] in class_set_1_ids:
            selected_class_set_1_instances[annotation['category_id']] += 1

    # Ensure at least 50% instances for each category in class_set_1
    for category_id, total_instances in class_set_1_total_instances.items():
        print(len(selected_image_ids))
        required_instances = total_instances * 0.3
        if selected_class_set_1_instances[category_id] < required_instances or len(selected_image_ids) < max_images:
            # iterations= 0
            for image_id, counts in sorted_images:
                # iterations+=1
                # if iterations%1000 == 0:
                    # print(f"Pass {iterations} images")
                if image_id not in selected_image_ids and counts['class_set_1_count'] > 0:
                    category_instances_added = sum(1 for annotation in image_annotations[image_id] if annotation['category_id'] == category_id)
                    if category_instances_added > 0:
                        selected_image_ids.add(image_id)
                        # selected_images.append((image_id, counts))
                        selected_class_set_1_instances[category_id] += category_instances_added
                        if selected_class_set_1_instances[category_id] >= required_instances:
                            break

    # Add to enough images to reach the maximum number of images
    """
        for image_id, counts in sorted_images:
        if len(selected_image_ids) >= max_images:
            print("Max images reached: ", len(selected_image_ids))
            break
        if image_id not in selected_image_ids:
            selected_image_ids.add(image_id)
    """        
    # Prepare output and statistics
    output_image_list = [image['file_name'] for image in coco_data['images'] if image['id'] in selected_image_ids]

    # Print statistics
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

    print(f"Percentage of total instances of class_set_1 chosen: {percentage_chosen_class_set_1:.2f}%")
    print(f"Percentage of total instances in the selected images list: {percentage_total_instances:.2f}%")

    # Save output to JSON file
    with open(output_json, 'w') as f:
        json.dump(output_image_list, f, indent=4)

    return output_image_list

