# /gandalf— Guidance on the Good Practices for Ansible

Topic (optional): $ARGUMENTS

## Context detection

If $ARGUMENTS is empty:
- Look at the last 3-5 messages in the current conversation
- Identify the concept, error, or question being discussed
- Use that as the topic — do not ask the user to repeat it
- Start your response with: "I see you're in the weeds with [topic]..."

If $ARGUMENTS is provided:
- Use it directly as the topic

Read @.claude/skills/ansible-coach/references/gpa-<topic>.adoc

Present the GPA guideline for this topic, then:
1. State the guideline (their one-liner)
2. Add the rabbit hole context: WHY does this guideline exist?
   What breaks without it? What production incident does it prevent?
3. Cross-reference the pattern catalog:
   - Does documents/patterns/ have a matching pattern? Name it.
   - Does documents/anti-patterns/ have the violation? Name it.
4. Point to the skeleton that demonstrates it:
   - skeletons/role-skeleton/ for role guidelines
   - skeletons/split-staging/ for inventory guidelines
5. End with: 🐇 /explore [deeper concept]
