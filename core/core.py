#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import logging
import re
import random

from bs4 import BeautifulSoup
from bs4 import element

import liwebspiderconf as Config

logging.basicConfig(format='%(asctime)s %(levelname)8s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Spider(object):

    def __init__(self, config):
        self.Config = config
        self.RegPattern = re.compile('%(\w+)%')
        self.TemplateVariables = {}

    def GrabHtmlContent(self, url):
        if not url:
            logger.warning('grab html content failed: no url provided.')
            return None

        request_counter = [0]

        def _request_content(user_agent='Chrome'):
            if request_counter[0] > self.Config.GrabHtmlContent['MaxTryCount']:
                return None

            request_counter[0] += 1

            try:
                req = urllib2.Request(url, headers={'User-Agent': user_agent})
                con = urllib2.urlopen(req)
                return con
            except Exception as e:
                # if forbidden, try it `Config.GrabHtmlContent['MaxTryCount']` more times
                # TO BE CLEAR : what the hell 'user_agent' is for ?
                return _request_content(random.sample('abcdefghijklmnopqrstuvwxyz', 10))

        con = _request_content()

        if con.code != 200:
            msg = 'grab html content failed: http code returns abnormally'
            logger.warning(msg)
            raise Exception('msg')

        return con.read()

    def _procTemplateVariable(self, var_name, var_value, template_var_cache):
        if var_name in template_var_cache:
            template_var_cache[var_name].append(var_value)
        else:
            template_var_cache[var_name] = [var_value]

        # TODO

    def _censorTagCandidateWithTemplate(self, candi_tag, template_tag, template_var_cache):
        if not type(candi_tag) == element.Tag or not type(template_tag) == element.Tag:
            return False

        if not candi_tag.name == template_tag.name:
            return False

        for tmpAttrKey, tmpAttrValue in template_tag.attrs.iteritems():
            if not candi_tag.has_attr(tmpAttrKey):
                return False

            candiAttrValue = candi_tag[tmpAttrKey]

            if tmpAttrKey == 'class':
                tmpAttrValue = ' '.join(tmpAttrValue)
                candiAttrValue = ' '.join(candiAttrValue)

            matchObj = self.RegPattern.search(tmpAttrValue)

            if matchObj is not None:
                varName = matchObj.group(1)
                varValue = candiAttrValue
                self._procTemplateVariable(varName, varValue, template_var_cache)
            elif not tmpAttrValue == candiAttrValue:
                return False

        return True

    def _parseTagRecursive(self, candi_tag, template_tag, template_var_cache):
        for idx, tmpChild in enumerate(template_tag.contents):
            if len(candi_tag.contents) <= idx:
                return False

            candiChild = candi_tag.contents[idx]
            if isinstance(tmpChild, element.NavigableString) and isinstance(candiChild, element.NavigableString):
                continue

            valid = self._censorTagCandidateWithTemplate(candiChild, tmpChild, template_var_cache)
            if valid is True:
                self._parseTagRecursive(candiChild, tmpChild, template_var_cache)
            else:
                template_var_cache.clear()
                return False

        return True

    def _mergeTemplateVariablesWithCache(self, template_var_cache):
        for key, value in template_var_cache.iteritems():
            if key in self.TemplateVariables:
                self.TemplateVariables[key].extend(value)
            else:
                self.TemplateVariables[key] = value

        # TODO

    def _stripWhitespaceAndReturnBeforeParsing(self, html_content):
        p = re.compile('\n*\s*(<[^<>]+>)\s*\n*')
        return p.sub('\g<1>', html_content)

    def ParseContent(self, html_content):
        hitTemplateElem = self.Config.HitTemplate['Element'][0]
        hitTemplateElem = self._stripWhitespaceAndReturnBeforeParsing(hitTemplateElem)

        templateSoup = BeautifulSoup(hitTemplateElem)
        templateRootTag = templateSoup.body.contents[0]

        if not type(templateRootTag) == element.Tag:
            # TODO: what do we do for this ?
            pass

        def _searching_helper_func(tag):
            templateVarsCache = {}
            ret = self._censorTagCandidateWithTemplate(tag, templateRootTag, templateVarsCache)

            if ret is True:
                self._mergeTemplateVariablesWithCache(templateVarsCache)

            return ret

        html_content = self._stripWhitespaceAndReturnBeforeParsing(html_content)
        htmlSoup = BeautifulSoup(html_content, 'html5lib')
        # tagCandidates = htmlSoup.find_all(name='ul')
        tagCandidates = htmlSoup.find_all(_searching_helper_func)

        # logger.debug(tagCandidates)

        for candiTag in tagCandidates:
            templateVarsCache = {}
            self._parseTagRecursive(candiTag, templateRootTag, templateVarsCache)

            if not len(templateVarsCache) == 0:
                self._mergeTemplateVariablesWithCache(templateVarsCache)

    def Run(self):
        for url in self.Config.GrabHtmlContent['URLScope']:
            reg = re.compile('%(\d+)-(\d+)%')
            matchObj = reg.search(url)

            if matchObj is not None:
                startPage = int(matchObj.group(1))
                endPage = int(matchObj.group(2)) + 1

                for page in xrange(startPage, endPage):
                    subed_url = reg.sub(str(page), url)
                    htmlContent = self.GrabHtmlContent(subed_url)
                    self.ParseContent(htmlContent)
            else:
                htmlContent = self.GrabHtmlContent(url)
                self.ParseContent(htmlContent)

        print self.TemplateVariables['IMG_1']

if __name__ == "__main__":
    sp = Spider(Config)
    sp.Run()


# def extract_elem_from_raw_tag(tag_row, tag_text, resize_image=False):
#     print "into func ing.."
#     # find author and id first, as the rss title
#     author_tag = tag_row.find(name='div', class_='author')
#     author = author_tag.find(name='strong').string
#     logging.debug('author = %s', author)
#
#     id_tag = tag_text.find(name='span', class_='righttext')
#     id = id_tag.string
#     logging.debug('id = %s', id)
#
#     # then find the img link
#     orig_img_tag = tag_text.find(name='a', class_='view_img_link')
#     orig_img_link = orig_img_tag.get('href')
#     logging.debug('orig_img_link = %s', orig_img_link)
#
#     # and at last get tht real image content
#     img_tag = tag_text.find(name='img')
#     img_link = img_tag.get('src')
#     logging.debug('img_link = %s', img_link)
#
#     image_con = grab_html_content(img_link)
#
#     if resize_image:
#         # resize the image using pillow
#         im = Image.open(cStringIO.StringIO(image_con))
#         new_size = (int(im.size[0] / IMG_SIZE_RATIO), int(im.size[1] / IMG_SIZE_RATIO))
#         im.resize(new_size)
#
#         image_io = cStringIO.StringIO()
#         im.save(image_io, im.format)
#         image_con = image_io.getvalue()
#         image_io.close()
#
#     return {'id': id,
#             'author': author,
#             'link': img_link,
#             'content': image_con}
#
# def extract_elem_from_raw_tag_entry(tag_row, tag_text, resize_image=False):
#     global _MyThreadDigger
#     _MyThreadDigger.AddTask(extract_elem_from_raw_tag, tag_row, tag_text, resize_image)
#
#
# def filter_html_content(html_content, recursive=False):
#     if not html_content:
#         logger.warning('filter html content failed : no html content provided.')
#         return None
#
#     soup = BeautifulSoup(html_content, "html.parser")
#
#     if __debug__:
#         with open(Debug_FilterHtmlContent_LocalFileName, "w") as f:
#             f.write(soup.prettify().encode('utf-8'))
#
#     raw_tags_row = soup.find_all(name='div', class_='row')
#     raw_tags_text = soup.find_all(name='div', class_='text')
#     # elems = []
#
#     print "size of raw_tags_row= %d" % len(raw_tags_row)
#     print "size of raw_tags_text= %d" % len(raw_tags_text)
#     for tag_row, tag_text in itertools.izip(raw_tags_row, raw_tags_text):
#         elem = extract_elem_from_raw_tag_entry(tag_row, tag_text)
#     # elems.append(elem)
#
#     if recursive is True:
#         cp_pagenavi_tag = soup.body.find(name='div', class_='cp-pagenavi')
#
#         def page_filter(tag):
#             return tag.has_attr('href') and not tag.has_attr('class')
#
#         rest_two_pages = cp_pagenavi_tag.find_all(page_filter)
#
#         for page in rest_two_pages:
#             previous_url = page.get('href')
#
#             logging.debug('previous_url = %s', previous_url)
#
#             previous_html = grab_html_content(previous_url)
#             filter_html_content(previous_html, False)
#             # elems.extend(previous_elems)
#
#     # elems.reverse()
#     # return elems
#
#
# def filter_html_content_entry(html_content):
#     global _MyThreadDigger
#     _MyThreadDigger = ThreadDigger(DIGGER_THREAD_COUNT)
#
#     filter_html_content(html_content, True)
#
#     _MyThreadDigger.StartToDig()
#
#     elems = _MyThreadDigger.WaitToEnd()
#
#     return elems
