# Configs Specific to LiSpider
#
# GrabHtmlContent - Mandatory
GrabHtmlContent = {
    'URLScope': [
        'http://xkcd.com/%100-105%/'
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
                <img src="%Img%" title="%Desc%" alt=%%">
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


# Configs Specific to ImgDownloader
#
ImgDownloader = {
    'ImgStoreRelPath': 'xkcd1',
    # 'FileNamePattern': ('page_', 'jpeg')
}
