# -*- coding: utf-8 -*-

from odoo import models, fields, api

class corerating(models.Model):
	_name = 'core.rating'


	name = fields.Char(string='Rating')
	range_from = fields.Float(string='Range From')
	range_to = fields.Float(string='Range To')
