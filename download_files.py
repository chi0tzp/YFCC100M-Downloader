import sys
import os
import urllib.request
from xml.dom.minidom import parse
import argparse
import multiprocessing
from multiprocessing import Pool
from tqdm import tqdm


root_url = "https://multimedia-commons.s3-us-west-2.amazonaws.com/"
error_file = 'file_errors.log'
errors = 0
erroneous_index_files = 0
manager = multiprocessing.Manager()
paths = manager.list()


def get_file(p):
    global errors
    if not os.path.isfile(p):
        try:
            urllib.request.urlretrieve(root_url + p, p)
        except:
            with open(error_file, "a") as f:
                f.write("{}\n".format(root_url + p))
                errors += 1


def get_paths(index_f):
    global erroneous_index_files
    try:
        for content in parse(open(index_f)).getElementsByTagName("Contents"):
            paths.append(content.getElementsByTagName("Key")[0].firstChild.data)
    except:
        erroneous_index_files += 1


if __name__ == '__main__':
    # Set up a parser for command line arguments

    parser = argparse.ArgumentParser("Download files for YFCC100M")
    # TODO: choose for which subset ('images', 'videos', or 'both') to download dataset files
    # parser.add_argument('-s', '--subset', type=str, default='both', choices=('images', 'videos', 'both'),
    #                     help="Choose dataset subset to be downloaded")
    parser.add_argument('-w', '--workers', type=int, default=None, help="Set number of multiprocessing workers")
    args = parser.parse_args()

    # TODO: parallelize this, if possible
    print("#.Collect index files in data/...")
    index_files = []
    for root, subdirs, files in os.walk("data/"):
        file_path = os.path.join(root, "index.xml")
        if os.path.exists(file_path):
            index_files.append(file_path)
    print("  \\__Found index files: {}".format(len(index_files)))

    print("#.Extract paths for files to be downloaded...")
    pool = Pool(args.workers)
    for _ in tqdm(pool.imap_unordered(get_paths, index_files), total=len(index_files)):
        pass
    pool.close()
    print("  \\__Found file paths: {}".format(len(paths)))
    print("  \\__Erroneous index files (e.g., empty): {}".format(erroneous_index_files))

    if erroneous_index_files > 0:
        print("     You may want to download again index files (i.e., run download_index.py again)")
        print("     This will attempt to recover any missing/erroneous index files.")
        print("     Any files included in erroneous index files will not be downloaded!")

        # Ask user for permission to continue downloading files or exit program
        while True:
            answer = input("Press enter to continue downloading files or 'q' to quit: ")
            if answer == "q":
                sys.exit()
            else:
                break

    print("#.Download files...")
    # Download files using multi-threading
    pool = Pool(args.workers)
    for _ in tqdm(pool.imap_unordered(get_file, paths), total=len(paths)):
        pass
    pool.close()
    print("  \\__Done! Errors for {} files.".format(errors))
    if errors > 0:
        print("      Run the script again until no errors found.")
