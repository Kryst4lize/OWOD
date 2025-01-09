import json
from collections import defaultdict
from pycocotools.coco import COCO
import csv

# All utilities to check the validation of the split file
# Load the COCO annotations file

def count_annotation(annotation_file, destination_file_path ='./' ,file_name='filename.csv'):
    print("Running count_annotation function")
    coco = COCO(annotation_file)
    # Get all categories
    categories = coco.loadCats(coco.getCatIds())
    category_names = {cat['id']: cat['name'] for cat in categories}

    # Initialize a dictionary to count instances per category
    category_counts = defaultdict(int)

    # Get all annotation IDs
    annotation_ids = coco.getAnnIds()

    # Loop through each annotation
    for ann_id in annotation_ids:
        ann = coco.loadAnns(ann_id)[0]
        category_id = ann['category_id']
        category_counts[category_id] += 1

    # Prepare data for CSV
    csv_data = [["Category", "Count"]]
    for category_id, count in category_counts.items():
        category_name = category_names[category_id]
        csv_data.append([category_name, count])

    # Save to CSV
    output_file = f"{destination_file_path}{file_name}"
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)
    print(f"Category counts saved to {output_file}")

# Check the total images in one subset dataset task 
def total_images_check (annotation_file, destination_file_path ='../json_coco_file/', classes=[], file_name='filename.csv'):
    print("Running total_images_check function")
    # Load the COCO annotations file
    coco = COCO(annotation_file)
    unique_image_ids = set()
    # List of category names to check

    category = coco.getCatIds(catNms=classes)
    category_image_counts = {category_name: 0 for category_name in classes}
    all_image_ids = coco.getImgIds()

    for image_id in all_image_ids:
        # Get all annotation IDs for the current image
        ann_ids = coco.getAnnIds(imgIds=image_id)
        anns = coco.loadAnns(ann_ids)
        present_category_ids = set(ann['category_id'] for ann in anns)

        if any(category_id in present_category_ids for category_id in category):
            unique_image_ids.add(image_id)
        
    total_unique_images = len(unique_image_ids)

    # Save to CSV
    
    output_file = f"{destination_file_path}{file_name}"
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Unique Images", total_unique_images])

def count_categories(annotation_path):
    print("Running count_categories function")
    # Initialize the COCO object
    coco = COCO(annotation_path)
    
    # Get all category IDs
    category_ids = coco.getCatIds()
    
    # Get all categories
    categories = coco.loadCats(category_ids)
    
    # Create a dictionary to store category names and their counts
    category_count = {cat['name']: 0 for cat in categories}
    
    # Iterate over all category IDs
    for cat_id in category_ids:
        # Get all annotation IDs for the category
        annotation_ids = coco.getAnnIds(catIds=[cat_id])
        
        # Get the category name
        category_name = coco.loadCats([cat_id])[0]['name']
        
        # Store the count of annotations for the category
        category_count[category_name] = len(annotation_ids)
    
    # Print the counts per category
    for category_name, count in category_count.items():
        print(f"Category: {category_name}, Count: {count}")
    print("Total categories:", len(category_count))

def count_total_images_in_coco(input_json):
    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)
    
    # Calculate the total number of images
    total_images = len(coco_data['images'])
    
    print(f"Total number of images in the COCO dataset: {total_images}")
    
    return total_images

def print_coco_categories_and_instances(coco_file_path):
    # Load the COCO annotation file
    with open(coco_file_path, 'r') as f:
        coco_data = json.load(f)

    # Extract categories and annotations
    categories = coco_data.get('categories', [])
    annotations = coco_data.get('annotations', [])

    # Create a dictionary to map category IDs to their names
    category_dict = {cat['id']: cat['name'] for cat in categories}

    # Create a dictionary to count instances per category
    category_instance_counts = {cat_id: 0 for cat_id in category_dict.keys()}

    # Count instances for each category
    for annotation in annotations:
        cat_id = annotation['category_id']
        check = 0
        if cat_id in category_instance_counts:
            category_instance_counts[cat_id] += 1
        else:
            check =1 
            
    # Print categories and their instance counts
    for cat_id, count in category_instance_counts.items():
        category_name = category_dict[cat_id]
        print(f"Category Name: {category_name}, Category ID: {cat_id}, Total Instances: {count}")

def get_coco_categories_and_instances(coco_file_path):
    # Load the COCO annotation file
    with open(coco_file_path, 'r') as f:
        coco_data = json.load(f)

    # Extract categories and annotations
    categories = coco_data.get('categories', [])
    annotations = coco_data.get('annotations', [])

    # Create a dictionary to map category IDs to their names
    category_dict = {cat['id']: cat['name'] for cat in categories}

    # Create a dictionary to count instances per category
    category_instance_counts = {cat_id: 0 for cat_id in category_dict.keys()}

    # Count instances for each category
    for annotation in annotations:
        cat_id = annotation['category_id']
        if cat_id in category_instance_counts:
            category_instance_counts[cat_id] += 1

    # Create the string output instead of printing
    output = []
    for cat_id, count in category_instance_counts.items():
        category_name = category_dict[cat_id]
        output.append(f"Category Name: {category_name}, Category ID: {cat_id}, Total Instances: {count}")
    
    # Join the list into a single string with newline characters
    return "\n".join(output)

