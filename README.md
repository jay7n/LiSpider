# LiSpiderLiSpider is a lightweight python module that is used to ease the effort of scraping/extracting HTML elements. By just specifying some of your customized Template Varible as the HTML elements attributes/texts, then all of them presents to you as a well-wrapped python dict object.## InstallLiSpider has not been uploaded to PyPI currently, but you can download the wheel package [lispider-0.1.dev0.tar.gz](https://github.com/jay7n/LiSpider/blob/master/dist/lispider-0.1.dev0.tar.gz) (click _'View Raw'_ in case you have no idea how to), and install it using your favorite pip.```    pip install lispider-0.1.dev0.tar.gz```## Usage### Config Your Config file first<ul><li> <h4> Specify the urls of web pages which your're interested in scraping </h4> </li>You need to specify which one (or which ones) web page(s) you want to scrape.``````<li> <h4> Specify the html template that fits your interests </h4> </li>Also you need to make it clear which specific one (or ones) html element(s) in the web page(s) you'd like to extract.``````<li> <h4> Specify others if you'd like </h4> </li>There're some other options you can set, and you can safely ignore them if you trust the default settings for them.``````So basically after all these configs get done, the config file looks like this:``````### Run LiSpider with Your Config fileWith the config file prepared well, you need to import the spider module and the config file first.Feed the spider with the config and activate it by calling its '_Run()_' method, then the spider will orgnize all your interests as a python dict object and return it to you.``` pythonfrom lispider import Spiderimport your_config as configspider = Spider(config)results = spider.Run()print(results)```In the above case's circumstance you're supposed to see the results as this:``````## Demos* ### ImgDownloader* ### RssChef## What Next1. Use json instead of python script itself as a more flexible config format* Add a multithread-worker to improve the scraping performance.* Add a js-evaluater to parse the javascript embedded in the html elements so as to extract the final results.