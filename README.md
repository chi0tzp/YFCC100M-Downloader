# YFCC100M Downloader

A set of Python3 scripts for downloading (using **multiprocessing**) the [YFCC100M dataset](https://multimediacommons.wordpress.com/yfcc100m-core-dataset/). The YFCC100M is the largest publicly and freely useable multimedia  collection, containing  the metadata of around 99.2 million photos and  0.8 million videos from [Flickr](https://www.flickr.com/), all of which were shared under one of the various [Creative Commons](https://creativecommons.org/) licenses.

**Step 1**: Download dataset index files:

~~~
python3 download_index.py --subset=<subset>
~~~

`subset` defines the subset of the dataset, for which index files will be downloaded. It can be `images`, `videos`, or `both`.

After downloading index files, the basic file structure of the dataset will have been created under `data/` directory, as follows:

~~~
TODO: add tree structure of data/ 
~~~



**Step 2**: Download dataset image and/or video files:

~~~
python3 download_files.py
~~~