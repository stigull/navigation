#! /usr/bin/env python
# -*- coding: utf8 -*-
import logging

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings

register = template.Library()

def navigation_menu(context):
	list_of_links = []
	try:
		url_info = settings.NAVIGATION
	except AttributeError:
		logging.info(u"Variable NAVIGATION missing from settings - no navigation tree rendered")
		return {}
	else:
		for verbose_name, url_name in url_info:
			try:
				href = reverse(url_name)
			except NoReverseMatch:
				logging.info("NoReverseMatch for %s - skipped while rendering the navigation tree" % url_name)
				pass
			else:
				is_current = href == context['request'].path
				list_of_links.append({'verbose_name': verbose_name, 'href': href, 'is_current': is_current })

		return {'list_of_links' : list_of_links }
register.inclusion_tag('navigation/generic_navigation.html', takes_context=True)(navigation_menu)