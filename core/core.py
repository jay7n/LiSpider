#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import logging
import re
import random

from bs4 import BeautifulSoup
from bs4 import element

import config2 as Config

logging.basicConfig(format='%(levelname)8s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.WARNING)


class Spider(object):

    def __init__(self, config):
        self.Config = config
        self.RegPattern = re.compile('%(\w*)%')
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

    def _censorNaviStrCandidateWithTemplate(self, candi_str, template_str, template_var_cache):
        if not type(candi_tag) == element.NavigableString or not type(template_tag) == element.NavigableString:
            return False

        matchObj = self.RegPattern.search(template_str)

        if matchObj is not None:
            varName = matchObj.group(1)
            varValue = None

            subed_tmpl_str = self.RegPattern.sub('(.+)', template_str)
            reg2 = re.compile(subed_tmpl_str)
            logger.debug('subed tmpl reg2 =', reg2)

            mo2 = reg2.match(candi_str)
            if mo2 is not None:
                varValue = mo2.group(1)
                self._procTemplateVariable(varName, varValue, template_var_cache)
            else:
                return False

        elif not candi_str == template_str:
            return False

        return True

    def _censorTagCandidateWithTemplate(self, candi_tag, template_tag, template_var_cache):
        if not type(candi_tag) == element.Tag or not type(template_tag) == element.Tag:
            return False

        if not candi_tag.name == template_tag.name:
            logger.debug('tag name inequality: \'%s\' is not equal to \'%s\'',
                         candi_tag.name, template_tag.name)
            return False

        # if candi_tag.name == 'img':
        #     print candi_tag

        for tmpAttrKey, tmpAttrValue in template_tag.attrs.iteritems():
            # if candi_tag.name == 'img':
                # print tmpAttrKey, tmpAttrValue

            if tmpAttrValue == '%%':
                # this means an empty variable,
                # indicating that it is expected to be ignored.
                continue

            if not candi_tag.has_attr(tmpAttrKey):
                logger.debug(candi_tag)
                logger.debug('tag attr not exsits: no attr \'%s\' in \'%s\'',
                             tmpAttrKey, candi_tag.name)
                return False

            candiAttrValue = candi_tag[tmpAttrKey]

            if tmpAttrKey == 'class':
                tmpAttrValue = ' '.join(tmpAttrValue)
                candiAttrValue = ' '.join(candiAttrValue)

            matchObj = self.RegPattern.search(tmpAttrValue)

            if matchObj is not None:
                varName = matchObj.group(1)
                varValue = candiAttrValue
                # print varName, varValue
                self._procTemplateVariable(varName, varValue, template_var_cache)

            elif not tmpAttrValue == candiAttrValue:
                logger.debug(candi_tag)
                logger.debug('tag attr inequality: \'%s\' is not equal to \'%s\' in \'%s\'',
                             tmpAttrValue, candiAttrValue, candi_tag.name)
                return False

        return True

    def _parseTagRecursive(self, candi_tag, template_tag, template_var_cache):
        for idx, tmpChild in enumerate(template_tag.contents):
            if tmpChild.name == 'lisc_pass':
                # this means <...>,
                # indicating that anything in this tag is expected to be ignored.
                continue

            if len(candi_tag.contents) <= idx:
                return False

            candiChild = candi_tag.contents[idx]
            if isinstance(tmpChild, element.NavigableString) and isinstance(candiChild, element.NavigableString):
                continue

            valid = False
            typeCandi = type(candiChild)
            typeTmp = type(tmpChild)

            if typeCandi == typeTmp == element.Tag:
                valid = self._censorTagCandidateWithTemplate(
                    candiChild, tmpChild, template_var_cache)
            elif typeCandi == typeTmp == element.NavigableString:
                valid = (candiChild == tmpChild)

            if valid is True:
                self._parseTagRecursive(candiChild, tmpChild, template_var_cache)
            else:
                if len(template_var_cache) > 0:
                    logger.debug(candi_tag)
                    logger.debug('censor not passed. cache will be cleared')
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

    def ParseHtmlContent(self, html_content):
        hitTemplateElem = self.Config.HitTemplate['Element'][0]
        hitTemplateElem = self._stripWhitespaceAndReturnBeforeParsing(hitTemplateElem)

        templateSoup = BeautifulSoup(hitTemplateElem, self.Config.ParseHtmlContent[
                                     'BeautifulSoupParser'])
        if self.Config.ParseHtmlContent['BeautifulSoupParser'] == 'html5lib':
            templateRootTag = templateSoup.body.contents[0]
        else:
            templateRootTag = templateSoup.contents[0]

        if not type(templateRootTag) == element.Tag:
            # TODO: what do we do for this ?
            pass

        def _searching_helper_func(tag):
            templateVarsCache = {}
            ret = self._censorTagCandidateWithTemplate(tag, templateRootTag, templateVarsCache)

            if ret is True:
                self._mergeTemplateVariablesWithCache(templateVarsCache)

            return ret

        htmlContent = self._stripWhitespaceAndReturnBeforeParsing(html_content)
        htmlSoup = BeautifulSoup(htmlContent, self.Config.ParseHtmlContent['BeautifulSoupParser'])
        tagCandidates = htmlSoup.find_all(_searching_helper_func)

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

                if startPage > endPage:
                    startPage, endPage = endPage, startPage

                for page in xrange(startPage, endPage):
                    subed_url = reg.sub(str(page), url)
                    htmlContent = self.GrabHtmlContent(subed_url)
                    self.ParseHtmlContent(htmlContent)
            else:
                htmlContent = self.GrabHtmlContent(url)
                self.ParseHtmlContent(htmlContent)

        print self.TemplateVariables

if __name__ == "__main__":
    sp = Spider(Config)
    sp.Run()
