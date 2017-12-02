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
    _inherit = 'todo.task'
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