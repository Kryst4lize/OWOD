import csv
import masking as mk
import select as slt
import instance as ins 
import oldeval as oe
T1_COCO_CLASS_NAMES = [
    "airplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
    "chair", "cow", "dining table", "dog", "horse", "motorcycle", "person",
    "potted plant", "sheep", "couch", "train", "tv"
]
T2_CLASS_NAMES = [
    "truck", "traffic light", "fire hydrant", "stop sign", "parking meter",
    "bench", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase",
    "microwave", "oven", "toaster", "sink", "refrigerator"
]
T3_CLASS_NAMES = [
    "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "hot dog", "pizza", "donut", "cake"
]
T4_CLASS_NAMES = [
    "bed", "toilet", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "book", "clock",
    "vase", "scissors", "teddy bear", "hair drier", "toothbrush",
    "wine glass", "cup", "fork", "knife", "spoon", "bowl"
]
min_images_required_task1 = 35000
max_images_required_task1 = 40000
min_images_required = 20000
max_images_required = 20000
min_images_required_val = 1000
max_images_required_val = 1000
annotation_path1  =  '../annotations/instances_train2017.json'
annotation_path2  =  '../annotations/instances_val2017.json'
annotation_path_1 =  '../annotations/instances_train2017_processed.json'
annotation_path_2 =  '../annotations/instances_val2017_processed.json'
destination_path  =  '../json_coco_file/'
Class = [T1_COCO_CLASS_NAMES,T2_CLASS_NAMES,T3_CLASS_NAMES,T4_CLASS_NAMES]

Image_list_train_old =  [   destination_path+'image_list_train_old1.json',
                            destination_path+'image_list_train_old2.json',
                            destination_path+'image_list_train_old3.json',
                            destination_path+'image_list_train_old4.json']

Image_list_train =      [   destination_path+'image_list_blank.json',     # Create manually or code, which doesn't have any images. Content: []  
                            destination_path+'image_list_train_task1.json',
                            destination_path+'image_list_train_task2.json',
                            destination_path+'image_list_train_task3.json',
                            destination_path+'image_list_train_task4.json',
                            destination_path+'image_list_train_task0.json']

Image_list_val =        [   destination_path+'image_list_blank.json',     # Create manually or code, which doesn't have any images. Content: []  
                            destination_path+'image_list_val_task1.json',
                            destination_path+'image_list_val_task2.json',
                            destination_path+'image_list_val_task3.json',
                            destination_path+'image_list_val_task4.json'
                        ]

Old_version_evaluation =[   destination_path+'T1_instances_train_old.json',
                            destination_path+'T2_instances_train_old.json',
                            destination_path+'T3_instances_train_old.json',
                            destination_path+'T4_instances_train_old.json']

Spliting_file_name =    [   [destination_path+'T0_instances_train2017.json'],
                            [destination_path+'T1_instances_val2017.json',destination_path+'T1_instances_train2017.json'], 
                            [destination_path+'T2_instances_val2017.json',destination_path+'T2_instances_train2017.json'], 
                            [destination_path+'T3_instances_val2017.json',destination_path+'T3_instances_train2017.json'], 
                            [destination_path+'T4_instances_val2017.json',destination_path+'T4_instances_train2017.json']]
Spliting_file_name_2 =  [   destination_path+'T1_instance_train_new.json',
                            destination_path+'T2_instance_train_new.json',
                            destination_path+'T3_instance_train_new.json',
                            destination_path+'T4_instance_train_new.json'
                        ]
# Change id of annotation 

mk.process_coco_categories(annotation_path1, annotation_path_1, Class)
mk.process_coco_categories(annotation_path2, annotation_path_2, Class)

# Split the original COCO annotations file into 5 different task (only list of images)

