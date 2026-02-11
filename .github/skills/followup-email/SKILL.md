---
name: followup-email
description: Generates post-engagement follow-up emails in HTML (and optionally plain text) from closeout summaries, transcripts, and engagement context. Use when drafting follow-up emails, thank-you emails, or when user says "follow-up email", "thank you email", "send recap", or "write follow-up".
---

# Follow-Up Email

Generates conversational, human-sounding follow-up emails for completed engagements.

## Quick Start

**Basic:**
```
"write follow-up email for DOS CfA"
"generate follow-up for Keller engagement"
```

**With context:**
```
"follow-up email for [Customer] - session was [date]"
"draft thank-you email for [Customer], include [specific detail]"
```

## When to Use

Use this skill when:
- An engagement session has been completed and a follow-up email is needed
- A closeout summary already exists (preferred) or transcript is available
- The user wants to send a recap with next steps to the customer

## What It Does

1. **Reads engagement context** from closeout summary, metadata, agenda, and README
2. **Always queries WorkIQ** for the meeting transcript, even if a closeout exists (transcripts surface specific moments, reactions, and detail that summaries compress away)
3. **Assesses audience and tone** based on attendee seniority and session type
4. **Generates HTML email** following tone and formatting guidelines
5. **Saves to engagement folder** as followup_email_[date].html

## Workflow Checklist

```
- [ ] Identify customer and engagement date
- [ ] Read closeout summary if available (for distilled outcomes)
- [ ] Query WorkIQ for meeting transcript (ALWAYS, even if closeout exists)
- [ ] Read engagement_metadata.json for team/stakeholder names and seniority
- [ ] Read agenda_data.json or README for session structure
- [ ] Assess audience tier (see Audience-Aware Tone section)
- [ ] Draft email following writing guidelines, calibrated to audience
- [ ] Save HTML to engagement folder
- [ ] Display for review
```

## Source Priority

Pull content from all available sources. More context produces better emails.

1. **closeout_summary_[date].md** - distilled outcomes, decisions, and next steps
2. **WorkIQ meeting transcript** - ALWAYS query this, even when a closeout exists. Transcripts surface specific moments, customer reactions, quotes, and nuance that summaries lose. Use these details to make the email feel grounded in the actual conversation.
3. **engagement_metadata.json** - names, roles, seniority, products, partners
4. **agenda_data.json** - session structure and topics covered
5. **README.md / qualification_notes.md** - strategic context, previous engagements

## Writing Guidelines

### Voice and Tone

Write like a real person sending an email to colleagues they just spent a day working with. The email should sound like it was written in 10 minutes after the session, not generated from a template.

**Do:**
- Write in first person, conversational tone
- Reference specific moments, decisions, or discussions from the session
- Use short, direct sentences mixed with longer ones
- Let the content vary in structure from email to email
- Address people by first name
- Use contractions naturally (we're, isn't, don't, can't)
- Calibrate tone to the audience (see Audience-Aware Tone below)

**Don't:**
- Use em dashes (---, &mdash;, or the character itself). Use commas, periods, or restructure instead.
- Use en dashes in ranges. Use hyphens (2-6 weeks, not 2-6 weeks)
- Use arrow characters (use "to" instead)
- Use phrases that appear across every email (see Banned Phrases below)
- Start with "I hope this email finds you well" or similar
- Use "please don't hesitate to reach out"
- Use the formal engagement title in the subject line

### Audience-Aware Tone

Not every email should read the same way. Calibrate based on who was in the room and what the session looked like.

**Assess these signals from metadata, transcript, and agenda:**
- Were executive sponsors or senior leadership actively involved (not just on the invite)?
- Was the conversation strategic/visionary or hands-on/technical?
- Is this a first engagement or a continuation of an existing relationship?
- Is the customer evaluating Microsoft against competitors?
- Are there partner relationships (Deloitte, Accenture, etc.) where positioning matters?

**Tier 1: Practitioner/Technical audience**
- Most conversational. Direct, specific, minimal polish.
- Focus on what was built, decided, and what's blocking.
- Skip strategic framing unless the practitioners asked for it.
- Example opening: "Great session yesterday. We covered a lot of ground."

**Tier 2: Mixed audience (practitioners + some leadership)**
- Conversational but slightly more polished.
- Include strategic context alongside technical outcomes.
- Acknowledge the value of what was accomplished without overselling.
- Example opening: "Thank you for a great day at the Hub. The fact that your team came prepared with X really set the tone for the session."

**Tier 3: Executive/leadership-heavy audience**
- More polished and strategic. It's appropriate to highlight the significance of outcomes.
- Frame accomplishments in terms of business value, competitive positioning, and organizational impact.
- Genuine enthusiasm is fine here; the key is being specific about what earned it rather than using generic superlatives.
- Include strategic opportunities and broader positioning.
- Example opening: "Thank you for bringing the leadership team together for yesterday's session. The alignment your team showed on [specific strategic decision] positions [Customer] to move quickly on [outcome]."

**Tier 4: Executive briefing or C-suite**
- Professional, concise, high-signal.
- Lead with the strategic narrative and business impact.
- Keep technical detail minimal; link to deeper materials if needed.
- Extended signature block with title and contact info.
- CC the account team visibly.

### Banned Phrases

These phrases are overused across follow-up emails and signal templated content. Never use them regardless of audience tier:

- "outstanding day"
- "incredible session"
- "one of the most productive workshops we've delivered/hosted"
- "the depth of preparation your team brought"
- "speaks to [Customer]'s maturity in this space"
- "please don't hesitate to reach out"
- "your team's clear vision for leading"
- "Key Outcomes from Our Session"
- "Looking Ahead"
- "compelling, repeatable pattern"