def task_statistic(input_json, class_set, output_file):
    # Load the COCO annotation file
    with open(input_json, 'r') as f:
        coco_data = json.load(f)

    # Create dictionaries for category mapping and counting instances
    category_mapping = {cat['id']: cat['name'] for cat in coco_data['categories']}
    
    # Prepare class set IDs mapping
    class_set_ids = []
    for class_names in class_set:
        class_set_ids.append({cat_id for cat_id, cat_name in category_mapping.items() if cat_name in class_names})

    # Initialize counters and statistics storage
    class_set_total_instances = [defaultdict(int) for _ in range(len(class_set))]
    class_set_image_annotations = [defaultdict(list) for _ in range(len(class_set))]
    image_ratings = [defaultdict(lambda: {'class_set_count': 0, 'total_count': 0}) for _ in range(len(class_set))]

    # Track selected images for each task (class set)
    selected_images_per_task = [set() for _ in range(len(class_set))]

    # Count instances per image and prepare image annotations for each class set
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        
        # Check which class set the category belongs to and update the corresponding counters
        for i, class_ids in enumerate(class_set_ids):
            if category_id in class_ids:
                image_ratings[i][image_id]['class_set_count'] += 1
                class_set_total_instances[i][category_id] += 1
            image_ratings[i][image_id]['total_count'] += 1
            class_set_image_annotations[i][image_id].append(annotation)
    
    # Open the output file for writing statistics
    with open(output_file, 'w') as out_file:
        # Process each class set separately
        for i, class_names in enumerate(class_set):
            total_class_set_instances = sum(class_set_total_instances[i].values())
            selected_images = [image_id for image_id, counts in image_ratings[i].items() if counts['class_set_count'] > 0]
            
            # Store selected images for duplication check
            selected_images_per_task[i].update(selected_images)
            
            total_selected_instances = sum(image_ratings[i][image_id]['total_count'] for image_id in selected_images)
            total_selected_class_set_instances = sum(class_set_total_instances[i].values())

            # Print statistics for the class set
            out_file.write(f"Class Set {i+1} - {class_names} Statistics:\n")
            for category_id, total_instances in class_set_total_instances[i].items():
                category_name = category_mapping[category_id]
                selected_instances = class_set_total_instances[i][category_id]
                percentage = (selected_instances / total_instances) * 100 if total_instances > 0 else 0
                out_file.write(f"  {category_name}: {selected_instances} / {total_instances} ({percentage:.2f}%)\n")

            percentage_chosen_class_set = (total_selected_class_set_instances / total_class_set_instances) * 100 if total_class_set_instances > 0 else 0
            percentage_total_instances = (total_selected_class_set_instances / total_selected_instances) * 100 if total_selected_instances > 0 else 0
            out_file.write(f"  Percentage of total instances of class_set chosen: {percentage_chosen_class_set:.2f}%\n")
            out_file.write(f"  Percentage of total instances in the selected images list: {percentage_total_instances:.2f}%\n")
            
            # Total images selected for the current task (class set)
            out_file.write(f"  Total images selected for Task {i+1}: {len(selected_images)}\n")
            out_file.write("\n")

        # Check for duplication between task pairs
        out_file.write(f"Image Duplication between Tasks:\n")
        num_tasks = len(class_set)
        for i in range(num_tasks):
            for j in range(i + 1, num_tasks):
                duplicate_images = selected_images_per_task[i].intersection(selected_images_per_task[j])
                out_file.write(f"  Duplication between Task {i+1} and Task {j+1}: {len(duplicate_images)} duplicate images\n")
        
        out_file.write("\n")

        # Print total images selected per task
        out_file.write("Total Images Selected Per Task:\n")
        for i in range(num_tasks):
            out_file.write(f"  Task {i+1}: {len(selected_images_per_task[i])} images\n")
        out_file.write("\n")
        # Calculate the percentage of duplicate images between task 2 and task 1, task 3 and task 2+1, task 4 and task 3+2+1
        

def calculate_duplicate_percentages(list_of_class, output_json):
    """
    Calculate duplicate percentages of images between sequential lists.
    
    Parameters:
        list_of_class (list): List of JSON file paths (e.g., [list1, list2, list3, list4]).
        output_json (str): Path to save the results as a JSON file.
    
    Returns:
        dict: A dictionary containing the duplicate percentages for each list.
    """
    duplicate_stats = {}
    all_images = set()  
    
    for i, list_path in enumerate(list_of_class):
        # Load the current list of images
        with open(list_path, 'r') as f:
            current_list = json.load(f)
        current_images = set(current_list)
        if i == 0:
            # The first list has no previous lists to compare to
            duplicate_stats[f"Task_{i+1}"] = 0.0
        else:
            # Calculate duplicates as a percentage of the current list
            duplicates = current_images & all_images
            duplicate_percentage = (len(duplicates) / len(current_images)) * 100 if current_images else 0
            duplicate_stats[f"Task_{i+1}"] = duplicate_percentage
        # Update all_images to include current images for comparison with the next list
        all_images.update(current_images)
    
    # Save the results to the output JSON file
    with open(output_json, 'w') as f:
        json.dump(duplicate_stats, f, indent=4)

    return duplicate_stats