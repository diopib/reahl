


from __future__ import print_function, unicode_literals, absolute_import, division
from reahl.tofu import test, set_up

from reahl.web_dev.fixtures import WebFixture
from reahl.webdev.tools import Browser, XPath
from reahl.sqlalchemysupport import Session

from reahl.doc.examples.tutorial.migrationexamplebootstrap.migrationexamplebootstrap import AddressBookUI, Address


class MigrateFixture(WebFixture):
    def new_wsgi_app(self):
        return super(MigrateFixture, self).new_wsgi_app(site_root=AddressBookUI)

        
    def new_existing_address(self):
        address = Address(name='John Doe', email_address='johndoe@some.org')
        address.save()
        return address

    def new_browser(self):
        return Browser(self.wsgi_app)

    def address_is_listed_as(self, name, email_address):
        return self.browser.is_element_present(XPath.paragraph_containing('%s: %s' % (name, email_address)))


@test(MigrateFixture)
def add_address(fixture):
    """A user can add an address, after which the address is listed."""
    browser = fixture.browser
    
    browser.open('/')
    browser.type(XPath.input_labelled('Name'), 'John')
    browser.type(XPath.input_labelled('Email'), 'johndoe@some.org')

    browser.click(XPath.button_labelled('Save'))
    
    assert fixture.address_is_listed_as('John', 'johndoe@some.org')


class DemoFixture(MigrateFixture):
    commit=True
    @set_up
    def do_demo_setup(self):
        Session.add(Address(name='John Doe', email_address='johndoe@some.org'))
        Session.add(Address(name='Jane Johnson', email_address='janejohnson@some.org'))
        Session.add(Address(name='Jack Black', email_address='jackblack@some.org'))

        Session.flush()
        Session.commit()

