# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError,AccessError,ValidationError


class pmt(models.Model):
	_name = 'pmt.main'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = 'Appraisals'

	#-----------------------------------
	#DATABASE
	#-----------------------------------


	@api.multi
	@api.constrains('appraisalbh_line_id')
	def check_exist_aspect_in_line(self):
		for appraisal in self:
			exist_aspect_list = []
			for line in appraisal.appraisalbh_line_id:
				if line.perspective_bh_id.id in exist_aspect_list:
					raise ValidationError(_('BEHAVIORAL ASPECTS CAN NOT BE DUPLICATED \n'+
						'PLEASE SELECT ANOTHER UNIQUE ASPECT!'))
				exist_aspect_list.append(line.perspective_bh_id.id)

	name = fields.Many2one('res.users',string='Employee Name', track_visibility="onchange", 
		default=lambda self: self.env.user.id, readonly=True)
	quarter = fields.Selection(
		[
			('mid', 'Mid-Year Appraisals')
		],
		string='Apprisal-Duration', default='mid', required=True,)
	appraisal_line_id = fields.One2many("appraisal.line", "appraisal_id", string="Initial Task") 
	appraisal_survey_line_id = fields.One2many('pmt.survey', 'appraisal_survey_id', string="Survey")
	appraisalbh_line_id = fields.One2many('appraisalbh.line','appraisalbh_id', string="Initial Task")

	state = fields.Selection(
		[
			('self', 'Self Assesment'),
			('manager', 'Manager Assesment'),
			('hod', 'Department Head Assesment'),
			('coo', 'COO\'s Assesment'),
			('ed', 'ED\'s Assesment'),
			('md', 'MD\'s Assesment'),
			('hr', 'HR Assesment')
		], default="self", track_visibility="onchange")

	position = fields.Char(string='Position/Role', track_visibility="onchange")
	number_of_years_in_role = fields.Char(string='Number Of Years In Current Role')
	last_date_review = fields.Date(string='Date Of Last Review')
	line_manager = fields.Many2one('res.users',string='Manager/Supervisor')
	branch = fields.Many2one('org.branch',string='Deployment Branch')
	staff_no = fields.Char(string="Staff No.", track_visibility="onchange", required=True)
	department_head = fields.Many2one('res.users',string='Head Of Department')
	partner_id = fields.Many2one('res.partner', string='Partner')

	job_level = fields.Selection(
		[
			('officer', 'Officer'),
			('manager', 'Manager'),
			('hod', 'Head Of Department'),
			('top', 'COO/ED/CFO/CCO/CRO(Chief Risk Officer)/Head Compliance/CIA(Chief Internal Auditor)')
		], string='Job Level', required=True, default='')

	#-----------------------------------------
	#BUSINESS LOGIC
	#-----------------------------------------

	@api.depends('appraisal_line_id.weighted_score')
	def _check_sec_a_net_weight(self):
		for record in self:
			subtotal_net_weight = 0.0
			for sub_weight in record.appraisal_line_id:				
				subtotal_net_weight += sub_weight.weighted_score
				subtotal_wieght_score = (subtotal_net_weight/10)
				print('SUBTOTAL WEIGHT: '+str(subtotal_wieght_score))
				record.section_a_net_weight = subtotal_wieght_score
				rating_stand = self.env['core.rating'].search([])
				for rec in rating_stand:
					if subtotal_wieght_score >= rec.range_from and subtotal_wieght_score <= rec.range_to:
						print('SECTION A RANGES' + 'FROM' +str(rec.range_from) + 'TO' + str(rec.range_to))
						print('SECTION A RATING: ' +str(rec.name))
						record.section_a_score = rec.name

	
	section_a_net_weight = fields.Float(string='SECTION A: WEIGHT', 
		compute='_check_sec_a_net_weight', store=True)


	user_id = fields.Many2one('res.users', string='Current Logged In User', default=lambda self: self.env.uid)

	@api.depends('appraisal_line_id.weighted_score')
	def _compute_section_a_score(self):
		for score in self:
			subtotal_score = 0.0
			for assement in score.appraisal_line_id:
				subtotal_score += assement.weighted_score
				rating_stand = self.env['core.rating'].search([])
				for rec in rating_stand:
					if subtotal_score >= rec.range_from and subtotal_score <= rec.range_to:
						print('SECTION A RATING: ' +str(rec.name))
						score.section_a_score = rec.name

	section_a_score = fields.Char(string='SECTION A: SCORE', compute='_check_sec_a_net_weight',
		store=True)


	@api.depends('appraisalbh_line_id.total_score_bh')
	def _compute_section_b_score(self):
		for score in self:
			subtotal_score = 0.0
			for assement in score.appraisalbh_line_id:
				subtotal_score += assement.total_score_bh
				final_score_weight = (subtotal_score/5)
				score.section_b_net_weight = final_score_weight
				rating_stand = self.env['value.rating'].search([])
				for rec in rating_stand:
					if final_score_weight >= rec.range_from and final_score_weight <= rec.range_to:
						print('SECTION B RATING: '+str(rec.name))
						score.section_b_average_score = rec.name


	section_b_net_weight = fields.Float(string='SECTION B: SCORE', compute='_compute_section_b_score', 
		store=True)

	section_b_average_score = fields.Float(string='SECTION B: RATING', compute='_compute_section_b_score' 
		,store=True)


	
	@api.depends('section_a_score', 'section_b_average_score')
	def _compute_overall_score(self):
		for record in self:
			record.overall_score = str(record.section_a_score)+ ' '+str(int(record.section_b_average_score))

	overall_score = fields.Char(string='OVERRALL', compute='_compute_overall_score',store=True)	

	def _check_existing_record_under_current_user(self,values):
		record_under_user = self.env['pmt.main'].search([('name', '=', self.env.uid)])
		print('Executing......')
		latest_record_date = None
		if record_under_user:
			for record in record_under_user:
				#pass my query
				self.env.cr.execute("""SELECT name,create_date
				FROM pmt_main
				ORDER BY create_date DESC
				LIMIT 1""")
				latest_record = self.env.cr.fetchall()
				print('fetched record contains '+str(latest_record))
				for rec in latest_record:
					print('record------ '+str(rec[1]))
					latest_record_date = rec[1]
					print('LATEST RECORD DATE: '+str(latest_record_date))
					return latest_record_date

	#-------------------------------------
	# OVERRIDE THE ORM
	#-------------------------------------

	@api.model
	def create(self, values):
		all_chosen_aspects = self.env['appraisalbh.line'].search([])
		
		records_under_profile = self.env['pmt.main'].search([('name', '=', self.env.uid)])
		if records_under_profile:
			raise ValidationError(_('There is an Existing Appraisal Record Ongoing Under your profile \n'+
				'Please Contact your Systems Administrator'))
		rec = super(pmt, self).create(values)
		return rec

	@api.multi
	def write(self, values):
		logged_in_user = self.env.uid
		if self.state == 'hr' and not self.env['res.users'].has_group('pmt.pmt_hr'):
			raise ValidationError(_('This record can no longer be Modified\n'+
				'Please Contact the Systems Administrator'))

		if self.env['res.users'].has_group('pmt.pmt_user') and self.state not in ['self']:
			raise AccessError(_('You are no longer Authorized to Modify this File \n'+
				'Please Contact your Systems Administrator'))
		
		if self.env['res.users'].has_group('pmt.pmt_officer') and self.state not in ['self', 'manager']:
			raise AccessError(_('You are no longer Authorized to Modify this File \n'+
				'Please Contact your Systems Administrator'))

		if self.env['res.users'].has_group('pmt.pmt_manager') and self.state not in ['self', 'hod']:
			raise UserError(_('You are no longer Authorized to Modify this File \n'+
				'Please Contact your Systems Administrator'))

		if self.env['res.users'].has_group('pmt.pmt_ed') and self.state  not in ['self','ed']:
			raise UserError(_('You are no longer Authorized to Modify this File \n'+
				'Pleas Contact your Systems Administrator'))

		if self.env['res.users'].has_group('pmt.pmt_manager_others') and self.state not in ['self','hod']:
			raise UserError(_('You are no longer Authorized to Modify this File \n'+
				'Pleas Contact your Systems Administrator'))

		if self.env['res.users'].has_group('pmt.pmt_other_direct_md_functions') and state not in ['self']:
			raise UserError(_('You are no longer Authorized to Modify this File \n'+
				'Please Contact your Systems Administrator'))

		if self.env['res.users'].has_group('pmt.pmt_coo') and self.state not in ['self','coo']:
			raise UserError(_('You are no longer Authorized to Modify this File \n'+
				'Please Contact your Systems Administrator'))

		rec = super(pmt, self).write(values)
		
		return rec

	@api.multi
	def unlink(self):
		rec = super(pmt, self).unlink()
		return rec

	def copy_data(self, context=None):
		raise UserError(_('Appraisal record can not be duplicated'))

	#-----------------------------------
	#BUSINESS LOGIC
	#-----------------------------------

	@api.depends('appraisal_line_id.net_weight')
	def check_total_net_weight(self):
		for record in self:
			subtotal_weight = 0.0
			for weight in record.appraisal_line_id:
				subtotal_weight += weight.net_weight
				print('NET WEIGHT IS '+str(subtotal_weight))
				record.section_a_percentage_score = subtotal_weight

	@api.depends('appraisalbh_line_id.net_weight_bh')
	def check_all_aspects_weight(self):
		for record in self:
			subtotal_weight = 0.0
			for weight in record.appraisalbh_line_id:
				subtotal_weight += weight.net_weight_bh
				print('SECTION B NET WEIGHT IS '+str(subtotal_weight))
				record.section_b_aspects = subtotal_weight

	section_a_percentage_score = fields.Integer(string='Overall Score', compute='check_total_net_weight', store=True)

	section_b_aspects = fields.Integer(string='Behavioral Aspects', compute='check_all_aspects_weight', store=True)

	@api.multi
	def submit_supervisor(self):
		for record in self:
			if record.section_a_percentage_score < 100 or record.section_a_percentage_score > 100:
				raise ValidationError(_('SECTION A OVERRALL PERCENTAGE IS NOT VALID \n'+
						'REQUIRED VALID PERCENTAGE IS 100%'))
			elif record.section_b_aspects < 20 or record.section_b_aspects > 20:
				raise ValidationError(_('SECTION B OVERRALL WEIGHT IS NOT VALID \n'+
					'CHOOSE ALL THE BEHAVIORAL ASPECTS,(20) '))
			record.write({'state':'manager'})

	@api.multi
	def submit_hod(self):
		for record in self:
			if record.section_a_percentage_score < 100 or record.section_a_percentage_score > 100:
				raise ValidationError(_('SECTION A OVERRALL PERCENTAGE IS NOT VALID \n'+
						'REQUIRED VALID PERCENTAGE IS 100%'))
			elif record.section_b_aspects < 20 or record.section_b_aspects > 20:
				raise ValidationError(_('SECTION B OVERRALL WEIGHT IS NOT VALID \n'+
					'CHOOSE ALL THE BEHAVIORAL ASPECTS,(20) '))
			record.write({'state':'hod'})

	@api.multi
	def submit_ed(self):
		for record in self:
			if record.section_a_percentage_score < 100 or record.section_a_percentage_score > 100:
				raise ValidationError(_('SECTION A OVERRALL PERCENTAGE IS NOT VALID \n'+
						'REQUIRED VALID PERCENTAGE IS 100%'))
			elif record.section_b_aspects < 20 or record.section_b_aspects > 20:
				raise ValidationError(_('SECTION B OVERRALL WEIGHT IS NOT VALID \n'+
					'CHOOSE ALL THE BEHAVIORAL ASPECTS,(20) '))
			record.write({'state':'ed'})

	@api.multi
	def submit_coo(self):
		for record in self:
			if record.section_a_percentage_score < 100 or record.section_a_percentage_score > 100:
				raise ValidationError(_('SECTION A OVERRALL PERCENTAGE IS NOT VALID \n'+
						'REQUIRED VALID PERCENTAGE IS 100%'))
			elif record.section_b_aspects < 20 or record.section_b_aspects > 20:
				raise ValidationError(_('SECTION B OVERRALL WEIGHT IS NOT VALID \n'+
					'CHOOSE ALL THE BEHAVIORAL ASPECTS,(20) '))
			record.write({'state': 'coo'})

	@api.multi
	def submit_md(self):
		for record in self:
			if record.section_a_percentage_score < 100 or record.section_a_percentage_score > 100:
				raise ValidationError(_('SECTION A OVERRALL PERCENTAGE IS NOT VALID \n'+
					'REQUIRED VALID PERCENTAGE IS 100%'))
			elif record.section_b_aspects < 20 or record.section_b_aspects > 20:
				raise ValidationError(_('SECTION B OVERRALL WEIGHT IS NOT VALID \n'+
					'CHOOSE ALL THE BEHAVIORAL ASPECTS,(20) '))
			record.write({'state': 'md'})


	@api.multi
	def submit_hr(self):
		for record in self:
			if record.section_a_percentage_score < 100 or record.section_a_percentage_score > 100:
				raise ValidationError(_('SECTION A OVERRALL PERCENTAGE IS NOT VALID \n'+
						'REQUIRED VALID PERCENTAGE IS 100%'))
			elif record.section_b_aspects < 20 or record.section_b_aspects > 20:
				raise ValidationError(_('SECTION B OVERRALL WEIGHT IS NOT VALID \n'+
					'CHOOSE ALL THE BEHAVIORAL ASPECTS,(20) '))
			record.write({'state':'hr'})

	@api.multi
	def sendback(self):
		for record in self:
			record_user = self.env['res.users'].browse(record.name.id)
			print('Record Owner Is '+str(record_user.id))
			if record.state == 'manager' and record.job_level == 'officer':
				record.write({'state': 'self'})
			if record.state == 'hod' and record.job_level == 'manager':
				record.write({'state':'self'})
			if record.state == 'hod' and record.job_level == 'officer':
				record.write({'state':'manager'})
			if record.state == 'ed' and record.job_level == 'hod':
				record.write({'state':'self'})
			if record.state in ['coo', 'ed', 'md']:
				record.write({'state': 'self'})
			if record.state in ['hr']:
				if record_user.has_group('pmt.pmt_user') or record_user.has_group('pmt.pmt_officer'):
					record.write({'state': 'hod'})
				if record_user.has_group('pmt.pmt_manager'):
					record.write({'state': 'coo'})
				if record_user.has_group('pmt.pmt_manager_others'):
					record.write({'state':'ed'})
				if record_user.has_group('pmt.pmt_coo') or record_user.has_group('pmt.pmt_other_direct_md_functions'):
					record.write({'state': 'md'})

	@api.multi
	def print_appraisal(self):
		return self.env.ref('pmt.action_print_report').report_action(self)

	#---------------------------------------
	#MESSAGING
	#---------------------------------------