**Tier-dependent guidance:**
- "Outstanding", "incredible", "exceptional" as qualifiers: avoid at Tier 1-2. At Tier 3-4, use only when it's genuinely warranted and paired with a specific reason.
- Strategic framing ("positions [Customer] to lead..."): skip at Tier 1. Fine at Tier 3-4 when grounded in something concrete from the session.

### Preferred Alternatives

Instead of formulaic section headers, vary them:
- "What we landed on:" / "Where we got to:" / "Key decisions:" / "What came out of the session:"
- "What's next:" / "Follow-on work:" / "Where this goes from here:"
- "Next Steps:" (this one is fine as-is for the table)

Instead of generic praise in the opening:
- Reference something specific the customer did: "The fact that your team came prepared with X really set the tone"
- Call out a specific moment: "The demo of your current workflow made it clear where the gaps are"
- Be direct: "Great session yesterday. We covered a lot of ground."

### Outcomes Format

List outcomes as plain statements, not "Category Name - Description" pairs:
- Bad: `Discovery & Current-State Mapping - Your team clearly articulated the TAS workflow`
- Good: `Current-state is well understood. The walkthrough of TAS processes gave us a clear picture of what's working and where the gaps are.`

Each outcome item should read like a standalone finding, not a label followed by elaboration.

## Email Structure

### Subject Line
Keep it simple and specific. Reference the session topic, not the formal engagement title.
- Good: "Yesterday's TAS / Dynamics Session - Thank You & Next Steps"
- Good: "AI Agent Workshop Recap and Next Steps"
- Bad: "DOS CfA Deloitte Dynamics Project Management and Customer Support Workshop - Thank You & Next Steps"

### Opening Paragraph
- Thank them (1 sentence, specific)
- Reference something concrete about the session (what they brought, what made it productive)
- State the key takeaway or where things stand (1 sentence)

### Outcomes Section (3-6 items)
- Numbered list with bold lead-in statements
- Each item is a plain-language finding, not a category label
- Include specific technologies, decisions, and details from the session
- Call out gaps honestly alongside strengths

### Next Steps Table
- HTML table with Action / Owner / Timeline columns
- Use real names for owners where known
- Timelines should be plain language ("Next 2 weeks", "2-6 weeks", "Near-term")
- Order by timeline (immediate first)

### Follow-On Engagements
- Brief section naming 1-3 logical next engagements
- Each gets one line explaining what it would accomplish
- No em dashes; use "to" to connect the engagement type to its purpose

### Closing
- 1-2 sentences about scheduling follow-up and who you'll coordinate with
- Simple "reach out anytime" instead of formal alternatives
- QR code placeholder for feedback survey
- Sign off: name + "Microsoft" (no title block unless multi-day/executive engagement)

## HTML Template

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Calibri, Arial, sans-serif; font-size: 11pt; line-height: 1.4; color: #333; max-width: 700px; }
        table { border-collapse: collapse; margin: 15px 0; }
        th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
        th { background-color: #f0f0f0; font-weight: bold; }
        strong { font-weight: bold; }
        .qr-placeholder { border: 2px dashed #999; padding: 40px; text-align: center; color: #666; margin: 15px 0; width: 150px; }
    </style>
</head>
<body>

<p><strong>Subject:</strong> [Specific, informal subject line]</p>

<p>Hi [First names],</p>

<p>[Opening: thank, reference something specific, state where things stand]</p>

<p><strong>[Outcomes header - vary this]:</strong></p>
<ol>
    <li><strong>[Finding as statement.]</strong> [Supporting detail from session.]</li>
    <li><strong>[Finding as statement.]</strong> [Supporting detail from session.]</li>
</ol>

<p><strong>Next Steps:</strong></p>
<table>
    <tr>
        <th>Action</th>
        <th>Owner</th>
        <th>Timeline</th>
    </tr>
    <tr>
        <td>[Action item]</td>
        <td>[Owner name(s)]</td>
        <td>[Timeline]</td>
    </tr>
</table>

<p><strong>[Follow-on header - vary this]:</strong></p>
<ul>
    <li><strong>[Engagement type]</strong> to [what it accomplishes]</li>
</ul>

<p>[Closing: scheduling coordination, "reach out anytime"]</p>

<p><strong>We'd love your feedback!</strong> Please take 2 minutes to share your thoughts on the session:</p>

<div class="qr-placeholder">[INSERT QR CODE]</div>

<p>Best regards,</p>

<p>Brendon Colburn<br>
Microsoft</p>

</body>
</html>
```

## Signature Variations

**Standard (single-day sessions):**
```html
<p>Brendon Colburn<br>
Microsoft</p>
```

**Extended (multi-day, executive, or first engagement with a new customer):**
```html
<p><strong>Brendon Colburn</strong><br>
Lead Technical Architect<br>
Microsoft Innovation Hub<br>
brendon.colburn@microsoft.com</p>
```

Include CC line when account team or additional Microsoft stakeholders should be visible:
```html
<p><em>CC: [Account team names]</em></p>
```

## Quality Checks

Before saving, verify:
- [ ] No em dashes or en dashes anywhere in the output
- [ ] No arrow characters (use "to" or commas)
- [ ] No banned phrases used
- [ ] Subject line is informal and specific (not the formal engagement title)
- [ ] Opening references something specific to this session
- [ ] Outcomes are statements, not "Label - Description" format
- [ ] Next steps table has real owner names where known
- [ ] Tone reads as conversational, not templated
- [ ] Contractions used naturally
- [ ] Each email would sound different from the last one if read side by side

## Files Created

```
[Customer]-[Date]/
└── followup_email_[date].html
```

## Related Skills

- **engagement-closeout**: Generates the closeout summary this skill draws from
- **agenda-builder**: Provides agenda structure for session recap
- **journey-promoter**: May follow if engagement leads to customer journey
