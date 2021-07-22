# -*- coding: utf-8 -*-

from odoo import models, fields, api

class behaviorating(models.Model):
	_name = 'value.rating'

	name = fields.Integer(string='Rating')
	range_from = fields.Float(string='Range From')
	range_to = fields.Float(string='Range To')

	final_rate_score = fields.Integer(string='RATE SCORE')

	description = fields.Text(string='Description')