# Train images file
slt.process_coco_annotations_task(annotation_path_1,Image_list_train[1], min_images_required_task1, max_images_required_task1, Class[0], Image_list_train[0])
slt.process_coco_annotations_task(annotation_path_1,Image_list_train[2], min_images_required, max_images_required, Class[1], Image_list_train[1])
slt.process_coco_annotations_task(annotation_path_1,Image_list_train[3], min_images_required, max_images_required, Class[2], Image_list_train[2])
slt.process_coco_annotations_task(annotation_path_1,Image_list_train[4], min_images_required, max_images_required, Class[3], Image_list_train[3])
slt.get_unique_images(annotation_path_1, Image_list_train[5], Image_list_train[:5])

# Validation images file
slt.process_coco_annotations_task(annotation_path_2,Image_list_val[1], min_images_required_val, max_images_required_val, Class[0], Image_list_val[0])
slt.process_coco_annotations_task(annotation_path_2,Image_list_val[2], min_images_required_val, max_images_required_val, Class[1], Image_list_val[1])
slt.process_coco_annotations_task(annotation_path_2,Image_list_val[3], min_images_required_val, max_images_required_val, Class[2], Image_list_val[2])
slt.process_coco_annotations_task(annotation_path_2,Image_list_val[4], min_images_required_val, max_images_required_val, Class[3], Image_list_val[3])

# Old version of evaluation images file
oe.process_coco_annotations_task(annotation_path_1,Image_list_train_old[0],Class[0])
oe.process_coco_annotations_task(annotation_path_1,Image_list_train_old[1],Class[1])
oe.process_coco_annotations_task(annotation_path_1,Image_list_train_old[2],Class[2])
oe.process_coco_annotations_task(annotation_path_1,Image_list_train_old[3],Class[3])

# Process into COCO format
# Split coco files train

mk.process_coco_annotations_task(annotation_path_1, Spliting_file_name[1][1], Image_list_train[1], Class[0], [])
mk.process_coco_annotations_task(annotation_path_1, Spliting_file_name[2][1], Image_list_train[2], Class[1], [Class[0]])
mk.process_coco_annotations_task(annotation_path_1, Spliting_file_name[3][1], Image_list_train[3], Class[2], [Class[0],Class[1]])
mk.process_coco_annotations_task(annotation_path_1, Spliting_file_name[4][1], Image_list_train[4], Class[3], [Class[0],Class[1],Class[2]])
mk.process_coco_annotations_unknown(annotation_path_1, Spliting_file_name[0][0], Image_list_train[5])

# Split coco files val
mk.process_coco_annotations_task_val(annotation_path_2, Spliting_file_name[1][0], Image_list_val[1], Class[0])
mk.process_coco_annotations_task_val(annotation_path_2, Spliting_file_name[2][0], Image_list_val[2], Class[1])
mk.process_coco_annotations_task_val(annotation_path_2, Spliting_file_name[3][0], Image_list_val[3], Class[2])
mk.process_coco_annotations_task_val(annotation_path_2, Spliting_file_name[4][0], Image_list_val[4], Class[3])

# Old version of evaluation images file
mk.process_coco_annotations_task_val(annotation_path_1, Old_version_evaluation[0], Image_list_train_old[0], Class[0])
mk.process_coco_annotations_task_val(annotation_path_1, Old_version_evaluation[1], Image_list_train_old[1], Class[1])
mk.process_coco_annotations_task_val(annotation_path_1, Old_version_evaluation[2], Image_list_train_old[2], Class[2])
mk.process_coco_annotations_task_val(annotation_path_1, Old_version_evaluation[3], Image_list_train_old[3], Class[3])

# Keep minimum instance in previous task (training one)
mk.process_coco_annotations_adding(Spliting_file_name[1][1], annotation_path_1,Spliting_file_name_2[0], Class[0], [],max_images_required,Image_list_train[1]) 
mk.process_coco_annotations_adding(Spliting_file_name[2][1], annotation_path_1,Spliting_file_name_2[1], Class[1], [Class[0]],max_images_required,Image_list_train[1])
mk.process_coco_annotations_adding(Spliting_file_name[3][1], annotation_path_1,Spliting_file_name_2[2], Class[2], [Class[0],Class[1]],max_images_required,Image_list_train[1])
mk.process_coco_annotations_adding(Spliting_file_name[4][1], annotation_path_1,Spliting_file_name_2[3], Class[3], [Class[0],Class[1],Class[2]],max_images_required,Image_list_train[1])

