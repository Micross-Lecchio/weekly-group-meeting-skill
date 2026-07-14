---
name: managing-weekly-group-meetings
description: Use when preparing recurring weekly group meetings, tracking labeled multi-week research tasks, handling [非任务] workspace-rule maintenance sessions, maintaining per-task weekly workspaces, generating meeting documents or presentations, or archiving completed project stages.
---

# Managing Weekly Group Meetings

## Overview

Use this Skill to manage long-running, labeled tasks across weekly group meetings. Keep the global task dashboard, weekly records, task-local temporary files, task-local deliverables, and completed-stage archives consistent.

`[非任务]` sessions are maintenance or rule-editing sessions for the workspace itself. They bypass stage-task registration and must not be forced into a permanent research-task label.

Project-specific permissions and file boundaries are defined by the root `AGENTS.md` and always take priority.

## Required Files

At the project root:

```text
AGENTS.md
TASKS.md
weekly/
completed-projects/
```

Each week contains one folder per active task:

```text
weekly/YYYY-Www/
├─ README.md
├─ tasks/
│  └─ [label]任务名称/
│     ├─ [label]任务记录.md
│     ├─ temporary/
│     ├─ deliverables/
│     └─ working/
├─ deliverables/
└─ non-task/
```

Use root-level `weekly/YYYY-Www/deliverables/` only for cross-task weekly summaries or group-meeting materials. Use `weekly/YYYY-Www/non-task/` only for `[非任务]` maintenance notes.

Templates are stored beside this Skill in `templates/`. The helper script is `scripts/init_week.py`.

## Trigger Conditions

Use this Skill when the user:

- starts or continues a labeled research task;
- asks to prepare weekly group-meeting material;
- requests a weekly summary, Word document, or presentation;
- asks to review earlier work with the same label;
- pauses, resumes, completes, or archives a multi-week task;
- asks to view or update the overall task progress;
- starts a `[非任务]` maintenance session to update workspace rules, the Skill, templates, scripts, indexes, or directory organization.

Do not use it for unrelated one-off work that does not belong to the weekly group-meeting workspace.

## Mandatory Workflow

### 1. Read Local Rules

Read the root `AGENTS.md` before making changes.

Never access paths outside the project root without explicit user authorization.

### 2. Validate the Label

If the user explicitly prefixes a request with `[非任务]`:

- treat it as a workspace-maintenance session;
- do not require a research-task label;
- do not create or update a stage-task row in `TASKS.md`;
- do not create a formal task record or task deliverable unless the user explicitly asks;
- place optional maintenance notes under `weekly/YYYY-Www/non-task/`;
- still read local rules, protect files, and verify any changes.

Each stage task requires a label in square brackets, for example:

```text
[paper]
[burnup]
[cf252]
```

If the user omitted the label:

- remind the user to provide one;
- do not invent a permanent label;
- do not create formal deliverables;
- analysis and planning may continue.

### 3. Read the Global Dashboard

Read root `TASKS.md`.

Skip this step only for `[非任务]` sessions that do not change stage-task progress.

Determine whether the label already exists.

- Existing label: continue that stage task, preserve its start date, and add the current week only if work is actually performed.
- New label: create a new stage-task row with today's date as the start date.
- Ambiguous duplicate meaning: ask the user to choose a more specific label.

### 4. Determine the ISO Week

Use ISO format:

```text
YYYY-Www
```

Example:

```text
2026-W29
```

Use the helper script when suitable:

```bash
python .agents/skills/managing-weekly-group-meetings/scripts/init_week.py
```

To initialize a task-local workspace:

```bash
python .agents/skills/managing-weekly-group-meetings/scripts/init_week.py --week 2026-W29 --label "[paper]" --task-name "任务名称"
```

The script must not overwrite existing files.

### 5. Review History

Before continuing an existing label, search within the project root for:

- matching task records under `weekly/*/tasks/`;
- matching entries in weekly `README.md` files;
- the most recent "下一步工作";
- matching deliverables;
- matching completed-project archives.

Do not rely only on chat history.

### 6. Create or Update the Weekly Task Record

Store each work item at:

```text
weekly/YYYY-Www/tasks/[label]任务名称/[label]任务记录.md
```

Use `templates/task-record.md`.

Update it during the work, not only after completion.

It must show:

- goal and original user request;
- inputs and modification permissions;
- historical context;
- work performed;
- important reasoning;
- temporary files;
- formal deliverables;
- result;
- unresolved issues;
- next step;
- user confirmations.

