#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# HFOS - Hackerfleet Operating System
# ===================================
# Copyright (C) 2011-2017 Heiko 'riot' Weinen <riot@c-base.org> and others.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Heiko 'riot' Weinen"
__license__ = "GPLv3"

"""
Schema: SensorData
====================

Contains
--------

SensorData:


"""
from hfos.schemata.base import base_object

SensorDataSchema = base_object('sensorData',
                               has_owner=False,
                               has_uuid=False,
                               all_roles='crew')

SensorDataSchema['properties'].update({
    'value': {
        'title': 'Value', 'description': 'Sensordata Value'
    },
    'timestamp': {
        'type': 'number', 'title': 'Timestamp',
        'description': 'Log Message timestamp (microSec)'
    },
    'type': {
        'type': 'string'
    }
})

SensorDataForm = [
    {
        'type': 'section',
        'htmlClass': 'row',
        'items': [
            {
                'type': 'section',
                'htmlClass': 'col-xs-4',
                'items': [

                ]
            },
            {
                'type': 'section',
                'htmlClass': 'col-xs-4',
                'items': [

                ]
            }
        ]
    },
    'description'
]

SensorData = {'schema': SensorDataSchema, 'form': SensorDataForm}
