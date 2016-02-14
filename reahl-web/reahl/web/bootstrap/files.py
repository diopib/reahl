# Copyright 2016 Reahl Software Services (Pty) Ltd. All rights reserved.
#-*- encoding: utf-8 -*-
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

"""
Widgets for uploading files.

.. versionadded:: 3.2

"""
from __future__ import print_function, unicode_literals, absolute_import, division

import six
from reahl.web.fw import Widget, Url
from reahl.web.ui import Div, A, Span, Li, Img, HTMLElement, Ol, WrappedInput, Label
from reahl.component.i18n import Translator
from reahl.web.bootstrap.ui import SimpleFileInput

_ = Translator('reahl-web')


#TOTEST
# Focus, blur
# What shows in js and what without
# Filling in the filename when chosen (scenario for more than one file)
# i18n

    
class FileInputButton(WrappedInput):
    def __init__(self, form, bound_field):
        label = Label(form.view)
        self.simple_input = label.add_child(SimpleFileInput(form, bound_field))
        self.simple_input.html_representation.append_class('btn-secondary')
        label.add_child(Span(form.view, text='Choose file'))
        super(FileInputButton, self).__init__(self.simple_input)
        self.add_child(label)

        label.append_class('reahl-bootstrapfileinputbutton')
        label.append_class('btn')
        label.append_class('btn-primary')
        self.set_html_representation(label)

    def get_js(self, context=None):
        js = ['$(".reahl-bootstrapfileinputbutton").bootstrapfileinputbutton({});']
        return super(FileInputButton, self).get_js(context=context) + js


class FileInput(WrappedInput):
    def __init__(self, form, bound_field):
        file_input = FileInputButton(form, bound_field)
        super(FileInput, self).__init__(file_input)

        self.input_group = self.add_child(Div(self.view))
        self.input_group.append_class('input-group')
        self.input_group.append_class('reahl-bootstrapfileinput')
        self.set_html_representation(self.input_group)

        span = self.input_group.add_child(Span(form.view))
        span.append_class('input-group-btn')
        span.add_child(file_input)

        filename_input = self.input_group.add_child(Span(self.view, text=_('No files chosen')))
        filename_input.append_class('form-control')
#        filename_input = self.input_group.add_child(HTMLElement(self.view, 'input'))
#        filename_input.set_attribute('type', 'text')
#        filename_input.append_class('form-control')
#        filename_input.set_attribute('readonly', 'readonly')

#        filename_input = self.input_group.add_child(TextInput(form, self.fields.filename))
#        filename_input.html_representation.set_attribute('readonly', 'readonly')


#    @exposed
#    def fields(self, fields):
#        fields.filename = Field()


    def get_js(self, context=None):
        js = ['$(".reahl-bootstrapfileinput").bootstrapfileinput({nfilesMessage: "%s", nofilesMessage: "%s"});' % \
              (_('files chosen'), _('No files chosen'))]
        return super(FileInput, self).get_js(context=context) + js
