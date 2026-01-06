# Project Stage Automation

## Overview

This module enables automatic stage transitions for tasks based on configurable rules, with full support for project templates.

## Features

- ✅ **Configurable Automation Rules**: Define when and how tasks should automatically change stages
- ✅ **Project Template Support**: Configure rules once on a template, inherit on all projects created from it
- ✅ **Multiple Trigger Types**: Stage entry
- ✅ **Multiple Condition Types**: Always, all subtasks done, dependencies done, percentage complete
- ✅ **Multiple Action Types**: Move to stage, set state, or both
- ✅ **Execution Tracking**: Monitor how many times rules have been executed
- ✅ **Full Integration**: Seamlessly integrates with Odoo's project workflow

## Installation

1. Copy the `vkd_project_stage_automation` module to your Odoo addons directory
2. Update the app list: Go to Apps → Update Apps List
3. Search for "Project Stage Automation"
4. Click Install

## Configuration

### Method 1: Configure on Project Template (Recommended)

1. Go to **Project → Configuration → Projects**
2. Create or open a project template
3. Go to the **Stage Automation** tab
4. Add automation rules:
   - **Name**: Descriptive name for the rule
   - **Trigger**: Which stage triggers this rule
   - **Condition**: What must be true for the rule to execute
   - **Action**: What to do when conditions are met

5. Link the template to a product (for sale_project integration)
6. All projects created from this template will inherit the automation rules!

### Method 2: Configure on Individual Project

1. Go to **Project → All Projects**
2. Open a project
3. Go to the **Stage Automation** tab
4. Add automation rules as needed

### Method 3: Global Management

1. Go to **Project → Configuration → Stage Automation**
2. View and manage all automation rules across all projects
3. Filter by project, condition type, or action type

## Usage Examples

### Example 1: Development Workflow

**Scenario**: Automatically move task to Testing when all development subtasks are complete.

**Configuration**:
```
Rule Name: Auto-move to Testing
Trigger: Development stage
Condition: All Subtasks Completed
Action: Move to "Testing" stage
```

**Result**: When a developer completes all subtasks in the Development stage, the task automatically moves to Testing.

### Example 2: Quality Assurance

**Scenario**: Mark task as Done when 100% of test subtasks are complete.

**Configuration**:
```
Rule Name: Auto-complete Task
Trigger: Testing stage
Condition: Subtasks Completion Percentage = 100%
Action: Move to "Done" stage AND Set state to "Done"
```

**Result**: When all testing subtasks are done, the task is automatically completed.

### Example 3: Dependency Management

**Scenario**: Resume work automatically when blocking dependencies are resolved.

**Configuration**:
```
Rule Name: Resume after dependencies
Trigger: Waiting stage
Condition: All Dependencies Completed
Action: Move to "In Progress" stage
```

**Result**: When the last blocking dependency is completed, the task automatically moves back to In Progress.

### Example 4: Template-Based Consistency

**Scenario**: Ensure all website development projects follow the same workflow.

**Setup**:
1. Create "Website Development Template" project
2. Add stages: Design → Frontend → Backend → Testing → Done
3. Add automation rules:
   - Design complete → Auto-move to Frontend
   - Frontend complete → Auto-move to Backend
   - Backend complete → Auto-move to Testing
   - Testing complete → Auto-mark Done

4. Link template to "Website Development Service" product
5. Every sale order for this service creates a project with these automation rules!

## Condition Types

| Condition | Description | Use Case |
|-----------|-------------|----------|
| **Always Execute** | No conditions, action is immediate | Quick stage transitions |
| **All Subtasks Completed** | All child tasks must be Done or Cancelled | Task breakdown workflows |
| **All Dependencies Completed** | All blocking tasks must be completed | Dependency management |
| **Subtasks Percentage** | Specified % of subtasks must be done | Progressive workflows |
| **No Open Subtasks** | Task has no subtasks or all are closed | Flexible completion |

## Action Types

| Action | Description | Result |
|--------|-------------|--------|
| **Move to Stage** | Changes task's stage (Kanban column) | Visual workflow progression |
| **Set Task State** | Changes task's internal state | Status tracking |
| **Both** | Performs both actions | Complete automation |

## Technical Details

### Models

#### `project.stage.automation`
Main model storing automation rules.

**Key Fields**:
- `name`: Rule name
- `project_id`: Related project (rules are copied with project)
- `trigger_stage_id`: Stage that triggers the rule
- `condition_type`: Type of condition to check
- `action_type`: Type of action to perform
- `action_stage_id`: Target stage for move action
- `action_state`: Target state for state action

**Key Methods**:
- `check_condition(task)`: Evaluates if condition is met
- `apply_action(task)`: Performs the configured action

#### `project.project` (inherited)
**Added Fields**:
- `stage_automation_ids`: One2many to automation rules (copy=True)
- `stage_automation_count`: Count of active rules
- `has_stage_automation`: Boolean indicator

#### `project.task` (inherited)
**Modified Methods**:
- `write()`: Triggers automation when stage changes
- `create()`: Triggers automation for new tasks

### Automation Flow

```
Task Stage Changed
    ↓
Check if project has automation rules
    ↓
Find rules matching new stage
    ↓
For each rule (in sequence order):
    ↓
    Check condition
    ↓
    If met: Apply action
    ↓
    Post message in task chatter
    ↓
    Update execution stats
```

### Template Copying

When a project is copied (including from templates):
1. All automation rules are automatically copied (`copy=True`)
2. Each rule maintains its configuration
3. Stage references are updated to new project's stages
4. Execution counts reset to 0

## Best Practices

### 1. Use Descriptive Names
```
✅ Good: "Auto-move to Testing when dev complete"
❌ Bad: "Rule 1"
```

### 2. Set Appropriate Sequences
Rules with lower sequence numbers execute first. Use this for priority:
```
Sequence 10: Critical automation
Sequence 20: Normal automation
Sequence 30: Optional automation
```

### 3. Test on Templates First
Configure and test automation rules on project templates before deploying to production projects.

### 4. Monitor Execution Counts
Check the execution count field to see which rules are most used and identify potential issues.

### 5. Use "Always Execute" Sparingly
The "Always Execute" condition can cause unexpected automation. Use specific conditions when possible.

### 6. Leverage Template Inheritance
Configure rules on templates for consistency across similar projects.

## Troubleshooting

### Rule Not Triggering

**Check**:
1. Is the rule active?
2. Is the project linked correctly?
3. Is the trigger stage correct?
4. Are conditions actually met?
5. Check server logs for errors

### Infinite Loops

The module includes loop prevention:
- Only one automation cycle per stage change
- Actions that change stage don't trigger new automation in same write cycle

### Stage Not Available

**Error**: "Action stage 'X' is not available in project 'Y'"

**Solution**: Ensure the action stage is linked to the project's available stages (type_ids).

## Dependencies

- `project`: Core project management module

## Compatibility

- **Odoo Version**: 19.0
- **Integration**: Works seamlessly with:
  - `sale_project`: Automation rules copied from product templates
  - `project_enterprise`: Full compatibility
  - Custom project modules: Extends standard write() method

## Support

For issues or feature requests, please contact your system administrator or module maintainer.

## License

LGPL-3

## Credits

**Author**: Your Company
**Website**: https://www.yourcompany.com
**Version**: 19.0.1.0.0

---

**Version**: 19.0.1.0.0
**Category**: Services/Project
**Odoo Version**: 19.0
