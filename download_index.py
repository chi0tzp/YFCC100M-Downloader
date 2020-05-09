import sys
import sys
import os
import os.path as osp
import argparse
import urllib.request
from xml.dom.minidom import parse
from multiprocessing import Pool
from tqdm import tqdm

root_url = "https://multimedia-commons.s3-us-west-2.amazonaws.com/?delimiter=/&prefix="
error_file = 'index_errors.log'
errors = 0


def get_index(d):
    global errors
    os.makedirs(d, exist_ok=True)
    index = osp.join(d, "index.xml")
    if not osp.isfile(index):
        try:
            urllib.request.urlretrieve(root_url + d, index)
        except:
            with open(error_file, "a") as f:
                f.write("{}\n".format(root_url + d))
                errors += 1


if __name__ == '__main__':
    # Set up a parser for command line arguments
    parser = argparse.ArgumentParser("Download index files for YFCC100M")
    parser.add_argument('-s', '--subset', type=str, default='both', choices=('images', 'videos'), help="")
    args = parser.parse_args()

    # Create data/ directory and download root index xml file
    print("#.Create data/ directory and download the root index xml file...")
    os.makedirs("data/", exist_ok=True)
    urllib.request.urlretrieve(root_url + "data/index.xml", "data/index.xml")

    # === Download index files for images subset
    if args.subset in ('images', 'both'):
        # Create images subdir under data/ and download the corresponding index.xml file
        print("#.Create data/images/ directory and download images index file...")
        os.makedirs("data/images/", exist_ok=True)
        if not osp.isfile("data/images/index.xml"):
            urllib.request.urlretrieve(root_url + "data/images/", "data/images/index.xml")

        print("  \\__Get image directories list...", end="")
        image_directories = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                             in parse(open("data/images/index.xml")).getElementsByTagName("CommonPrefixes")]
        print("{} image directories".format(len(image_directories)))

        print("#.Download image directories...")
        if osp.exists(error_file):
            os.remove(error_file)
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
            pool.map(get_index, cur_img_dir_subdirs)
            pool.close()
        print("  \\__Done! Errors for {} image index files.".format(errors))
        if errors > 0:
            print("      Run the script again until no errors found.")

    # === TODO: Download index files for videos subset
    if args.subset in ('videos', 'both'):
        # Create videos subdir under data/ and download the corresponding index.xml file
        print("#.Create data/videos/ directory and download videos index file...")
        os.makedirs("data/videos/", exist_ok=True)
        print("  \\__.Get video categories...")
        if not osp.isfile("data/videos/index.xml"):
            urllib.request.urlretrieve(root_url + "data/videos/", "data/videos/index.xml")
        video_dir_categories = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                                in parse(open("data/videos/index.xml")).getElementsByTagName("CommonPrefixes")]
        # =============================================================
        # Get data/videos/keyframes/
        print("       \\__.Get {}...".format(video_dir_categories[0]))
        keyframes_dir = video_dir_categories[0]
        # Create keyframes directory and get subdir list
        os.makedirs(keyframes_dir, exist_ok=True)
        keyframes_dir_index = osp.join(keyframes_dir, 'index.xml')
        if not osp.isfile(keyframes_dir_index):
            urllib.request.urlretrieve(root_url + keyframes_dir, keyframes_dir_index)
        keyframes_dir_subdirs = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                                 in parse(open(keyframes_dir_index)).getElementsByTagName("CommonPrefixes")]
        # Download subdirs of keyframes directory using multi-threading
        # Use the maximum number of the available threads -- for specifying the number of threads, call Pool() as
        # pool = Pool(processes=<num_of_workers>), e.g., pool = Pool(processes=4)
        pool = Pool()
        pool.map(get_index, keyframes_dir_subdirs)
        pool.close()

        # Download keyframes subdirs
        for i in tqdm(range(len(keyframes_dir_subdirs))):
            cur_dir = keyframes_dir_subdirs[i]
            # Create current directory and get subdir list
            os.makedirs(cur_dir, exist_ok=True)
            cur_dir_index = osp.join(cur_dir, 'index.xml')
            if not osp.isfile(cur_dir_index):
                urllib.request.urlretrieve(root_url + cur_dir, cur_dir_index)
            cur_dir_subdirs = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                               in parse(open(cur_dir_index)).getElementsByTagName("CommonPrefixes")]
            # Download subdirs of current directory using multi-threading
            # Use the maximum number of the available threads -- for specifying the number of threads, call Pool() as
            # pool = Pool(processes=<num_of_workers>), e.g., pool = Pool(processes=4)
            pool = Pool()
            pool.map(get_index, cur_dir_subdirs)
            pool.close()

        # =============================================================
        # Get data/videos/metadata/
        print("       \\__.Get {}...".format(video_dir_categories[1]))
        metadata_dir = video_dir_categories[1]
        # Create metadata directory and get subdir list
        os.makedirs(metadata_dir, exist_ok=True)
        metadata_dir_index = osp.join(metadata_dir, 'index.xml')
        if not osp.isfile(metadata_dir_index):
            urllib.request.urlretrieve(root_url + metadata_dir, metadata_dir_index)
        # metadata_dir_subdirs = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
        #                         in parse(open(metadata_dir_index)).getElementsByTagName("CommonPrefixes")]
        # print("metadata_dir_subdirs: {}".format(metadata_dir_subdirs))
        #
        # # Download subdirs of metadata directory using multi-threading
        # # Use the maximum number of the available threads -- for specifying the number of threads, call Pool() as
        # # pool = Pool(processes=<num_of_workers>), e.g., pool = Pool(processes=4)
        # pool = Pool()
        # pool.map(get_index, metadata_dir_subdirs)
        # pool.close()
        #
        # # Download metadata subdirs
        # for i in tqdm(range(len(metadata_dir_subdirs))):
        #     cur_dir = metadata_dir_subdirs[i]
        #     # Create current directory and get subdir list
        #     os.makedirs(cur_dir, exist_ok=True)
        #     cur_dir_index = osp.join(cur_dir, 'index.xml')
        #     if not osp.isfile(cur_dir_index):
        #         urllib.request.urlretrieve(root_url + cur_dir, cur_dir_index)
        #     cur_dir_subdirs = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
        #                        in parse(open(cur_dir_index)).getElementsByTagName("CommonPrefixes")]
        #     # Download subdirs of current directory using multi-threading
        #     # Use the maximum number of the available threads -- for specifying the number of threads, call Pool() as
        #     # pool = Pool(processes=<num_of_workers>), e.g., pool = Pool(processes=4)
        #     pool = Pool()
        #     pool.map(get_index, cur_dir_subdirs)
        #     pool.close()
        #     break

        # =============================================================
        # Get data/videos/mp4/
        print("       \\__.Get {}...".format(video_dir_categories[2]))
        mp4_dir = video_dir_categories[2]
        # Create mp4 directory and get subdir list
        os.makedirs(mp4_dir, exist_ok=True)
        mp4_dir_index = osp.join(mp4_dir, 'index.xml')
        if not osp.isfile(mp4_dir_index):
            urllib.request.urlretrieve(root_url + mp4_dir, mp4_dir_index)
        mp4_dir_subdirs = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                           in parse(open(mp4_dir_index)).getElementsByTagName("CommonPrefixes")]
        # Download subdirs of mp4 directory using multi-threading
        # Use the maximum number of the available threads -- for specifying the number of threads, call Pool() as
        # pool = Pool(processes=<num_of_workers>), e.g., pool = Pool(processes=4)
        pool = Pool()
        pool.map(get_index, mp4_dir_subdirs)
        pool.close()

        # Download mp4 subdirs
        for i in tqdm(range(len(mp4_dir_subdirs))):
            cur_dir = mp4_dir_subdirs[i]
            # Create current directory and get subdir list
            os.makedirs(cur_dir, exist_ok=True)
            cur_dir_index = osp.join(cur_dir, 'index.xml')
            if not osp.isfile(cur_dir_index):
                urllib.request.urlretrieve(root_url + cur_dir, cur_dir_index)
            cur_dir_subdirs = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                               in parse(open(cur_dir_index)).getElementsByTagName("CommonPrefixes")]
            # Download subdirs of current directory using multi-threading
            # Use the maximum number of the available threads -- for specifying the number of threads, call Pool() as
            # pool = Pool(processes=<num_of_workers>), e.g., pool = Pool(processes=4)
            pool = Pool()
            pool.map(get_index, cur_dir_subdirs)
            pool.close()
