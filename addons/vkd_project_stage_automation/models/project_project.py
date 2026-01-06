# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    stage_automation_ids = fields.One2many(
        'project.stage.automation',
        'project_id',
        string='Stage Automation Rules',
        copy=True,  # ← KEY: Rules are copied when project is copied from template
        help="Automation rules for automatic stage transitions based on conditions"
    )

    stage_automation_count = fields.Integer(
        string='Automation Rules Count',
        compute='_compute_stage_automation_count',
        store=True
    )

    has_stage_automation = fields.Boolean(
        string='Has Stage Automation',
        compute='_compute_has_stage_automation',
        store=True,
        help="Indicates if this project has active automation rules"
    )

    # ==================== PROJECT-LEVEL AUTOMATION ====================
    project_stage_automation_ids = fields.One2many(
        'project.project.stage.automation',
        'project_template_id',
        string='Project Stage Automation Rules',
        copy=True,  # ← Copied when project is duplicated
        help="Automation rules for automatic PROJECT stage transitions based on task conditions"
    )

    project_stage_automation_count = fields.Integer(
        string='Project Automation Rules Count',
        compute='_compute_project_stage_automation_count',
        store=True
    )

    has_project_stage_automation = fields.Boolean(
        string='Has Project Stage Automation',
        compute='_compute_has_project_stage_automation',
        store=True,
        help="Indicates if this project has active project-level automation rules"
    )

    @api.depends('stage_automation_ids', 'stage_automation_ids.active')
    def _compute_stage_automation_count(self):
        """Count active automation rules"""
        for project in self:
            project.stage_automation_count = len(
                project.stage_automation_ids.filtered('active')
            )

    @api.depends('stage_automation_count')
    def _compute_has_stage_automation(self):
        """Check if project has active automation"""
        for project in self:
            project.has_stage_automation = project.stage_automation_count > 0

    @api.depends('project_stage_automation_ids', 'project_stage_automation_ids.active')
    def _compute_project_stage_automation_count(self):
        """Count active project automation rules"""
        for project in self:
            project.project_stage_automation_count = len(
                project.project_stage_automation_ids.filtered('active')
            )

    @api.depends('project_stage_automation_count')
    def _compute_has_project_stage_automation(self):
        """Check if project has active project-level automation"""
        for project in self:
            project.has_project_stage_automation = project.project_stage_automation_count > 0

    def action_view_stage_automation_rules(self):
        """Open task automation rules for this project"""
        self.ensure_one()
        return {
            'name': _('Task Stage Automation Rules'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.stage.automation',
            'view_mode': 'tree,form',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
                'search_default_active': 1,
            },
            'help': """
                <p class="o_view_nocontent_smiling_face">
                    Create your first automation rule
                </p>
                <p>
                    Automation rules automatically change task stages or states based on conditions.
                    For example, automatically move a task to "Testing" when all development subtasks are completed.
                </p>
            """,
        }

    def action_view_project_stage_automation_rules(self):
        """Open project automation rules for this project"""
        self.ensure_one()
        return {
            'name': _('Project Stage Automation Rules'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.project.stage.automation',
            'view_mode': 'tree,form',
            'domain': [('project_template_id', '=', self.id)],
            'context': {
                'default_project_template_id': self.id,
                'search_default_active': 1,
            },
            'help': """
                <p class="o_view_nocontent_smiling_face">
                    Create your first project automation rule
                </p>
                <p>
                    Project automation rules automatically change the PROJECT stage based on task completion.
                    For example, automatically move project to "Completed" when all tasks are done.
                </p>
            """,
        }
