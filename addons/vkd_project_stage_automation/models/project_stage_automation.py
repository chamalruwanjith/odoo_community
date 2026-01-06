# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectStageAutomation(models.Model):
    _name = 'project.stage.automation'
    _description = 'Project Stage Automation Rule'
    _order = 'project_id, sequence, id'

    name = fields.Char(
        string='Rule Name',
        required=True,
        translate=True,
        help="Name of the automation rule"
    )

    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        ondelete='cascade',
        index=True,
        help="Project to which this rule belongs"
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
    trigger_stage_id = fields.Many2one(
        'project.task.type',
        string='When Entering Stage',
        required=True,
        ondelete='cascade',
        help="The automation will trigger when a task enters this stage"
    )

    trigger_stage_name = fields.Char(
        related='trigger_stage_id.name',
        string='Trigger Stage Name',
        readonly=True,
        store=True
    )

    # ==================== CONDITION ====================
    condition_type = fields.Selection([
        ('always', 'Always Execute'),
        ('all_subtasks_done', 'All Subtasks Completed'),
        ('all_dependencies_done', 'All Dependencies Completed'),
        ('subtasks_percentage', 'Subtasks Completion Percentage'),
        ('no_open_subtasks', 'No Open Subtasks (Done or Cancelled)'),
    ], string='Condition Type', default='always', required=True,
        help="Condition that must be met for the rule to execute")

    condition_value = fields.Float(
        string='Threshold (%)',
        default=100.0,
        help="For percentage-based conditions, the minimum percentage required"
    )

    condition_description = fields.Text(
        string='Condition Description',
        compute='_compute_condition_description',
        store=False
    )

    # ==================== ACTION ====================
    action_type = fields.Selection([
        ('move_stage', 'Move to Stage'),
        ('set_state', 'Set Task State'),
        ('both', 'Move Stage and Set State'),
    ], string='Action Type', default='move_stage', required=True,
        help="Action to perform when conditions are met")

    action_stage_id = fields.Many2one(
        'project.task.type',
        string='Move to Stage',
        ondelete='set null',
        help="Stage to move the task to"
    )

    action_stage_name = fields.Char(
        related='action_stage_id.name',
        string='Action Stage Name',
        readonly=True,
        store=True
    )

    action_state = fields.Selection([
        ('01_in_progress', 'In Progress'),
        ('02_changes_requested', 'Changes Requested'),
        ('03_approved', 'Approved'),
        ('1_done', 'Done'),
        ('1_canceled', 'Cancelled'),
        ('04_waiting_normal', 'Waiting'),
    ], string='Set Task State',
        help="State to set on the task")

    action_description = fields.Text(
        string='Action Description',
        compute='_compute_action_description',
        store=False
    )

    # ==================== METADATA ====================
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='project_id.company_id',
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
    @api.depends('condition_type', 'condition_value')
    def _compute_condition_description(self):
        """Generate human-readable condition description"""
        for rule in self:
            if rule.condition_type == 'always':
                rule.condition_description = _("No conditions (always execute)")
            elif rule.condition_type == 'all_subtasks_done':
                rule.condition_description = _("All subtasks must be marked as Done or Cancelled")
            elif rule.condition_type == 'all_dependencies_done':
                rule.condition_description = _("All blocking dependencies must be completed")
            elif rule.condition_type == 'subtasks_percentage':
                rule.condition_description = _("At least %.0f%% of subtasks must be completed") % rule.condition_value
            elif rule.condition_type == 'no_open_subtasks':
                rule.condition_description = _("Task must have no open subtasks")
            else:
                rule.condition_description = ""

    @api.depends('action_type', 'action_stage_id', 'action_state')
    def _compute_action_description(self):
        """Generate human-readable action description"""
        for rule in self:
            descriptions = []

            if rule.action_type in ('move_stage', 'both'):
                if rule.action_stage_id:
                    descriptions.append(_("Move to '%s' stage") % rule.action_stage_id.name)
                else:
                    descriptions.append(_("Move to stage (not configured)"))

            if rule.action_type in ('set_state', 'both'):
                if rule.action_state:
                    state_label = dict(rule._fields['action_state'].selection).get(rule.action_state, '')
                    descriptions.append(_("Set state to '%s'") % state_label)
                else:
                    descriptions.append(_("Set state (not configured)"))

            rule.action_description = ' AND '.join(descriptions) if descriptions else ""

    # ==================== CONSTRAINTS ====================
    @api.constrains('action_type', 'action_stage_id', 'action_state')
    def _check_action_configuration(self):
        """Ensure action fields are properly configured"""
        for rule in self:
            if rule.action_type in ('move_stage', 'both') and not rule.action_stage_id:
                raise ValidationError(
                    _("Rule '%s': You must select a stage to move to when action type is 'Move to Stage'") % rule.name
                )
            if rule.action_type in ('set_state', 'both') and not rule.action_state:
                raise ValidationError(
                    _("Rule '%s': You must select a state when action type is 'Set Task State'") % rule.name
                )

    @api.constrains('condition_value')
    def _check_condition_value(self):
        """Ensure condition value is valid"""
        for rule in self:
            if rule.condition_type == 'subtasks_percentage':
                if rule.condition_value < 0 or rule.condition_value > 100:
                    raise ValidationError(
                        _("Rule '%s': Percentage must be between 0 and 100") % rule.name
                    )

    @api.constrains('trigger_stage_id', 'action_stage_id')
    def _check_stage_project_consistency(self):
        """Ensure trigger and action stages belong to the same project"""
        for rule in self:
            if rule.trigger_stage_id and rule.project_id not in rule.trigger_stage_id.project_ids:
                raise ValidationError(
                    _("Rule '%s': Trigger stage '%s' is not available in project '%s'") %
                    (rule.name, rule.trigger_stage_id.name, rule.project_id.name)
                )
            if rule.action_stage_id and rule.project_id not in rule.action_stage_id.project_ids:
                raise ValidationError(
                    _("Rule '%s': Action stage '%s' is not available in project '%s'") %
                    (rule.name, rule.action_stage_id.name, rule.project_id.name)
                )

    # ==================== BUSINESS METHODS ====================
    def check_condition(self, task):
        """
        Check if the rule's condition is met for the given task

        :param task: project.task record
        :return: bool
        """
        self.ensure_one()

        if self.condition_type == 'always':
            return True

        elif self.condition_type == 'all_subtasks_done':
            # No subtasks = condition met
            if not task.child_ids:
                return True
            # All subtasks must be in closed state
            closed_states = ['1_done', '1_canceled']
            return all(child.state in closed_states for child in task.child_ids)

        elif self.condition_type == 'all_dependencies_done':
            # No dependencies = condition met
            if not task.depend_on_ids:
                return True
            # All dependencies must be closed
            closed_states = ['1_done', '1_canceled']
            return all(dep.state in closed_states for dep in task.depend_on_ids)

        elif self.condition_type == 'subtasks_percentage':
            # No subtasks = condition met
            if not task.child_ids:
                return True
            # Check completion percentage
            percentage = task.subtask_completion_percentage * 100
            return percentage >= self.condition_value

        elif self.condition_type == 'no_open_subtasks':
            # No subtasks OR all subtasks closed
            if not task.child_ids:
                return True
            closed_states = ['1_done', '1_canceled']
            return all(child.state in closed_states for child in task.child_ids)

        return False

    def apply_action(self, task):
        """
        Apply the rule's action to the given task

        :param task: project.task record
        :return: bool (True if action was applied)
        """
        self.ensure_one()

        if not task:
            return False

        # Prepare values to update
        vals = {}
        action_messages = []

        # Move to stage
        if self.action_type in ('move_stage', 'both') and self.action_stage_id:
            # Only move if different from current stage
            if task.stage_id != self.action_stage_id:
                vals['stage_id'] = self.action_stage_id.id
                action_messages.append(
                    _("Moved to stage '%s'") % self.action_stage_id.name
                )

        # Set state
        if self.action_type in ('set_state', 'both') and self.action_state:
            # Only set if different from current state
            if task.state != self.action_state:
                vals['state'] = self.action_state
                state_label = dict(self._fields['action_state'].selection).get(self.action_state, '')
                action_messages.append(
                    _("State changed to '%s'") % state_label
                )

        # Apply changes if any
        if vals:
            # Use sudo to avoid permission issues during automation
            task.sudo().write(vals)

            # Update execution stats
            self.sudo().write({
                'execution_count': self.execution_count + 1,
                'last_execution_date': fields.Datetime.now(),
            })

            # Post message on task
            message = _("🤖 <b>Automation Rule Applied:</b> %s<br/>%s") % (
                self.name,
                '<br/>'.join(action_messages)
            )
            task.message_post(body=message, subtype_xmlid='mail.mt_note')

            return True

        return False

    # ==================== VIEWS ====================
    def name_get(self):
        """Custom name display"""
        result = []
        for rule in self:
            name = f"[{rule.project_id.name}] {rule.name}"
            result.append((rule.id, name))
        return result

    def action_view_stage_automation_rules(self):
        """
        Action to view all automation rules for the same project
        """
        self.ensure_one()
        return {
            'name': _('Stage Automation Rules - %s', self.project_id.name),
            'type': 'ir.actions.act_window',
            'res_model': 'project.stage.automation',
            'view_mode': 'tree,form',
            'domain': [('project_id', '=', self.project_id.id)],
            'context': {
                'default_project_id': self.project_id.id,
                'search_default_active': 1,
            },
        }
