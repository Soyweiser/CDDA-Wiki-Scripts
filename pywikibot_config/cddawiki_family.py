# -*- coding: utf-8 -*-
"""Family module for CDDA/mediawiki wiki."""
#
# (C) Pywikibot team, 2006-2015
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

__version__ = '$Id: 5fd30f497c158166479ff15ef56e636e9053b2ec $'

from pywikibot import family


# The MediaWiki family
class Family(family.WikimediaFamily, family.SingleSiteFamily):

    """Family module for CDDA wiki."""

    name = 'cddawiki'
    domain = 'cddawiki.chezzo.com'
    codes = ['en']
    
    def ignore_certificate_error(self, code):
        return True
    
    def hostname(self,code):
        return 'cddawiki.chezzo.com'
    def protocol(self, code): #wiki doesn't use https, this forces http. (which should not be possible according to the pywikibot documentation).
        return 'http'
    def path(self, code):
        return '/index.php'
    def scriptpath(self, code):
        return '/cdda_wiki'