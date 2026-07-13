# Weekly Group Meeting Skill

## 安装

将本压缩包中的全部内容解压到你的组会工作根目录。

关键文件应位于：

```text
AGENTS.md
TASKS.md
.agents/skills/managing-weekly-group-meetings/SKILL.md
```

如果你的 Codex 环境使用不同的项目级 Skill 目录，请保持
`managing-weekly-group-meetings/` 内部结构不变，并将该目录移动到环境要求的位置。

## 初始化当前周

在根目录运行：

```bash
python .agents/skills/managing-weekly-group-meetings/scripts/init_week.py
```

初始化指定周：

```bash
python .agents/skills/managing-weekly-group-meetings/scripts/init_week.py --week 2026-W29
```

脚本只创建缺失内容，不覆盖已有文件。

## 测试

```bash
python -m unittest discover .agents/skills/managing-weekly-group-meetings/tests -v
```

## 推荐首次指令

```text
请读取根目录 AGENTS.md 和 managing-weekly-group-meetings Skill，
初始化本周工作目录。只创建缺失的目录和文件，不要移动或修改已有文件。
```