# Compress the file 
for file_group in Spliting_file_name:
    for file_path in file_group:
        mk.compress_coco_json(file_path)
 
for file_path in Spliting_file_name_2:
    mk.compress_coco_json(file_path)
for Old_version in Old_version_evaluation:
    mk.compress_coco_json(Old_version)
# Test out
# Save a statistic file for COCO processing file
ins.task_statistic(annotation_path_1, Class, destination_path+'task_statistic1.txt')
ins.task_statistic(annotation_path_2, Class, destination_path+'task_statistic2.txt')
print("Original stats of the COCO dataset")
ins.print_coco_categories_and_instances(annotation_path1)

print("Stats of the COCO dataset after changing the category IDs")
ins.print_coco_categories_and_instances(annotation_path_1)

# Save a statistic file for each task
print("Stats of the COCO dataset in each task")
combined_output = []
for file_group in Spliting_file_name:
    for file_path in file_group:
        combined_output.append("Task")  # This adds "Task" as a header for each file
        task_output = ins.get_coco_categories_and_instances(file_path)
        combined_output.append(task_output)  # Collect the result from each file

for file_path in Spliting_file_name_2:
    combined_output.append("Stats of new file trained processed")
    task_output=ins.get_coco_categories_and_instances(file_path)
    combined_output.append(task_output)

final_output = "\n".join(combined_output)    # Join all the outputs with new lines separating them

# Save the combined output to a text file
with open(destination_path+'task_statistic.txt', 'w') as f:
    f.write(final_output)

# Save a statistic file for old version of evaluation
combined_output = []
duplicate_percentages = ins.calculate_duplicate_percentages(Image_list_train_old, destination_path + 'Duplicate_evaluation.txt')
combined_output.append("Duplicate Percentages:")
import json
combined_output.append(json.dumps(duplicate_percentages, indent=4))  

# Join all the outputs with new lines separating them
combined_output = "\n".join(combined_output)

with open(destination_path+'task_statistic1.txt', 'a') as f:
    f.write(combined_output)

combined_output = []
duplicate_percentages = ins.calculate_duplicate_percentages(Image_list_train, destination_path + 'Duplicate_evaluation.txt')
combined_output.append("Duplicate Percentages:")
combined_output.append(json.dumps(duplicate_percentages, indent=4))  

# Join all the outputs with new lines separating them
combined_output = "\n".join(combined_output)

with open(destination_path+'Quality.txt', 'a') as f:
    f.write(combined_output)


# All comment below are for testing, validate and give an example of how to use the function

# mk.masking_json(annotation_path_1, destination_path+spliting_file_name[1], Class[1], num_images= 3000) 
# slt.filter_and_select_images(destination_path+spliting_file_name[1], '../json_coco_file/T2_instances_train2017_split_revised.json', [20000, 50000], Class[1])
# ins.count_categories('../json_coco_file/T2_instances_train2017_split_revised.json')
# ins.count_categories('../json_coco_file/T2_instances_train2017_split.json')
# ins.total_images_check(destination_path+spliting_file_name[1],destination_file_path=destination_path, classes=Class[1].append("unknown"), file_name='T2_total_images.csv')
# ins.count_annotation(destination_path+spliting_file_name[1], destination_file_path =destination_path, file_name='T2_annotation.csv')
# slt.process_coco_annotations_task(annotation_path_1,destination_path+'image_list_train_task1.json', min_images_required, max_images_required, T1_COCO_CLASS_NAMES)
# ins.count_categories('../json_coco_file/T1_instances_train2017_split.json')
# ins.count_annotation(annotation_file, dest_file, 'category_bruh.csv')
# ins.total_images_check(annotation_file, dest_file, T1_COCO_CLASS_NAMES, 'total_images.csv')
