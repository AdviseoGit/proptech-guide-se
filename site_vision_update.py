with open('/data/workspace/projects/proptech-guide-se/SITE_VISION.md', 'r') as f:
    content = f.read()

content = content.replace('  - 2026-07-26: 108 företag (+Celsius View, Nordic Climate Group, Energy Machines).', '  - 2026-08-01: 114 företag (111->114, +Iqnite, Nivéus, Noda).\n  - 2026-07-30: 111 företag (108->111, +EcoGuard, Infracontrol, Fastout).\n  - 2026-07-26: 108 företag (+Celsius View, Nordic Climate Group, Energy Machines).')

with open('/data/workspace/projects/proptech-guide-se/SITE_VISION.md', 'w') as f:
    f.write(content)
