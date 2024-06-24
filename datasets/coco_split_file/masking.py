import json
import random 

def masking_json(input_json, output_json, categories, num_images= 15000):
    print("Running masking_json function")
    with open(input_json, 'r') as f:
        data = json.load(f)

    # Create a mapping from category id to category name
    category_name_to_id = {cat['name']: cat['id'] for cat in data['categories']}
    category_id_to_name = {cat['id']: cat['name'] for cat in data['categories']}

    # Filter out category IDs based on the provided category names
    selected_category_ids = set(category_name_to_id[cat] for cat in categories if cat in category_name_to_id)

    # Randomly select the specified number of image ids
    if len(image_ids) > num_images:
        image_ids = set(random.sample(image_ids, num_images))

    # Track image ids that should be included
    image_ids = set()

    # Collect image ids that have at least one annotation in the selected categories
    for ann in data['annotations']:
        if ann['category_id'] in selected_category_ids:
            image_ids.add(ann['image_id'])

    structure = {
        'info': data.get('info', {}),
        'licenses': data.get('licenses', []),
        'images': [],
        'annotations': [],
        'categories': data['categories'] + [{'id': max(category_name_to_id.values()) + 1, 'name': 'unknown'}]  # Add 'unknown' category
    }

    unknown_category_id = max(category_name_to_id.values()) + 1


    # Filter annotations based on collected image ids and change unspecified categories to 'unknown'
    for ann in data['annotations']:
        if ann['image_id'] in image_ids:
            if ann['category_id'] not in selected_category_ids:
                ann['category_id'] = unknown_category_id
            structure['annotations'].append(ann)

    # Filter images based on collected image ids
    structure['images'] = [img for img in data['images'] if img['id'] in image_ids]

    # Write the new JSON data to the output file
    with open(output_json, 'w') as f:
        json.dump(structure, f, indent=4)