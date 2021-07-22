# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError,AccessError,ValidationError

class res_users(models.Model):
	_inherit = 'res.users'



class res_groups(models.Model):
	_inherit = 'res.groups'

	