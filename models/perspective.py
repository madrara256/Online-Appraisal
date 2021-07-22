from odoo import models, fields, api

class perspective(models.Model):
	_name = 'pmt.perspective'


	name = fields.Char(string='Perspective')
	contribution = fields.Integer(string='contribution(%)')