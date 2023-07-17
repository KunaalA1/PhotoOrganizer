
import os
import numpy as np
import cv2
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import shutil

#System Design:
#Process Images:
#Ask for how you want to organize the images
#Open up each image, and process them
#

status = 1
def main(): 
    program_exit = False
    while(program_exit == False):
        selection = input(print_menu(status))
        if(selection == "1"):
            valid_selection = False
            while(valid_selection is False):
                user_select = input("What folder do you want to organize: {}\n".format(next(os.walk('.'))[1]))
                if user_select in os.listdir():
                    print("{} has been selected\n".format(user_select))
                    valid_selection = True
                else: 
                    print("not a valid selection")
            valid_arr = valid_filter(user_select)
            get_image_taken_similarity(valid_arr, user_select)
            
                
                
            #for image in valid_arr:
            #    print(image)
        elif(selection == "2"):
            program_exit = True
        else:
            print("Not a valid selection, try again\n")

    return


def print_organization():
    print("How do you want to organize the images\n")
    print("1. Date Taken\n")
    print("2. Geolocation\n")
    print("3. Similarity\n")
    return "Selection: "
     

def print_menu(status):
#    result = pyfiglet.figlet_format("Photo Organizer", font = "3-d")
#    print(result)
#     
    print("1. Process Images\n")
    print("2. Exit Program\n")
    return "Selection: "

def valid_filter(dir):
    valid_array = []
    file_array = os.listdir(os.path.abspath(dir))
    for file in file_array:
        if(file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")):
            file_path = os.path.abspath(dir) + "/{}".format(file)
            valid_array.append(file_path)
    return valid_array
            
#def similarity_process(img_array):
'''
def get_image_taken_date(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is not None:
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            print(tag_name, ":", value)
'''


#exif_data returns hex keys: 296=0x0128, 34665 =
def create_color_histogram(image):
    #calculate color histogram for the image.
    color_hist = cv2.calcHist([image], [0,1,2], None, [64,64,64], [0,256,0,256,0,256])
    cv2.normalize(color_hist, color_hist, 255, cv2.NORM_MINMAX)
    return color_hist.flatten()

def histogram_intersection(hist1, hist2):
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
#get_image_taken_similarity: takes the image list, uses, cv2 to 
def get_image_taken_similarity(valid_arr, user_select):

    histogram_dict = {}
    for image in valid_arr:
        im = cv2.imread(image)
        histogram_dict[image] = create_color_histogram(im)
    data = list(histogram_dict.values())
    linkage_data = linkage(data, method = 'ward', metric='euclidean')
    dendrogram(linkage_data)
    threshold = 5
    labels = fcluster(linkage_data, t = threshold, criterion="distance")
    #process the color histograms of each histogram and cluster them together with the agglomerative clustering algorithm

    new_dict = {}
    im_list = list(histogram_dict.keys())
    for i in range(len(labels)):
        new_dict[im_list[i]] = labels[i]
    superlist = []
    #map images with the label given by the agglomerative clustering algorithm
    highest = max(labels)
    print(highest)
    #need to get the highest value in labels

    for i in range(highest):
        sublist = []
        for key in new_dict:
            print(key)
            if new_dict[key] == i+1:
                sublist.append(key)
        superlist.append(sublist)
    print(superlist)
    #Process dictionary data to separate into different folders

    counter = 1
    for folder in superlist:
        os.mkdir(os.path.abspath(user_select) + "/folder{}/".format(counter))
        for file in folder:
            path = os.path.abspath(file)
            new_path = os.path.dirname(file) + "/folder{}/".format(counter) + os.path.basename(file).split('/')[-1]
            shutil.move(path, new_path)
        counter += 1
    #the statement creates a new directory for each item in the superlist, then you need to move the files in each sublist into its new folder
    
    
#I want this code to be able to iterate through the dictionary, and compare the i/k/jth dictionary value to the curr_val, which is a value that is the first value to not be set to 1. the reason it should not be set to 1 is because

if __name__ == "__main__":
    main()