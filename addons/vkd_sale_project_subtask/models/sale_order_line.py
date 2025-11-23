# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_task(self, project):
        """
        Override to create subtasks based on product subtask templates
        after the main task is created
        """
        # Call parent method to create the main task
        task = super()._timesheet_create_task(project)

        # Create subtasks if product has subtask templates
        if task and self.product_id.subtask_template_ids:
            self._create_subtasks_from_templates(task)

        return task

    def _create_subtasks_from_templates(self, parent_task):
        """
        Create subtasks for the given parent task based on product's subtask templates

        :param parent_task: project.task record (parent task)
        :return: recordset of created subtasks
        """
        self.ensure_one()

        # Get active subtask templates ordered by sequence
        subtask_templates = self.product_id.subtask_template_ids.filtered('active').sorted('sequence')

        if not subtask_templates:
            return self.env['project.task']

        # Prepare subtask values for batch creation
        subtask_vals_list = []
        for template in subtask_templates:
            subtask_vals = self._prepare_subtask_values(parent_task, template)
            subtask_vals_list.append(subtask_vals)

        # Create all subtasks in batch
        subtasks = self.env['project.task'].sudo().create(subtask_vals_list)

        # Post message on parent task about subtasks creation
        if subtasks:
            subtask_names = ', '.join(subtasks.mapped('name'))
            parent_task.message_post(
                body=_("%(count)s subtask(s) created automatically: %(names)s",
                    count=len(subtasks),
                    names=subtask_names
                )
            )

        return subtasks

    def _prepare_subtask_values(self, parent_task, template):
        """
        Prepare values for creating a subtask from a template

        :param parent_task: project.task record (parent task)
        :param template: product.subtask.template record
        :return: dict of values for task creation
        """
        self.ensure_one()

        values = {
            'name': template.name,
            'parent_id': parent_task.id,
            'project_id': parent_task.project_id.id,
            'partner_id': parent_task.partner_id.id,
            'sale_line_id': self.id,
            'sale_order_id': self.order_id.id,
            'company_id': parent_task.company_id.id,
            'description': template.description or '',
            'allocated_hours': template.allocated_hours,
            'display_in_project': False,  # Keep subtasks hidden under parent
            'user_ids': False,  # No assigned users initially
        }

        return values