class pmt_appraisal_line(models.Model):
	_name = 'appraisal.line'
	_description = 'Performance Agreement Appraisal Line'

	#----------------------------------------
	#DATABASE
	#----------------------------------------

	name = fields.Char(string="Initial/Task/Planned Activity/Action")
	appraisal_id = fields.Many2one("pmt.main", "Appraisal Reference", ondelete="cascade")
	targets = fields.Text(string="Target & Measure/KPI")
	performance_level = fields.Selection(
		[
			(10,10),
			(8,8),
			(6,6),
			(4,4),
			(2,2)
		],string="Performance Levels")
	actual_level =  fields.Text(string="Actual Achievment")
	evidence = fields.Text(string="Evidence")
	total_score = fields.Selection(
		[
			(10,10),
			(8,8),
			(6,6),
			(4,4),
			(2,2)
		] ,string="Total/10", track_visibility="onchange")
	weighted_score = fields.Float(string="Weighted Score(%)", track_visibility="onchange")
	comments = fields.Text(string='Comments')
	perspective_id = fields.Many2one("pmt.perspective", string="Perspective")
	net_weight = fields.Integer(string="Net Weight(%)")


	#-----------------------------------
	#BUSINESS LOGIC
	#-----------------------------------

	@api.onchange('net_weight', 'total_score')
	def _compute_weighted_score(self):
		if self.net_weight <= 0 and self.total_score <= 0:
			pass
		else:
			self.weighted_score = ((self.total_score/10)*self.net_weight)


	class pmt_appraisal_bh_line(models.Model):
		_name = 'appraisalbh.line'
		_description = 'Behavioral Appraisal Line'

		#--------------------------------------
		#DATABASE
		#--------------------------------------

		name = fields.Char(string="Initial/Task/Planned Activity/Action")
		appraisalbh_id = fields.Many2one("pmt.main", "Appraisal Reference", ondelete="cascade")
		perspective_bh_id = fields.Many2one("pmt.corevalue", string="Perspective")

		targets_bh = fields.Html(related='perspective_bh_id.description',string="Target & Measure/KPI")
		net_weight_bh = fields.Integer(related='perspective_bh_id.net_score',string="Net Weight")

		section_rating = fields.Integer(string="Ratings",track_visibility="onchange")

		actual_level_bh =  fields.Text(string="Actual Achievment")
		evidence_bh = fields.Text(string="Evidence")
		total_score_bh = fields.Selection(
			[
				(1,1),
				(2,2),
				(3,3),
				(4,4),
				(5,5)
			],string="Score/5")
		weighted_score_bh = fields.Float(string="Weighted Score")
		comments = fields.Text(string='Comments')

		#---------------------------------------
		#BUSINESS LOGIC
		#---------------------------------------
		@api.onchange('total_score_bh')
		def _check_score_entered(self):
			for record in self:
				if record.total_score_bh > 5:
					raise UserError(_('VALUES GREATER THAN 5 ARE NOT VALID ENTRIES'))
				else:
					section_rating = self.env['value.rating'].search([])
					for rate in section_rating:
						if record.total_score_bh >= rate.range_from and record.total_score_bh <= rate.range_to:
							record.section_rating = rate.name	
