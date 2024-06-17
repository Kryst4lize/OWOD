import json
from collections import defaultdict
from pycocotools.coco import COCO
import csv

T1_COCO_CLASS_NAMES = [
    "airplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
    "chair", "cow", "dining table", "dog", "horse", "motorcycle", "person",
    "potted plant", "sheep", "couch", "train", "tv"
]


annotation_file = './annotations/instances_train2017.json'
dest_file ='./'

# Load the COCO annotations file
def count_annotation(annotation_file, destination_file_path ='./' ,file_name='filename.csv'):
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

def total_images_check (annotation_file, destination_file_path ='./', classes=[], file_name='filename.csv'):
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

count_categories('json_coco_file/T1_instances_train2017_split.json')
# count_annotation(annotation_file, dest_file, 'category_bruh.csv')
# total_images_check(annotation_file, dest_file, T1_COCO_CLASS_NAMES, 'total_images.csv')
