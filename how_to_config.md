# How to Set up Your Configs

* ## Specify the urls of web pages which your're interested in scraping

    You need to specify which one (or which ones) web page(s) you want to scrape.  

    For example you're going to take some image samples from [xkcd.com](xkcd.com). According to the assumption of your knowledge to this site, you already know each page has been assigned to an well encoded url, most of which look like this :

    > http://xkcd.com/706/  
    > http://xkcd.com/707/  
    > http://xkcd.com/708/  
    > ......

    And each page has been filled up in with an image telling a funny yet great story. Your purpose is just to extract these image links (which is of course a html element). So first you need to tell the spider where you want to pick them up.

    ``` python
    GrabHtmlContent = {
        'URLScope': [
            'http://xkcd.com/706',
            'http://xkcd.com/707',
            'http://xkcd.com/708',
        ],
        'MaxTryCount': 5
    }
    ```

    The key __URLScope__ in __GrabHtmlContent__ corresponds to a list where you can put as many as you can url items. The spider will loop for this list to get the interested html elements.

    __MaxTryCount__ means that sometimes there're some glitches in opening the url link and then how many times you would like to let the spider try once again. In this example we give it 5 times to try each page.

    Often we have a sense that in fact the pages we're taking are aligned by orders. For example here they're 706-708, so it's not necessary to specify each ordered page one by one actually. You can make things easy by using __Template Specifier "%"__ (The idea is inspired by _Jinja2_):

    ``` python
    GrabHtmlContent = {
        'URLScope': [
            'http://xkcd.com/%706-708%/',
            'http://xkcd.com/100/', # this gives you the idea that you can combine both styles.
        ],
        'MaxTryCount': 5
    }
    ```


* ## Specify the html template that fits your interests

    Also you need to make it clear which specific one (or ones) html element(s) in the web page you'd like to extract. Well, this requires you to have some html/css skills ( having the web design background is better ! ), but managing them is quite simple.

    In the [xkcd.com](xkcd.com) case above, through web analysis tool, e.g. _Chroms's "Developer Tools_", you spot and find the elements lie somewhere like here:

    ``` html
    <div id="ctitle">Freedom</div>
    ```

    as well as :

    ``` html
    <div id="comic">
        <img src="//imgs.xkcd.com/comics/freedom.png" title="Sometimes I'm terrified to realize how many options other people have." alt="Freedom">
    </div>
    ```

    Take an example here, the value of "_img src_" is the exact part you're looking for: "_//imgs.xkcd.com/comics/freedom.png_".

    In most cases you can paste this link in your browser and then you see the result. But after all, That has nothing to do with the business here. Here what the magic power of LiSpider provides you with is an automatic ability to gather this kind of elements in batch.

    To get things done with LiSpider you need to define your own __Template Variables (bracketed with "%")__, like such:

    ``` python
    HitTemplate = {
        'Elements': [
            u'''
                <div id="ctitle">%Title%</div>
            ''',

            u'''
                <div id="comic">
                    <img src="%Img%" title="%Desc%" alt="%%">
                    <lisp_pass>
                </div>
            ''',
        ]
    }
    ```

    LiSpider will scan all the pages you specify in __"URLScope"__ and look for all elements that hit the template html elements here(__'Elements'__ in __'HitTemplate'__). When encountering a temmplate variable like _"%Title%"_, _"%Img%"_ or _"%Desc%"_, it will gather their values in a list, respectively, and wrap these lists with the vairable names in a dict. Finally LiSpider will give this dict back to you.

    Note that __'Elements'__ is a list so that you can include as many as elements as your interests hit points. In this case there're 2 elements seen as the templates.

    So in the end you will get a dict like such:

    ``` python
    {
        ''
        'Title': ['Freedom', ], # and with others if any
        'Img': ['//imgs.xkcd.com/comics/freedom.png', ], # and with others if any
        'Desc': ["Sometimes I'm terrified to realize how many options other people have.", ], # and with others if any
    }
    ```

    In addition to these regular template variables, and as you've maybe already noted,  there are some other indications: __"%%"__ and __"&lt;lisp_pass>"__ sepcificlly. __"%%"__ is an empty template variable meaning that whatever its actual value is, this value will always get passed the test under no conditions. This is very useful when you lock down one element as the target yet don't care about some specific attributes(like 'id' for example, which differs from one to another).

    __"&lt;lisp_pass>"__ also serves the similar purpose as __"%%"__, but in a higher level. It means the entire element whose locatoin matches here will be totally ignored and seen as passed. Sometimes you will focus on extracting an element's child node, but indifferent to its sibling nodes. Then for those siblings you can replace them with __"&lt;lisp_pass>"__. The name __"lisp"__ is just a joke, it means __"lispider"__ actually, not the language you've ever heard of :)


* ## Specify others if you'd like to take care

    There're some other options you can set, and you can safely ignore them if you're satified with the default settings for them.

    ``` python
    ParseHtmlContent =
    {
        # 'html5lib', 'lxml', 'xml', 'html.parser'
        'BeautifulSoupParser': 'html5lib'
    }

    Debug = {
        'LoggingLevel': 'WARNING'
    }
    ```

    LiSpider uses _BeautifulSoup_ as the tool to cope with html elements. So you can specify a parser which is recognized by _BeautifulSoup_. By default this parser(__'BeautifulSoupParser'__ in __'ParseHtmlContent'__) is set as _'html5lib'_, orienting the modern html world. But sometimes you'll encounter some html contents written in old and dirty ways(html4), then you can change another parser instead (like _'html.parser'_).

    If something goes wrong and maybe you need to get access to the working status of LiSpider thourgh logging. You can then set the __'LoggingLevel'__ in __'Debug'__ dict as _'DEBUG'_. By default this value is set as _'WARNING'_


So basically after all these configs get done, the config file looks like this:

```
# Configs Specific to LiSpider
#
# GrabHtmlContent - Mandatory
GrabHtmlContent = {
    'URLScope': [
        'http://xkcd.com/%706-708%/',
        'http://xkcd.com/100/',
    ],
    'MaxTryCount': 5
}

# HitTemplate - Mandatory
HitTemplate = {
    'Elements': [
        u'''
            <div id="ctitle">%Title%</div>
        ''',

        u'''
            <div id="comic">
                <img src="%Img%" title="%Desc%" alt="%%">
                <lisp_pass>
            </div>
        ''',
    ]
}

# ParseHtmlContent - Optional
ParseHtmlContent = {
    # 'html5lib', 'lxml', 'xml', 'html.parser'
    'BeautifulSoupParser': 'html5lib'
}

# Debug - Optional
Debug = {
    'LoggingLevel': 'WARNING'
}
```
