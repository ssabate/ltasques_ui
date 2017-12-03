# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Tag(models.Model):
    _name = 'todo.task.tag'
    name = fields.Char('Nom')
    task_ids = fields.Many2many('todo.task',string='Llista tasques')


class Stage(models.Model):
    _name = 'todo.task.stage'
    _order = 'sequence,name'
    # String fields:
    name = fields.Char('Nom')
    desc = fields.Text('Descripcio')
    state = fields.Selection([('draft','New'), ('open','Started'),('done','Closed')],'State')
    docs = fields.Html('Documentacio')
    # Numeric fields:
    sequence = fields.Integer('Sequencia')
    perc_complete = fields.Float('% Complet', (3, 2))
    # Date fields:
    date_effective = fields.Date('Data d\'efecte')
    date_changed = fields.Datetime('Ultim canvi')
    # Other fields:
    fold = fields.Boolean('Plegat?')
    image = fields.Binary('Imatge')
    # Relational fields
    #task_id = fields.One2many('todo.task','Llista tasques')

    task_id = fields.One2many(
        'todo.task',
        # related model
        'stage_id',
        # field for "this" on related model
        'Tasks in this stage')

class TodoTask(models.Model):

    _name = 'todo.task'
    _inherit = ['mail.thread']
    user_id = fields.Many2one('res.users','Responsable')
    date_deadline = fields.Date('Data caducitat')
    name = fields.Char(help="Què s'ha de fer?")
    isDone = fields.Boolean('Feta?')
    isActive = fields.Boolean('Activa?', default=True)

    @api.multi
    def do_clear_done(self):
        domain = [('isDone', '=', True),
                  '|', ('user_id', '=', self.env.uid),
                  ('user_id', '=', False)]

        done_recs = self.search(domain)
        done_recs.write({'isActive': False})
        return True

    @api.one
    def do_toggle_done(self):
        if self.user_id != self.env.user:
            raise Exception('Only the responsible can do this!')
        else:
            return super(TodoTask, self).do_toggle_done()


    stage_id = fields.Many2one('todo.task.stage', 'Estat')
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')
    stage_fold = fields.Boolean(
        'Stage Folded?',
        compute='_compute_stage_fold')
    stage_state = fields.Selection(
        related='stage_id.state',
        string='Stage State')
    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold

    @api.one
    def compute_user_todo_count(self):
        self.user_todo_count = self.search_count(
                [('user_id', '=', self.user_id.id)])

    user_todo_count = fields.Integer(
            'User To-Do Count',
            compute='compute_user_todo_count')

    effort_estimate = fields.Integer('Esforç estimat')