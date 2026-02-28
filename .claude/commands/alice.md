
Explain the following concept as if to a 5-year-old, using only the story of Bob, Alice, and Eve.

Topic (optional): $ARGUMENTS

## Context detection

If $ARGUMENTS is empty:
- Look at the last 3-5 messages in the current conversation
- Identify the concept, error, or question being discussed
- Use that as the topic — do not ask the user to repeat it
- Start your response with: "Chasing down the topic of [topic]..."

If $ARGUMENTS is provided:
- Use it directly as the topic

Rules:

- Bob and Alice want to share a secret (a message, a key, a handshake — whatever fits)
- Eve is always watching, listening, or trying to sneak in
- No jargon. If a technical term is unavoidable, explain it through what Bob, Alice, or Eve *experiences*
- Be brief
- Use one concrete analogy (a locked box, a secret language, a special handshake, etc.)
- End with one sentence that connects the story back to the real concept

Concept to explain:
$ARGUMENTS
