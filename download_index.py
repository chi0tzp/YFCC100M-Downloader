import sys
import os
import os.path as osp
import urllib.request
from xml.dom.minidom import parse
from multiprocessing import Pool
from tqdm import tqdm

root_url = "https://multimedia-commons.s3-us-west-2.amazonaws.com/?delimiter=/&prefix="
img_error_file = 'image_errors.log'
img_errors = 0
vid_error_file = 'video_errors.log'
# vid_errors


def get_img_index(d):
    global img_errors
    os.makedirs(d, exist_ok=True)
    index = osp.join(d, "index.xml")
    if not osp.isfile(index):
        try:
            urllib.request.urlretrieve(root_url + d, index)
        except:
            with open(img_error_file, "a") as f:
                f.write("{}\n".format(root_url + d))
                img_errors += 1


if __name__ == '__main__':
    # Create data/ directory and download root index xml file
    print("#.Create data/ directory and download the root index xml file...")
    os.makedirs("data/", exist_ok=True)
    urllib.request.urlretrieve(root_url + "data/index.xml", "data/index.xml")

    # Create images subdir under data/ and download the corresponding index.xml file
    print("#.Create data/images/ directory and download images index file...")
    os.makedirs("data/images/", exist_ok=True)
    if not osp.isfile("data/images/index.xml"):
        urllib.request.urlretrieve(root_url + "data/images/", "data/images/index.xml")

    print("  \\__Get image directories list...", end="")
    image_directories = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                         in parse(open("data/images/index.xml")).getElementsByTagName("CommonPrefixes")]
    print("{} image directories".format(len(image_directories)))

    # Create videos subdir under data/ and download the corresponding index.xml file
    print("#.Create data/videos/ directory and download videos index file...")
    os.makedirs("data/videos/", exist_ok=True)
    print("  \\__Get video directories list...", end="")
    if not osp.isfile("data/videos/index.xml"):
        urllib.request.urlretrieve(root_url + "data/videos/", "data/videos/index.xml")
    video_directories = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                         in parse(open("data/videos/index.xml")).getElementsByTagName("CommonPrefixes")]
    print("{} video directories".format(len(video_directories)))

    print("#.Download image directories...")
    if osp.exists(img_error_file):
        os.remove(img_error_file)
    for i in tqdm(range(len(image_directories))):
        cur_img_dir = image_directories[i]
        # Create current image directory and get subdir list
        os.makedirs(image_directories[i], exist_ok=True)
        cur_img_dir_index = osp.join(cur_img_dir, 'index.xml')
        if not osp.isfile(cur_img_dir_index):
            urllib.request.urlretrieve(root_url + cur_img_dir, cur_img_dir_index)
        cur_img_dir_subdirs = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                               in parse(open(cur_img_dir_index)).getElementsByTagName("CommonPrefixes")]
        # Download subdirs of current directory using multi-threading
        # Use the maximum number of the available threads -- for specifying the number of threads, call Pool() as
        # pool = Pool(processes=<num_of_workers>), e.g., pool = Pool(processes=4)
        pool = Pool()
        pool.map(get_img_index, cur_img_dir_subdirs)
        pool.close()

    print("  \\__Done! Errors for {} image index files".format(img_errors))
