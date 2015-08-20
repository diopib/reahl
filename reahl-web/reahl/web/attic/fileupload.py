# Copyright 2015 Reahl Software Services (Pty) Ltd. All rights reserved.
# -*- encoding: utf-8 -*-
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


import reahl.web.ui

class FileUploadLi(reahl.web.ui._FileUploadLi):
    pass


class FileUploadPanel(reahl.web.ui._FileUploadPanel):
    pass


class UniqueFilesConstraint(reahl.web.ui._UniqueFilesConstraint):
    pass


class FileUploadInput(reahl.web.ui._FileUploadInput):
    __doc__ = reahl.web.ui._FileUploadInput.__doc__




