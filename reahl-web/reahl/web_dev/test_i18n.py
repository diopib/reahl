# Copyright 2013, 2014, 2015 Reahl Software Services (Pty) Ltd. All rights reserved.
#
#    This file is part of Reahl.
#
#    Reahl is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation; version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import print_function, unicode_literals, absolute_import, division
from nose.tools import istest
from reahl.tofu import Fixture, test
from reahl.tofu import vassert

from reahl.web_dev.fixtures import WebBasicsMixin
from reahl.web_dev.fixtures import WebFixture

from reahl.component.context import ExecutionContext
from reahl.component.i18n import Translator
from reahl.web.fw import UserInterface, IdentityDictionary, Bookmark, UrlBoundView, Url
from reahl.web.ui import HTML5Page
from reahl.webdev.tools import Browser, WidgetTester


@test(WebFixture)
def i18n_urls(fixture):
    """The current locale is determined by reading the first segment of the path. If the locale is not present in the
    path, web.default_url_locale is used."""
    _ = Translator('reahl-web')

    class I18nUI(UserInterface):
        def assemble(self):
            view = self.define_view('/aview', title=_('A View'))

    class MainUI(UserInterface):
        def assemble(self):
            self.define_page(HTML5Page)
            self.define_user_interface('/a_ui',  I18nUI,  IdentityDictionary(), name='test_ui')
            
    wsgi_app = fixture.new_wsgi_app(site_root=MainUI)
    browser = Browser(wsgi_app)

    browser.open('/a_ui/aview')
    vassert( browser.title == 'A View' )

    browser.open('/af/a_ui/aview')
    vassert( browser.title == '\'n Oogpunt' )

    fixture.context.config.web.default_url_locale = 'af'
    browser.open('/a_ui/aview')
    vassert( browser.title == '\'n Oogpunt' )
    
    browser.open('/en_gb/a_ui/aview')
    vassert( browser.title == 'A View' )


@test(WebFixture)
def bookmarks(fixture):
    """Bookmarks normally refer to the current locale. You can override that to be a specified locale instead.
    """

    bookmark = Bookmark('/base_path', '/relative_path', 'description')
    af_bookmark = Bookmark('/base_path', '/relative_path', 'description', locale='af')

    vassert( af_bookmark.locale == 'af' )
    vassert( af_bookmark.href.path == '/af/base_path/relative_path' )

    vassert( bookmark.locale is None )
    vassert( bookmark.href.path == '/base_path/relative_path' )
