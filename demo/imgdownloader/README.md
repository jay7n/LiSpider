# ImgDownloader

[ImgDownloader](demo/imgdownloader) is a program to scrape images from web pages (from [xkcd.com](xkcd.com) website as the example, and of course you can instead replace with any other sites you like). By utiling __LiSpider__ to extract the image links in batch, it can easily download the image source files using whatever a relevant python lib (_'urllib.urlretrieve'_ is used in this demo).

[ImgDownloader](demo/imgdownloader) will download the images and package them into a directory you specified, which you can pin in the end of the config file that LiSpider uses. Beyond that you can also specify what conventions the downloaded file names will follow. Below is the example used in this demo:

``` python
ImgDownloader = {
    'ImgStoreRelPath': 'xkcd1',
    # 'FileNamePattern': ('page_', 'jpeg')
}
```

uncomment __'FileNamePattern'__ to enable customizing file naming. It's a python tuple: a file prefix with a suffix. The undersocre '\_' will be followed by a number indicating the image indices downloaded in order.