### 7. Separate Temporary Files and Deliverables

Temporary work:

```text
weekly/YYYY-Www/tasks/[label]任务名称/temporary/
```

Formal results:

```text
weekly/YYYY-Www/tasks/[label]任务名称/deliverables/
```

All formal result filenames begin with the task label:

```text
[label]filename.ext
```

Do not overwrite existing formal deliverables unless the user explicitly requests it. Prefer version suffixes.

Use:

```text
weekly/YYYY-Www/tasks/[label]任务名称/working/
```

for task-specific source trees, drafts, scripts, extracted text, calculation folders, or other files that are neither temporary scratch nor final deliverables. If an existing root-level working tree is already referenced by tests or code paths, leave it in place and document ownership from the task record instead of moving it.

### 8. Update All Three Records

Before ending a work session, synchronize:

1. root `TASKS.md`;
2. weekly `README.md`;
3. the labeled task record.

For `[非任务]` sessions, synchronize only the files directly affected by the maintenance work. Do not invent dashboard rows.

Update progress immediately after material changes, including:

- task created;
- new week of work started;
- important result produced;
- status changed;
- user input or permissions required;
- task paused or resumed;
- user declared the stage complete;
- archive completed.

### 9. Generate Group-Meeting Material

When the user asks for a weekly summary, document, or presentation:

1. read the current weekly README;
2. read current-week task records under `tasks/*/[label]任务记录.md`;
3. inspect relevant task-local deliverables and cross-task weekly deliverables;
4. read earlier records only when needed for context;
5. emphasize results, methods, problems, and next steps;
6. exclude unnecessary temporary details;
7. save the output under the current week's `deliverables/`;
8. update all indexes.

Suggested names:

```text
[weekly]YYYY-Www组会总结.docx
[weekly]YYYY-Www组会汇报.pptx
[label]YYYY-Www组会汇报.pptx
```

### 10. Complete and Archive a Stage Task

Only archive after the user explicitly declares the stage task complete.

Procedure:

1. set status to `已完成`;
2. record the completion date;
3. create:

```text
completed-projects/[label]阶段任务名称/
├─ README.md
├─ source-index.md
└─ deliverables/
```

4. copy relevant formal deliverables into the archive;
5. keep all originals in `weekly/`;
6. do not copy unnecessary temporary files;
7. complete the stage summary using `templates/project-summary.md`;
8. complete the source index using `templates/source-index.md`;
9. move the row in `TASKS.md` to "已完成的任务";
10. set final status to `已归档`.

## Task Status Values

Use only:

```text
未开始
进行中
等待用户输入
等待权限
暂停
待确认
已完成
已归档
```

Do not mark a task complete or fill a completion date without explicit user confirmation.

## Dashboard Rules

A stage task appears once in `TASKS.md`, not once per week.

Preserve:

- original start date;
- all actual execution weeks;
- latest update date;
- current status;
- current task record or final archive path.

Execution weeks use Chinese separators:

```text
2026-W29、2026-W30、2026-W32
```

Do not add weeks in which no work occurred.

`[非任务]` maintenance sessions never appear in `TASKS.md`.

## Error Handling

Stop and inform the user when:

- the label is missing;
- a target file is ambiguous;
- external path access is required;
- extra permissions, internet access, or installation is required;
- a destructive or irreversible change may occur;
- a file cannot be safely modified;
- `TASKS.md` cannot be updated.

For `[非任务]`, do not stop for a missing stage-task label; continue under the non-task maintenance rules.

Never claim the dashboard or files were updated when writing failed.

## Completion Report

At the end of each work session report:

```markdown
## 已完成

- 任务标签：
- 完成内容：
- 工作记录：
- 正式成果：
- 临时文件：
- 更新的索引：
- 当前状态：
- 是否需要用户确认：
- 下一步：
```

## Common Mistakes

- Inventing a label when the user forgot one.
- Treating `[非任务]` as a normal stage-task label.
- Creating deliverables without a task record.
- Mixing temporary files and formal deliverables.
- Placing different tasks' temporary files or deliverables in the same weekly folder.
- Creating duplicate rows for the same stage task.
- Changing the original start date on resumed work.
- Adding weeks where no work occurred.
- Archiving by moving instead of copying.
- Marking a task complete without explicit confirmation.
- Accessing files outside the root without permission.
