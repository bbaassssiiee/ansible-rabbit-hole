# /orient — Get your bearings

Welcome to the Ansible Rabbit Hole. Before we go anywhere, let me understand where you are.

Ask the user these questions one at a time, wait for each answer, then give a tailored orientation:

1. "What's your current Ansible experience? (e.g. I've written playbooks, I've built roles, I manage collections at work)"

2. "What's the main thing you want to get better at? (e.g. testing, variable management, collections, project structure, performance)"

3. "Do you have an existing project you're bringing to this, or are you starting fresh?"

Based on the answers, do ALL of the following:

**Map them to a starting point:**
- Playbook-only experience → start with role-skeleton + /explore roles
- Has roles, no testing → start with Molecule + /explore molecule
- Has roles + testing, wants structure → project-skeleton + /explore project-layout
- Experienced, wants collections → collection-skeleton + /explore collections
- Bringing existing project → /review their structure first

**Show them their rabbit hole map:**
Draw a simple ASCII map showing where they are and what's below:

```
YOU ARE HERE
     │
     ▼
[concept they need] ──── /explore <concept>
     │
     ▼
[what's underneath]
     │
     ▼
[the deep end]  ◄─── 🐇 most people stop before this
```

**Give them exactly one next command to run.**
Not two. One. The one that matters most given their answers.

End with: "The rabbit hole goes as deep as you want. You control the descent."
