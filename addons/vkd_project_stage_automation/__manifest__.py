# -*- coding: utf-8 -*-
{
    'name': 'Project Stage Automation',
    'version': '19.0.1.0.0',
    'category': 'Services/Project',
    'summary': 'Automatically change task stages based on configurable rules',
    'description': """
Project Stage Automation
========================
This module enables automatic stage transitions for tasks based on configurable rules.

Key Features:
-------------
* Configure automation rules on projects (or project templates)
* Rules automatically copied when project is created from template
* Multiple trigger types: stage entry, state change
* Multiple condition types: always, all subtasks done, dependencies done, percentage
* Multiple action types: move to stage, set state
* Full integration with Odoo's project workflow
* **Subtask-aware**: Automatically triggers parent task automation when subtasks change
* Configurable per project for maximum flexibility
* Perfect integration with vkd_sale_project_subtask module

Use Cases:
----------
* Automatically move task to "Testing" when all development subtasks are completed
* Auto-close task when all dependencies are done
* Move to "Review" when 100% of subtasks are complete
* Set task state to "Done" when entering "Completed" stage
* Parent task auto-advances when all child subtasks are complete

Template Support:
-----------------
Configure automation rules once on a project template, and all projects created
from that template will inherit the rules automatically.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_stage_automation_views.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
