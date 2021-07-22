# -*- coding: utf-8 -*-

from odoo import models, fields, api

class survey(models.Model):
	_name = 'pmt.survey'

	name = fields.Char(string='Reference')
	category_id = fields.Many2one('pmt.survey.category', string="Category")
	appraisal_survey_id = fields.Many2one('pmt.main', string="Appraisal Reference")
	descriptions = fields.Text(string="Description")
	comments = fields.Text(string="Comments")



class survey_category(models.Model):
	_name = 'pmt.survey.category'

	name = fields.Char(string="Name")
	description = fields.Html(string="Description")