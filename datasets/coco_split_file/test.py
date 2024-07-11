import csv
import masking as mk
import instance as ins 
import select as slt

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
max_images_required_task1 = 35000
min_images_required = 21000
max_images_required = 21000
annotation_path =    '../annotations/instances_train2017.json'
destination_path =   '../json_coco_file/'

Class = [T1_COCO_CLASS_NAMES,T2_CLASS_NAMES,T3_CLASS_NAMES,T4_CLASS_NAMES]

Image_list = [destination_path+'image_list_blank.json',     # Create manually or code, which doesn't have any images. Content: []  
              destination_path+'image_list_task1.json',
              destination_path+'image_list_task2.json',
              destination_path+'image_list_task3.json',
              destination_path+'image_list_task4.json',
              destination_path+'image_list_task0.json']

Spliting_file_name =[destination_path+'T0_instances_train2017_split.json',
                     destination_path+'T1_instances_train2017_split.json', 
                     destination_path+'T2_instances_train2017_split.json', 
                     destination_path+'T3_instances_train2017_split.json', 
                     destination_path+'T4_instances_train2017_split.json']

# Split the original COCO annotations file into 5 different task (only list of images)

slt.process_coco_annotations_task(annotation_path,Image_list[1], min_images_required_task1, max_images_required_task1, Class[0], Image_list[0])
slt.process_coco_annotations_task(annotation_path,Image_list[2], min_images_required, max_images_required, Class[1], Image_list[1])
slt.process_coco_annotations_task(annotation_path,Image_list[3], min_images_required, max_images_required, Class[2], Image_list[2])
slt.process_coco_annotations_task(annotation_path,Image_list[4], min_images_required, max_images_required, Class[3], Image_list[3])
slt.get_unique_images(annotation_path, Image_list[5], Image_list[:5])

# Split coco files 
mk.process_coco_annotations_task(annotation_path, Spliting_file_name[1], Image_list[1], Class[0])
mk.process_coco_annotations_task(annotation_path, Spliting_file_name[2], Image_list[2], Class[1])
mk.process_coco_annotations_task(annotation_path, Spliting_file_name[3], Image_list[3], Class[2])
mk.process_coco_annotations_task(annotation_path, Spliting_file_name[4], Image_list[4], Class[3])
mk.process_coco_annotations_unknown(annotation_path, Spliting_file_name[0], Image_list[5])



# All comment below are for testing, validate and give an example of how to use the function

# mk.masking_json(annotation_path, destination_path+spliting_file_name[1], Class[1], num_images= 3000) 
# slt.filter_and_select_images(destination_path+spliting_file_name[1], '../json_coco_file/T2_instances_train2017_split_revised.json', [20000, 50000], Class[1])
# ins.count_categories('../json_coco_file/T2_instances_train2017_split_revised.json')
# ins.count_categories('../json_coco_file/T2_instances_train2017_split.json')
# ins.total_images_check(destination_path+spliting_file_name[1],destination_file_path=destination_path, classes=Class[1].append("unknown"), file_name='T2_total_images.csv')
# ins.count_annotation(destination_path+spliting_file_name[1], destination_file_path =destination_path, file_name='T2_annotation.csv')
# slt.process_coco_annotations_task(annotation_path,destination_path+'image_list_task1.json', min_images_required, max_images_required, T1_COCO_CLASS_NAMES)
# ins.count_categories('../json_coco_file/T1_instances_train2017_split.json')
# ins.count_annotation(annotation_file, dest_file, 'category_bruh.csv')
# ins.total_images_check(annotation_file, dest_file, T1_COCO_CLASS_NAMES, 'total_images.csv')