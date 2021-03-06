# Copyright 2013-2016 Reahl Software Services (Pty) Ltd. All rights reserved.
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

import warnings

from webob import Request

from nose.tools import istest
from reahl.tofu import test, vassert
from reahl.stubble import stubclass

from reahl.webdev.tools import Browser
from reahl.web_dev.fixtures import WebFixture

from reahl.web.fw import UserInterface, Widget, FactoryDict, UserInterfaceFactory, RegexPath, UrlBoundView
from reahl.web.layout import PageLayout, ColumnLayout
from reahl.web.ui import HTML5Page, P, A, Div, Slot


@istest
class UserInterfaceTests(object):
    @test(WebFixture)
    def basic_ui(self, fixture):
        """A UserInterface is a chunk of web app that can be grafted onto the URL hierarchy of any app.
        
           A UserInterface has its own views. Its Views are relative to the UserInterface itself.
        """
        class UIWithTwoViews(UserInterface):
            def assemble(self):
                self.define_view('/', title='UserInterface root view')
                self.define_view('/other', title='UserInterface other view')

        class MainUI(UserInterface):
            def assemble(self):
                self.define_page(HTML5Page)
                self.define_user_interface('/a_ui',  UIWithTwoViews,  {}, name='myui')

        wsgi_app = fixture.new_wsgi_app(site_root=MainUI)
        browser = Browser(wsgi_app)

        browser.open('/a_ui/')
        vassert( browser.title == 'UserInterface root view' )

        browser.open('/a_ui/other')
        vassert( browser.title == 'UserInterface other view' )

    @test(WebFixture)
    def ui_slots_map_to_window(self, fixture):
        """The UserInterface uses its own names for Slots. When attaching a UserInterface, you have to specify 
            which of the UserInterface's Slots plug into which of the page's Slots.
        """
        class UIWithSlots(UserInterface):
            def assemble(self):
                root = self.define_view('/', title='UserInterface root view')
                root.set_slot('text', P.factory(text='in user_interface slot named text'))

        class MainUI(UserInterface):
            def assemble(self):
                self.define_page(HTML5Page).use_layout(PageLayout(contents_layout=ColumnLayout('main').with_slots()))
                self.define_user_interface('/a_ui',  UIWithSlots,  {'text': 'main'}, name='myui')

        wsgi_app = fixture.new_wsgi_app(site_root=MainUI)
        browser = Browser(wsgi_app)

        browser.open('/a_ui/')
        vassert( browser.title == 'UserInterface root view' )

        # The widget in the UserInterface's slot named 'text' end up in the HTML5Page slot called main
        [p] = browser.lxml_html.xpath('//div[contains(@class,"column-main")]/p')
        vassert( p.text == 'in user_interface slot named text' )


    @test(WebFixture)
    def ui_redirect(self, fixture):
        """When opening an URL without trailing slash that maps to where a UserInterface is attached,
           the browser is redirected to the UserInterface '/' View."""
           
        class UIWithRootView(UserInterface):
            def assemble(self):
                self.define_view('/', title='UserInterface root view')

        class MainUI(UserInterface):
            def assemble(self):
                self.define_page(HTML5Page)
                self.define_user_interface('/a_ui',  UIWithRootView,  {}, name='myui')

        wsgi_app = fixture.new_wsgi_app(site_root=MainUI)
        browser = Browser(wsgi_app)

        browser.open('/a_ui')
        vassert( browser.title == 'UserInterface root view' )
        vassert( browser.location_path == '/a_ui/' )

    @test(WebFixture)
    def ui_arguments(self, fixture):
        """UserInterfaces can take exta args and kwargs."""
           
        class UIWithArguments(UserInterface):
            def assemble(self, kwarg=None):
                self.kwarg = kwarg
                text = self.kwarg
                root = self.define_view('/', title='A view')
                root.set_slot('text', P.factory(text=text))

        class MainUI(UserInterface):
            def assemble(self):
                self.define_page(HTML5Page).use_layout(PageLayout(contents_layout=ColumnLayout('main').with_slots()))
                self.define_user_interface('/a_ui', UIWithArguments, {'text': 'main'},
                                name='myui', kwarg='the kwarg')

        wsgi_app = fixture.new_wsgi_app(site_root=MainUI)
        browser = Browser(wsgi_app)

        browser.open('/a_ui/')
        [p] = browser.lxml_html.xpath('//p')
        vassert( p.text == 'the kwarg' )

    @test(WebFixture)
    def bookmarks(self, fixture):
        """Bookmarks are pointers to Views. You need them, because Views are relative to a UserInterface and
           a Bookmark can, at run time, turn these into absolute URLs. Bookmarks also contain metadata,
           such as the title of the View it points to.
        """
        user_interface = UserInterface(None, '/a_ui', {}, False, 'test_ui')
        view = UrlBoundView(user_interface, '/aview', 'A View title', {})
        bookmark = view.as_bookmark()

        # What the bookmark knows
        vassert( bookmark.href.path == '/a_ui/aview' )
        vassert( bookmark.description == 'A View title' )
        vassert( bookmark.base_path == '/a_ui' )
        vassert( bookmark.relative_path == '/aview' )

        # How you would use a bookmark in other views (possibly in other UserInterfaces)
        a = A.from_bookmark(fixture.view, bookmark)
        vassert( str(a.href) == str(bookmark.href) )


    @test(WebFixture)
    def bookmarks_overrides(self, fixture):
        """Various bits of information can be overridden from the defaults when creating a bookmark from a View.
        """
        user_interface = UserInterface(None, '/a_ui', {}, False, 'test_ui')
        view = UrlBoundView(user_interface, '/aview', 'A View title', {})
        bookmark = view.as_bookmark(description='different description',
                                    query_arguments={'arg1': 'val1'},
                                    locale='af')

        # What the bookmark knows
        vassert( bookmark.description == 'different description' )
        vassert( bookmark.query_arguments == {'arg1': 'val1'} )
        vassert( bookmark.locale == 'af' )


    @test(WebFixture)
    def bookmarks_from_other_sources(self, fixture):
        """Bookmarks can also be made from ViewFactories, UserInterfaces or UserInterfaceFactories. 
        """
        class UIWithRelativeView(UserInterface):
            def assemble(self):
                view_factory = self.define_view('/aview', title='A View title')

                # How you could get a bookmark from a UserInterface or ViewFactory
                fixture.bookmark_from_view_factory = view_factory.as_bookmark(self)
                fixture.bookmark_from_ui = self.get_bookmark(relative_path='/aview')

        class MainUI(UserInterface):
            def assemble(self):
                self.define_page(HTML5Page)
                fixture.ui_factory = self.define_user_interface('/a_ui',  UIWithRelativeView,  {}, name='myui')

                # How you could get a bookmark from a UserInterfaceFactory
                fixture.bookmark_from_ui_factory = fixture.ui_factory.get_bookmark(relative_path='/aview')

        wsgi_app = fixture.new_wsgi_app(site_root=MainUI)
        Browser(wsgi_app).open('/a_ui/aview') # To execute the above once

        for bookmark in [fixture.bookmark_from_view_factory, 
                         fixture.bookmark_from_ui, 
                         fixture.bookmark_from_ui_factory]:
            # What the bookmark knows
            vassert( bookmark.href.path == '/a_ui/aview' )
            vassert( bookmark.description == 'A View title' )
            vassert( bookmark.base_path == '/a_ui' )
            vassert( bookmark.relative_path == '/aview' )


    class LifeCycleFixture(WebFixture):
        def current_view_is_plugged_in(self, page):
            return page.slot_contents['main_slot'].__class__ is Div

    @test(LifeCycleFixture)
    def the_lifecycle_of_a_ui(self, fixture):
        """This test illustrates the steps a UserInterface goes through from being specified, to
           being used. It tests a couple of lower-level implementation issues (see comments)."""

        @stubclass(UserInterface)
        class UserInterfaceStub(UserInterface):
            assembled = False
            def assemble(self, **ui_arguments):
                self.controller_at_assemble_time = self.controller
                root = self.define_view('/some/path', title='A view')
                root.set_slot('slotA', Div.factory())
                self.assembled = True

        # Phase1: specifying a user_interface and assembleing it to a site (with kwargs)
        parent_ui = None
