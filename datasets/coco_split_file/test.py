import csv
input_file = 'total_images.csv'

# Initialize a variable to store the total number of images
total_images = 0

# Read the CSV file and sum the counts
with open(input_file, mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        category_name, count = row
        total_images += int(count)

## idont know why 
print(f"Total number of images: {total_images}")