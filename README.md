# LiSpiderLiSpider is a lightweight python module that is used to ease the effort of scraping/extracting HTML elements. By just specifying some of your customized Template Varible as the HTML elements attributes/texts, then all of them presents to you as a well-wrapped python dict object.![intro](intro.png)## InstallLiSpider has not been uploaded to PyPI currently, but you can download the wheel package [lispider-0.1.dev0.tar.gz](https://github.com/jay7n/LiSpider/blob/master/dist/lispider-0.1.dev0.tar.gz) (click _'View Raw'_ in case you have no idea how to), and install it using your favorite pip.```    pip install lispider-0.1.dev0.tar.gz```## Usage### Setup Your Config file firstBefore using LiSpider you need to set up your configs by a file.It is helpful to take some time to read this ["How To Config"](how_to_config.md) tutorial, which takes an famous website: [xkcd.com](xkcd.com) as the example to show you how to scrape some info on it.### Run LiSpider with Your Config fileWith the config file prepared well, you need to import the spider module and the config file first.Feed the spider with the config and activate it by calling its '_Run()_' method, then the spider will orgnize all your interests as a python dict object and return it to you.``` pythonfrom lispider import Spiderimport your_config as configspider = Spider(config)results = spider.Run()print(results)```In the above example's circumstance you're supposed to see the results as this (formatted here for a better looking):``` python{u'Desc':    [u"Sometimes I'm terrified to realize how many options other people have.",     u"You'll be moved up from 49 of ~7 billion to 31 of ~7 billion.",     u'You roll for initiative, and ... [roll] ... wow, do you ever take it.',     u"This was my friend David's idea"],u'Img':    [u'//imgs.xkcd.com/comics/freedom.png',     u'//imgs.xkcd.com/comics/joshing.png',     u'//imgs.xkcd.com/comics/sex_dice.png',     u'//imgs.xkcd.com/comics/family_circus.jpg'],u'Title':    [u'Freedom',     u'Joshing',     u'Sex Dice',     u'Family Circus']}```## Demos* ### [ImgDownloader](demo/imgdownloader)* ### RssChef (TODO)## What's Next1. Use json instead of python script itself as a more flexible config format* Add a multithread-worker to improve the scraping performance.* Add a js-evaluater to parse the javascript embedded in the html elements so as to get the final true html elements.* Guard the various exceptions in a more robust level.* Prepare to apply to PyPI.