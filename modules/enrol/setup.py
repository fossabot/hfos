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

from setuptools import setup, find_packages

setup(name="hfos-enrol",
      version="0.0.1",
      description="hfos-enrol",
      author="Hackerfleet Community",
      author_email="riot@c-base.org",
      url="https://github.com/hackerfleet/hfos-enrol",
      license="GNU General Public License v3",
      packages=find_packages(),
      long_description="""HFOS - Enrol
================

A module to manage user invitations and registrations

This software package is a plugin module for HFOS.
""",
      dependency_links=[
      ],
      install_requires=[
          'hfos>=1.2.0',
          'hfos-navdata>=0.0.1'
      ],
      entry_points="""[hfos.components]
    enrol=hfos.enrol.manager:Manager
    [hfos.schemata]
    enrollment=hfos.enrol.enrollment:Enrollment
    """,
      test_suite="tests.main.main",
      )
