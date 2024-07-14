# All function in this file only using for experiment on for spliting the dataset, not for the final version. 
# It also have testing and printing function for the experiment only
# The final version will be in the select.py file

import json
from collections import defaultdict
import random
# All utitlities to split the COCO dataset
#Not include unspecified classes

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

# Including specified classes 
def filter_annotations_nonstrict(annotation_path, destination_path, categories):
    # Load the original JSON file
    with open(annotation_path, 'r') as f:
        data = json.load(f)

    # Create a mapping from category id to category name
    category_name_to_id = {cat['name']: cat['id'] for cat in data['categories']}
    selected_category_ids = set(category_name_to_id[cat] for cat in categories if cat in category_name_to_id)

    new_coco_data = {
        'info': data.get('info', {}),
        'licenses': data.get('licenses', []),
        'images': [],
        'annotations': [],
        'categories': data['categories']  # Keep all categories
    }
    image_ids = set()

    # Collect image ids that have at least one annotation in the selected categories
    for ann in data['annotations']:
        if ann['category_id'] in selected_category_ids:
            image_ids.add(ann['image_id'])

    # Filter annotations based on collected image ids
    for ann in data['annotations']:
        if ann['image_id'] in image_ids:
            new_coco_data['annotations'].append(ann)

    # Filter images based on collected image ids
    new_coco_data['images'] = [img for img in data['images'] if img['id'] in image_ids]

    # Write the new JSON data to the output file
    with open(destination_path, 'w') as f:
        json.dump(new_coco_data, f, indent=4)

# Usage
"""
annotation_path = '../annotations/instances_train2017.json'
destination_path = '../json_coco_file/'
spliting_file_name = ["T1_instances_train2017_split.json","T2_instances_train2017_split.json","T3_instances_train2017_split.json","T4_instances_train2017_split.json"]
Class = [T1_COCO_CLASS_NAMES,T2_CLASS_NAMES,T3_CLASS_NAMES,T4_CLASS_NAMES]
"""

"""
for i in range(4):
    # filter_annotations(annotation_path, destination_path + spliting_file_name[i], Class[i])

    # Dung cai nay neu muon filter theo cac class co san trong COCO (ca class chinh va class phu)
    filter_annotations_nonstrict(annotation_path, destination_path + spliting_file_name[i], Class[i])
"""

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

