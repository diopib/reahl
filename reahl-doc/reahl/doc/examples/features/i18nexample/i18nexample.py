from __future__ import print_function, unicode_literals, absolute_import, division

from reahl.component.i18n import Translator
from reahl.web.fw import UserInterface, Url
from reahl.web.bootstrap.ui import P, HTML5Page
from reahl.web.bootstrap.navs import Nav, PillLayout

_ = Translator('reahl-doc')


class TranslatedUI(UserInterface):
    def assemble(self):
        self.define_view('/some_page', title=_('Translated example'), 
                                       page=HomePage.factory())


class HomePage(HTML5Page):
    def __init__(self, view):
        super(HomePage, self).__init__(view)

        menu = Nav(self.view).use_layout(PillLayout(stacked=True)).with_languages()
        self.body.add_child(menu)

        current_url = Url.get_current_url()
        message = _('This is a translated string. The current URL is "%s".') \
                    % current_url.path
        self.body.add_child(P(view, text=message))








