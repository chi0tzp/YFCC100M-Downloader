# YFCC100M Downloader

This repo provides a pair of Python3 scripts for downloading (using **multiprocessing**) the [YFCC100M dataset](https://multimediacommons.wordpress.com/yfcc100m-core-dataset/). The YFCC100M is a large publicly and freely usable multimedia collection, containing  the metadata of around 99.2 million photos and  0.8 million videos from [Flickr](https://www.flickr.com/), all of which were shared under one of the various [Creative Commons](https://creativecommons.org/) licenses.



**Step 1**: Download dataset index files:

~~~
python3 download_index.py --subset=<subset>
~~~

`subset` defines the subset of the dataset, for which index files will be downloaded. It can be `images`, `videos`, or `both` (by default).

After downloading index files, the basic file structure of the dataset will have been created under `data/` directory. At this point, the structure contains only the index files, which will be used by the second script (`download_files.py`) in order to download dataset's actual files under the same structure.



**Step 2**: Download dataset files:

~~~
python3 download_files.py
~~~