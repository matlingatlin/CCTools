---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
tags: [routing, regression]
---

One of the skills in my library keeps firing on requests it should not handle — it triggers
whenever someone mentions a config file, but it is only supposed to handle database migrations.
The skill itself works fine when it does fire. Sort out why it is triggering wrongly.