def process_coco_annotations_task2(input_json, output_json, min_images, max_images, class_set_1, class_set_2, list_json):
    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)

    # Load the list of images from task 1
    with open(list_json, 'r') as f:
        task_1_image_list = json.load(f)
    task_1_image_ids = {img.split('.')[0] for img in task_1_image_list}

    # Create dictionaries for category mapping and counting instances
    category_mapping = {cat['id']: cat['name'] for cat in coco_data['categories']}
    class_set_1_ids = {cat_id for cat_id, cat_name in category_mapping.items() if cat_name in class_set_1}
    class_set_2_ids = {cat_id for cat_id, cat_name in category_mapping.items() if cat_name in class_set_2}
    combined_class_ids = class_set_1_ids.union(class_set_2_ids)

    # Initialize counters and image ratings
    image_ratings = defaultdict(lambda: {'class_set_1_count': 0, 'class_set_2_count': 0, 'total_count': 0})
    class_set_1_total_instances = defaultdict(int)
    class_set_2_total_instances = defaultdict(int)
    image_annotations = defaultdict(list)

    # Count instances per image and prepare image annotations
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        if category_id in class_set_1_ids:
            image_ratings[image_id]['class_set_1_count'] += 1
            class_set_1_total_instances[category_id] += 1
        if category_id in class_set_2_ids:
            image_ratings[image_id]['class_set_2_count'] += 1
            class_set_2_total_instances[category_id] += 1
        image_ratings[image_id]['total_count'] += 1
        image_annotations[image_id].append(annotation)

    # Calculate Rating 1 and Rating 2 for each image
    for counts in image_ratings.values():
        counts['rating_1'] = counts['class_set_1_count'] / counts['total_count'] if counts['total_count'] > 0 else 0
        counts['rating_2'] = (counts['class_set_1_count'] + counts['class_set_2_count']) / counts['total_count'] if counts['total_count'] > 0 else 0

    # Sort images based on Rating 1
    sorted_images_by_rating_1 = sorted(image_ratings.items(), key=lambda x: (x[1]['rating_1'], x[1]['class_set_1_count']), reverse=True)
    sorted_images_by_rating_2 = sorted(image_ratings.items(), key=lambda x: (x[1]['rating_2'], x[1]['class_set_1_count'] + x[1]['class_set_2_count']), reverse=True)

    # Select initial set of top images based on Rating 1
    selected_images = []
    for image_id, counts in sorted_images_by_rating_1:
        if image_id not in task_1_image_ids and counts['rating_1'] >= 0.6:
            selected_images.append((image_id, counts))
        if len(selected_images) >= min_images:
            break
    print("Initial set of images selected phase 1: ", len(selected_images))

    # If not enough images, keep adding based on Rating 2
    if len(selected_images) < min_images:
        for image_id, counts in sorted_images_by_rating_2[len(selected_images):]:
            if image_id not in task_1_image_ids and counts['rating_2'] >= 0.7:
                selected_images.append((image_id, counts))
            if len(selected_images) >= min_images:
                break
    print("Initial set of images selected phase 2: ", len(selected_images))
    
    selected_class_set_1_instances = defaultdict(int)
    selected_class_set_2_instances = defaultdict(int)
    selected_image_ids = set(image_id for image_id, _ in selected_images)

    for annotation in coco_data['annotations']:
        if annotation['image_id'] in selected_image_ids:
            if annotation['category_id'] in class_set_1_ids:
                selected_class_set_1_instances[annotation['category_id']] += 1
            if annotation['category_id'] in class_set_2_ids:
                selected_class_set_2_instances[annotation['category_id']] += 1

    # Ensure minimum percentage of instances for each category in class_set_1 and class_set_2
    for category_id, total_instances in class_set_1_total_instances.items():
        required_instances = total_instances * 0.3
        while selected_class_set_1_instances[category_id] < required_instances and len(selected_image_ids) < max_images:
            for image_id, counts in sorted_images_by_rating_2:
                if image_id not in task_1_image_ids and image_id not in selected_image_ids and counts['class_set_1_count'] > 0:
                    category_instances_added = sum(1 for annotation in image_annotations[image_id] if annotation['category_id'] == category_id)
                    if category_instances_added > 0:
                        selected_image_ids.add(image_id)
                        selected_class_set_1_instances[category_id] += category_instances_added
                        if selected_class_set_1_instances[category_id] >= required_instances:
                            break
  
    # Prepare output and statistics
    output_image_list = [image['file_name'] for image in coco_data['images'] if image['id'] in selected_image_ids]

    # Print statistics
    print("Category-wise Statistics:")
    total_selected_class_set_1_instances = sum(selected_class_set_1_instances.values())
    total_class_set_1_instances = sum(class_set_1_total_instances.values())
    total_selected_class_set_2_instances = sum(selected_class_set_2_instances.values())
    total_class_set_2_instances = sum(class_set_2_total_instances.values())
    total_selected_instances = sum(image_ratings[image_id]['total_count'] for image_id in selected_image_ids)

    for category_id, total_instances in class_set_1_total_instances.items():
        selected_instances = selected_class_set_1_instances[category_id]
        category_name = category_mapping[category_id]
        percentage = (selected_instances / total_instances) * 100 if total_instances > 0 else 0
        print(f"{category_name} (Class Set 1): {selected_instances} / {total_instances} ({percentage:.2f}%)")

    for category_id, total_instances in class_set_2_total_instances.items():
        selected_instances = selected_class_set_2_instances[category_id]
        category_name = category_mapping[category_id]
        percentage = (selected_instances / total_instances) * 100 if total_instances > 0 else 0
        print(f"{category_name} (Class Set 2): {selected_instances} / {total_instances} ({percentage:.2f}%)")

    percentage_chosen_class_set_1 = (total_selected_class_set_1_instances / total_class_set_1_instances) * 100 if total_class_set_1_instances > 0 else 0
    percentage_chosen_class_set_2 = (total_selected_class_set_2_instances / total_class_set_2_instances) * 100 if total_class_set_2_instances > 0 else 0
    percentage_total_instances = ((total_selected_class_set_1_instances + total_selected_class_set_2_instances) / total_selected_instances) * 100 if total_selected_instances > 0 else 0

    print(f"Percentage of total instances of class_set_1 chosen: {percentage_chosen_class_set_1:.2f}%")
    print(f"Percentage of total instances of class_set_2 chosen: {percentage_chosen_class_set_2:.2f}%")
    print(f"Percentage of total instances in the selected images list: {percentage_total_instances:.2f}%")

    # Save output to JSON file
    with open(output_json, 'w') as f:
        json.dump(output_image_list, f, indent=4)

    return output_image_list

