# -*- coding: utf-8 -*-

GrabHtmlContent = {
    'URLScope': [
        # 'http://jandan.net/ooxx/page-%1931-1920%#comments'
        'http://jandan.net/ooxx/page-1931#comments'
    ],
    'MaxTryCount': 5,
}

ParseHtmlContent = {
    # 'html5lib', 'lxml', 'xml', 'html.parser'
    'BeautifulSoupParser': 'html5lib'
}

# <div class="vote" id="%%"><span id="%%"></span><a title="%%" class="acvclick acv4" id="%%" href="%%">OO</a> [<span id="%%">5</span>] <a title="叉叉/反对" class="acvclick acva" id="%%" href="%%">XX</a> [<span id="%%">2</span>]<span class="time"><a href="javascript:;"> ↓吐槽 <span class="ds-thread-count" data-thread-key="%%" data-count-type="comments"> [1]</span></a></span></div>
# </div>

HitTemplate = {
    'Meta': '''
    ''',

    'Element': [
        # u'''
        #     <div class="text"><span class="righttext"><a href="%%">48270</a></span><p><a href="%IMG_ORI%" target="_blank" class="view_img_link">[查看原图]</a><br><img src="%IMG%"></p>
        #         <lisc_pass>
        #     </div>
        # ''',
        #
        u'''
            <div class="author"><strong title="%%">%AUTHOR%</strong>                            <br>
                <lisc_pass>
            </div>
        '''
    ]
}

Debug = {
    'FilterHtmlContent': {
        'LocalFileName': 'try_this'
    }
}
