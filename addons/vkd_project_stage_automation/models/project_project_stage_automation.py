# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectProjectStageAutomation(models.Model):
    _name = 'project.project.stage.automation'
    _description = 'Project Stage Automation Rule'
    _order = 'project_template_id, sequence, id'

    name = fields.Char(
        string='Rule Name',
        required=True,
        translate=True,
        help="Name of the project automation rule"
    )

    project_template_id = fields.Many2one(
        'project.project',
        string='Project Template',
        ondelete='cascade',
        index=True,
        help="Project template to which this rule belongs (optional - can apply to all projects)"
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help="Inactive rules will not be executed"
    )

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of execution when multiple rules match"
    )

    # ==================== TRIGGER ====================
    trigger_type = fields.Selection([
        ('task_stage_change', 'When Task Reaches Stage'),
        ('tasks_completion', 'When Tasks Completed'),
    ], string='Trigger Type', default='tasks_completion', required=True,
        help="What triggers this project automation")

    trigger_task_stage_id = fields.Many2one(
        'project.task.type',
        string='When Task Reaches Stage',
        help="Trigger when any task reaches this stage"
    )

    # ==================== CONDITION ====================
    condition_type = fields.Selection([
        ('all_tasks_done', 'All Tasks Completed'),
        ('tasks_percentage', 'Tasks Completion Percentage'),
        ('all_tasks_in_stage', 'All Tasks in Specific Stage'),
        ('always', 'Always Execute'),
    ], string='Condition Type', default='all_tasks_done', required=True,
        help="Condition that must be met for the rule to execute")

    condition_value = fields.Float(
        string='Threshold (%)',
        default=100.0,
        help="For percentage-based conditions"
    )

    condition_task_stage_id = fields.Many2one(
        'project.task.type',
        string='Required Task Stage',
        help="For 'All Tasks in Specific Stage' condition"
    )

    condition_description = fields.Text(
        string='Condition Description',
        compute='_compute_condition_description'
    )

    # ==================== ACTION ====================
    action_type = fields.Selection([
        ('move_project_stage', 'Move Project to Stage'),
    ], string='Action Type', default='move_project_stage', required=True,
        help="Action to perform when conditions are met")

    action_project_stage_id = fields.Many2one(
        'project.project.stage',
        string='Move Project to Stage',
        help="Project stage to move to"
    )

    action_description = fields.Text(
        string='Action Description',
        compute='_compute_action_description'
    )

    # ==================== METADATA ====================
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='project_template_id.company_id',
        store=True,
        readonly=True
    )

    execution_count = fields.Integer(
        string='Executions',
        default=0,
        readonly=True,
        help="Number of times this rule has been executed"
    )

    last_execution_date = fields.Datetime(
        string='Last Execution',
        readonly=True,
        help="Last time this rule was executed"
    )

    # ==================== COMPUTE METHODS ====================
    @api.depends('condition_type', 'condition_value', 'condition_task_stage_id')
    def _compute_condition_description(self):
        """Generate human-readable condition description"""
        for rule in self:
            if rule.condition_type == 'always':
                rule.condition_description = _("No conditions (always execute)")
            elif rule.condition_type == 'all_tasks_done':
                rule.condition_description = _("All tasks in project must be completed (Done or Cancelled)")
            elif rule.condition_type == 'tasks_percentage':
                rule.condition_description = _("At least %.0f%% of tasks must be completed") % rule.condition_value
            elif rule.condition_type == 'all_tasks_in_stage':
                stage_name = rule.condition_task_stage_id.name if rule.condition_task_stage_id else "?"
                rule.condition_description = _("All tasks must be in '%s' stage") % stage_name
            else:
                rule.condition_description = ""

    @api.depends('action_type', 'action_project_stage_id')
    def _compute_action_description(self):
        """Generate human-readable action description"""
        for rule in self:
            if rule.action_type == 'move_project_stage':
                if rule.action_project_stage_id:
                    rule.action_description = _("Move project to '%s' stage") % rule.action_project_stage_id.name
                else:
                    rule.action_description = _("Move project to stage (not configured)")
            else:
                rule.action_description = ""

    # ==================== CONSTRAINTS ====================
    @api.constrains('action_type', 'action_project_stage_id')
    def _check_action_configuration(self):
        """Ensure action fields are properly configured"""
        for rule in self:
            if rule.action_type == 'move_project_stage' and not rule.action_project_stage_id:
                raise ValidationError(
                    _("Rule '%s': You must select a project stage to move to") % rule.name
                )

    @api.constrains('condition_value')
    def _check_condition_value(self):
        """Ensure condition value is valid"""
        for rule in self:
            if rule.condition_type == 'tasks_percentage':
                if rule.condition_value < 0 or rule.condition_value > 100:
                    raise ValidationError(
                        _("Rule '%s': Percentage must be between 0 and 100") % rule.name
                    )

    # ==================== BUSINESS METHODS ====================
    def check_condition(self, project):
        """
        Check if the rule's condition is met for the given project

        :param project: project.project record
        :return: bool
        """
        self.ensure_one()

        if self.condition_type == 'always':
            return True

        elif self.condition_type == 'all_tasks_done':
            # Get all active tasks in project
            tasks = project.task_ids.filtered(lambda t: t.active)
            if not tasks:
                return True  # No tasks = condition met
            # All tasks must be in closed state
            closed_states = ['1_done', '1_canceled']
            return all(task.state in closed_states for task in tasks)

        elif self.condition_type == 'tasks_percentage':
            # Get all active tasks
            tasks = project.task_ids.filtered(lambda t: t.active)
            if not tasks:
                return True
            # Calculate completion percentage
            closed_states = ['1_done', '1_canceled']
            completed = len([t for t in tasks if t.state in closed_states])
            percentage = (completed / len(tasks)) * 100
            return percentage >= self.condition_value

        elif self.condition_type == 'all_tasks_in_stage':
            if not self.condition_task_stage_id:
                return False
            # Get all active tasks
            tasks = project.task_ids.filtered(lambda t: t.active)
            if not tasks:
                return True
            # All tasks must be in specified stage
            return all(task.stage_id == self.condition_task_stage_id for task in tasks)

        return False

    def apply_action(self, project):
        """
        Apply the rule's action to the given project

        :param project: project.project record
        :return: bool (True if action was applied)
        """
        self.ensure_one()

        if not project:
            return False

        # Prepare values to update
        vals = {}
        action_messages = []

        # Move project to stage
        if self.action_type == 'move_project_stage' and self.action_project_stage_id:
            # Only move if different from current stage
            if project.stage_id != self.action_project_stage_id:
                vals['stage_id'] = self.action_project_stage_id.id
                action_messages.append(
                    _("Project moved to stage '%s'") % self.action_project_stage_id.name
                )

        # Apply changes if any
        if vals:
            # Use sudo to avoid permission issues during automation
            project.sudo().write(vals)

            # Update execution stats
            self.sudo().write({
                'execution_count': self.execution_count + 1,
                'last_execution_date': fields.Datetime.now(),
            })

            # Post message on project
            message = _("🤖 <b>Project Automation Rule Applied:</b> %s<br/>%s") % (
                self.name,
                '<br/>'.join(action_messages)
            )
            project.message_post(body=message, subtype_xmlid='mail.mt_note')

            return True

        return False

    def name_get(self):
        """Custom name display"""
        result = []
        for rule in self:
            if rule.project_template_id:
                name = f"[{rule.project_template_id.name}] {rule.name}"
            else:
                name = f"[All Projects] {rule.name}"
            result.append((rule.id, name))
        return result
