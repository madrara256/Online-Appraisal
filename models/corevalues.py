# -*- coding: utf-8 -*-

from odoo import models, fields, api

class corevalues(models.Model):
	_name = 'pmt.corevalue'

	name = fields.Char(string='Core Values/Behavioral')
	net_score = fields.Integer(string='Net Score')
	description = fields.Html(string="Measures")
