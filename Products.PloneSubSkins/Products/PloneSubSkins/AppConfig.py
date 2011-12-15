# -*- coding: utf-8 -*-
#
# File: AppConfig.py
#
# Copyright (c) 2007 by Espen MOE-NILSSEN / Eric BREHAULT
# Zope Public License (ZPL)
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__author__ = """Eric BREHAULT <ebrehault@gmail.com>"""
__docformat__ = 'plaintext'


# Product specific configuration.
#
sub_skins_categories = ({'id' : 'base',
                        'label' : 'Base skin',
                        'help' : 'Select the default css-skin for Base.'
                        },
                        {'id' : 'top',
                        'label' : 'Top skin',
                        'help' : 'Select the default css-skin for the Top section.'
                        },
                        {'id' : 'text',
                        'label' : 'Text skin',
                        'help' : 'Select the default css-skin for the text.'
                        },
                        {'id' : 'globalnav',
                        'label' : 'Global navigation skin',
                        'help' : 'Select the default css-skin for the global navigation.'
                        },
                        {'id' : 'portlets',
                        'label' : 'Portlets skin',
                        'help' : 'Select the default css-skin for the portlets.'
                        },
                        {'id' : 'navigation',
                        'label' : 'Navigation skin',
                        'help' : 'Select the default css-skin for the Navigation portlet.'
                        },
                        {'id' : 'calendar',
                        'label' : 'Calendar skin',
                        'help' : 'Select the default css-skin for the Calendar portlet.'
                        },
                        {'id' : 'bottom',
                        'label' : 'Bottom skin',
                        'help' : 'Select the default css-skin for the Bottom section.'
                        },
                        {'id': 'extra',
                        'label': 'Extra stuff',
                        'help': 'Extra stuff.'
                        }
                        )
