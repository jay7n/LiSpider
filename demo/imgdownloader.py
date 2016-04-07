# -*- coding: utf-8 -*-

import logging
import os
import sys

try:  # for python3
    import urllib.request as urllib
except ImportError:
    import urllib as urllib

from lispider import Spider
import demo.imgdownloader_config as config

logger = logging.getLogger()


def main():
    dir = os.path.join(os.path.dirname(__file__), config.ImgDownloader['ImgStoreRelPath'])
    if os.path.exists(dir):
        print('error: the designate folder has existed. please specify a new one instead.')
        return

    spider = Spider(config)
    vars = spider.Run()

    if 'Img' in vars and 'Title' in vars:
        logger.debug(vars['Img'])
        logger.debug(vars['Title'])
        logger.debug(vars['Desc'])

        os.mkdir(dir)
        fileName = None

        for idx, imgLink in enumerate(vars['Img']):
            imgLink = 'http:' + imgLink if imgLink and imgLink[0:2] == '//' else imgLink

            if 'FileNamePattern' in config.ImgDownloader:
                baseName, suffix = config.ImgDownloader['FileNamePattern']
                fileName = baseName + str(idx) + '.' + suffix
            else:
                fileName = imgLink.split('/')[-1]

            fileName = os.path.join(dir, fileName)
            urllib.urlretrieve(imgLink, fileName)

        print('done.')
    else:
        print('No \'Img\' elements found')

if __name__ == '__main__':
    main()