def process_coco_annotations_task3(input_json, output_json, min_images, max_images, class_set_1, list_json):
    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)

    # Load the list of images from task 1
    with open(list_json, 'r') as f:
        task_1_image_list = json.load(f)
    task_1_image_ids = {img.split('.')[0] for img in task_1_image_list}

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

    # Calculate Rating 1 for each image
    for counts in image_ratings.values():
        counts['rating_1'] = counts['class_set_1_count'] / counts['total_count'] if counts['total_count'] > 0 else 0

    # Sort images based on Rating 1
    sorted_images_by_rating_1 = sorted(image_ratings.items(), key=lambda x: (x[1]['rating_1'], x[1]['class_set_1_count']), reverse=True)

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

    # Ensure minimum percentage of instances for each category in class_set_1
    for category_id, total_instances in class_set_1_total_instances.items():
        required_instances = total_instances * 0.3
        while selected_class_set_1_instances[category_id] < required_instances and len(selected_image_ids) < max_images:
            for image_id, counts in sorted_images_by_rating_1:
                if image_id not in task_1_image_ids and image_id not in selected_image_ids and counts['class_set_1_count'] > 0:
                    category_instances_added = sum(1 for annotation in image_annotations[image_id] if annotation['category_id'] == category_id)
                    if category_instances_added > 0:
                        selected_image_ids.add(image_id)
                        selected_class_set_1_instances[category_id] += category_instances_added
                        if selected_class_set_1_instances[category_id] >= required_instances:
                            break
    print("Selected images after ensure minimum: ", len(selected_image_ids))

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
        
"""
    for category_id, total_instances in class_set_2_total_instances.items():
        required_instances = total_instances * 0.3
        while selected_class_set_2_instances[category_id] < required_instances and len(selected_image_ids) < max_images:
            for image_id, counts in sorted_images_by_rating_2:
                if image_id not in task_1_image_ids and image_id not in selected_image_ids and counts['class_set_2_count'] > 0:
                    category_instances_added = sum(1 for annotation in image_annotations[image_id] if annotation['category_id'] == category_id)
                    if category_instances_added > 0:
                        selected_image_ids.add(image_id)
                        selected_class_set_2_instances[category_id] += category_instances_added
                        if selected_class_set_2_instances[category_id] >= required_instances:
                            break
"""
# Update version including spliting the dataset into two parts and shuffle the images
def process_coco_annotations_task(input_json, output_json, image_file, class_set):
    # Load input COCO annotations file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)
    
    # Load image file
    with open(image_file, 'r') as f:
        image_list = json.load(f)
    
    # Shuffle the images randomly
    random.shuffle(image_list)
    
    # Split the images into two sets
    images_1000 = image_list[:1000]
    images_20000 = image_list[1000:]
    
    # Helper function to filter the COCO data
    def filter_coco_data(image_set, coco_data, class_set):
        image_ids = {img['id'] for img in image_set}
        
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
            'images': list(image_set),
            'annotations': filtered_annotations,
            'categories': filtered_categories,
            'info': coco_data.get('info', {}),
            'licenses': coco_data.get('licenses', []),
        }
        
        return filtered_coco_data
    
    # Convert images to sets for quick lookup
    image_set_1000 = {img for img in coco_data['images'] if img['file_name'] in images_1000}
    image_set_20000 = {img for img in coco_data['images'] if img['file_name'] in images_20000}
    
    # Filter the COCO data for each set
    filtered_coco_data_1000 = filter_coco_data(image_set_1000, coco_data, class_set)
    filtered_coco_data_20000 = filter_coco_data(image_set_20000, coco_data, class_set)
    
    # Save the filtered COCO data to the output files
    output_json_1, output_json_2 = output_json
    with open(output_json_1, 'w') as f:
        json.dump(filtered_coco_data_1000, f, indent=4)
    
    with open(output_json_2, 'w') as f:
        json.dump(filtered_coco_data_20000, f, indent=4)
    
    return [filtered_coco_data_1000, filtered_coco_data_20000]