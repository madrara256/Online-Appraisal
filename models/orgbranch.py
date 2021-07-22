# -*- coding: utf-8 -*-

from odoo import models, fields, api

class orgbranch(models.Model):
	_name = 'org.branch'


	name = fields.Char(string='Branch')
	mobile = fields.Char(string='Mobile')
	phone = fields.Char(string='Phone')