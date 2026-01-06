# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Add flag to prevent infinite loops
    _automation_in_progress = False

    def write(self, vals):
        """
        Override write to trigger automation rules when stage or state changes
        """
        # Call parent write first
        result = super(ProjectTask, self).write(vals)

        # Trigger automation on stage change OR state change
        if ('stage_id' in vals or 'state' in vals) and not self._automation_in_progress:
            # Set flag to prevent recursive calls
            self._automation_in_progress = True
            try:
                # Apply automation on current task(s)
                self._apply_stage_automation()

                # IMPORTANT: Also trigger automation on parent tasks
                # This allows subtask changes to trigger parent automation
                self._trigger_parent_automation()
            finally:
                # Reset flag
                self._automation_in_progress = False

        return result

    def _apply_stage_automation(self):
        """
        Apply automation rules when task enters a new stage
        """
        for task in self:
            # Skip if task has no project (private tasks)
            if not task.project_id:
                continue

            # Skip if project has no automation rules
            if not task.project_id.has_stage_automation:
                continue

            # Get automation rules for current project and stage
            rules = self.env['project.stage.automation'].search([
                ('project_id', '=', task.project_id.id),
                ('trigger_stage_id', '=', task.stage_id.id),
                ('active', '=', True),
            ], order='sequence, id')

            if not rules:
                continue

            _logger.info(
                f"Stage automation: Found {len(rules)} rule(s) for task '{task.name}' "
                f"entering stage '{task.stage_id.name}'"
            )

            # Apply each matching rule
            for rule in rules:
                try:
                    # Check if condition is met
                    if rule.check_condition(task):
                        _logger.info(
                            f"Stage automation: Condition met for rule '{rule.name}', applying action"
                        )
                        # Apply action
                        rule.apply_action(task)
                    else:
                        _logger.debug(
                            f"Stage automation: Condition not met for rule '{rule.name}', skipping"
                        )
                except Exception as e:
                    _logger.error(
                        f"Stage automation: Error applying rule '{rule.name}' on task '{task.name}': {str(e)}"
                    )
                    # Continue with next rule even if one fails
                    continue

    def _trigger_parent_automation(self):
        """
        Trigger automation on parent tasks when subtasks change.
        This is critical for conditions like "all_subtasks_done" to work properly.
        """
        # Get all unique parent tasks from current tasks
        parent_tasks = self.mapped('parent_id').filtered(lambda p: p.project_id.has_stage_automation)

        if not parent_tasks:
            return

        _logger.info(
            f"Stage automation: Triggering parent automation for {len(parent_tasks)} parent task(s) "
            f"due to subtask changes"
        )

        # Re-evaluate automation rules on parent tasks
        # Use the parent's current stage as trigger
        for parent in parent_tasks:
            # Get automation rules for parent's current stage
            rules = self.env['project.stage.automation'].search([
                ('project_id', '=', parent.project_id.id),
                ('trigger_stage_id', '=', parent.stage_id.id),
                ('active', '=', True),
            ], order='sequence, id')

            if not rules:
                continue

            _logger.info(
                f"Stage automation: Checking {len(rules)} rule(s) for parent task '{parent.name}' "
                f"after subtask change"
            )

            # Apply each matching rule
            for rule in rules:
                try:
                    # Check if condition is met (e.g., all_subtasks_done)
                    if rule.check_condition(parent):
                        _logger.info(
                            f"Stage automation: Condition met for rule '{rule.name}' on parent task, applying action"
                        )
                        # Apply action
                        rule.apply_action(parent)
                    else:
                        _logger.debug(
                            f"Stage automation: Condition not met for rule '{rule.name}' on parent task"
                        )
                except Exception as e:
                    _logger.error(
                        f"Stage automation: Error applying rule '{rule.name}' on parent task '{parent.name}': {str(e)}"
                    )
                    continue

    @api.model
    def create(self, vals):
        """
        Override create to trigger automation for newly created tasks
        """
        # Create task first
        task = super(ProjectTask, self).create(vals)

        # Trigger automation if stage is set
        if task.stage_id and task.project_id and task.project_id.has_stage_automation:
            task._apply_stage_automation()

        return task

    def action_view_automation_rules(self):
        """
        Action to view automation rules for current task's project
        """
        self.ensure_one()

        if not self.project_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('No Project'),
                    'message': _('This task is not linked to a project'),
                    'type': 'warning',
                }
            }

        return self.project_id.action_view_stage_automation_rules()
