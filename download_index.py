import os
import os.path as osp
import urllib.request
from xml.dom.minidom import parse

root_url = "https://multimedia-commons.s3-us-west-2.amazonaws.com/?delimiter=/&prefix="


def download(prefix, path):
    url = root_url + prefix
    print("Download {}".format(url))
    urllib.request.urlretrieve(url, path)
    return path


def collect(prefix):
    if not osp.isdir(prefix):
        os.makedirs(prefix)

    # Get index xml file
    index = prefix + "index.xml"
    if not osp.isfile(index):
        download(prefix, index)

    # Parse index xml file
    children = [common_prefix.getElementsByTagName("Prefix")[0].firstChild.data for common_prefix
                in parse(open(index)).getElementsByTagName("CommonPrefixes")]
    for child_prefix in children:
        collect(child_prefix)


if __name__ == '__main__':
    print("Download index files of YFCC100M")
    collect("data/")