#        parent_ui = EmptyStub(base_path='/')
        slot_map = {'slotA': 'main_slot'}
        ui_factory = UserInterfaceFactory(parent_ui, RegexPath('/', '/', {}), slot_map, UserInterfaceStub, 'test_ui')


        # Phase2: creating a user_interface
        request = Request.blank('/some/path')
        fixture.context.set_request(request)
        user_interface = ui_factory.create('/some/path', for_bookmark=False)

        # - Assembly happened correctly
        vassert( user_interface.parent_ui is parent_ui )
        vassert( user_interface.slot_map is slot_map )
        vassert( user_interface.name is 'test_ui' )
        vassert( user_interface.relative_base_path == '/' )
        vassert( user_interface.controller_at_assemble_time is not None)
        vassert( user_interface.controller is not None )
        vassert( user_interface.assembled )

        # - Create for_bookmark empties the relative_path
        user_interface = ui_factory.create('/some/path', for_bookmark=True)
        vassert( user_interface.relative_path == '' )

        # - The relative_path is reset if not done for_bookmark
        #   This is done in case a for_bookmark call just
        #   happened to be done for the same UserInterface in the same request
        #   before the "real" caal is done
        user_interface = ui_factory.create('/some/path', for_bookmark=False)
        vassert( user_interface.relative_path == '/some/path' )

        # Phase5: create the page and plug the view into it
        page = Widget.factory().create(user_interface.current_view)
        page.add_child(Slot(user_interface.current_view, 'main_slot'))

        page.plug_in(user_interface.current_view)
        vassert( fixture.current_view_is_plugged_in(page) )
        vassert( isinstance(user_interface.sub_resources, FactoryDict) )
