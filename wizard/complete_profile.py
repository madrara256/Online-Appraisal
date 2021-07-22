# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from odoo.exceptions import Warning, UserError,ValidationError


_logger = logging.getLogger(__name__)

class complete_user_profile_wizard(models.TransientModel):
	_name = 'complete.profile.wizard'


	 # User can write on a few of his own fields (but not his groups for example)
	SELF_WRITEABLE_FIELDS = ['signature', 'action_id', 'company_id', 'email', 'name', 'image', 'image_medium', 'image_small', 'lang', 'tz']
    # User can read a few of his own fields
	SELF_READABLE_FIELDS = ['signature', 'company_id', 'login', 'email', 'name', 'image', 'image_medium', 'image_small', 'lang', 'tz', 'tz_offset', 'groups_id', 'partner_id', '__last_update', 'action_id']

	current_user = fields.Many2one('res.users', string="Current User:", default=lambda self: self.env.uid, readonly=True)
	login = fields.Char(related='current_user.login', string='Email Address')
	name = fields.Char(related='current_user.name', string='Name')
	partner_id = fields.Many2one(related='current_user.partner_id', string='Related Partner')
	email = fields.Char(related='current_user.email', string='Email')
	active = fields.Boolean(related="current_user.active", string='Active', default=True, readonly=True)

	# def default_user_groups(self):
	# 	return self.env['res.groups'].search([('category_id', '=', 62)])
		
	
	job_level = fields.Many2one('res.users',string='Job Level',domain="[('category_id', '=', 62)]")

	
