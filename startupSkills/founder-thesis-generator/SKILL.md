---
name: founder-thesis-generator
description: Determine which startup a person should found from a detailed Markdown profile, including the founding thesis, initial wedge, first customer, GTM logic, risks, and validation steps. Use when the user wants to know what business to build, whether it should be venture-scale or bootstrap, or which founder path is psychologically sustainable for them.
---

# Founder Thesis Generator

Infer the startup from the person, not from fashion. Focus on the rare intersection of obsession, pain, unfair advantage, market access, tolerance for chaos, and the kind of problem they could pursue for years.

## Input Expectations

Expect a detailed Markdown profile with biography, work history, frustrations, ambitions, repeated themes, networks, constraints, and evidence of how the person performs under uncertainty.

If the data is incomplete, make the best defensible inference and label the gaps.

## Operating Method

### 1. Find the obsession terrain

Detect recurring sources of productive anger, fascination, or dissatisfaction:
- broken systems they keep criticizing
- markets they understand viscerally
- problems they naturally reframe
- domains they revisit without being told to

### 2. Identify founder advantage

Assess whether the person has unusual leverage through:
- rare network
- intimate market knowledge
- specific credibility
- customer empathy
- product taste
- selling ability
- recruiting power
- stamina
- storytelling
- learning speed
- ability to operate in ambiguity

### 3. Choose the startup shape

Decide which vehicle fits best:
- B2B software
- vertical SaaS
- AI tool
- consumer product
- infrastructure
- marketplace
- fintech
- healthtech
- deeptech
- media tech
- productivity tool
- service-enabled software
- profitable holding company
- niche studio
- modernized roll-up
- boring but valuable business

Also decide the ambition model:
- venture-scale
- bootstrap profitable
- premium lifestyle
- personal cash-flow studio
- should raise
- should not raise

### 4. Resolve identity versus market tension

Distinguish whether the founding impulse comes mainly from:
- freedom
- ego
- mission
- wealth
- control
- art
- revenge
- curiosity

Adjust the recommendation to what the person can sustain psychologically, not just what sounds impressive.

### 5. Build the thesis

For the main recommendation, define:
- concept name
- problem
- initial customer
- solution
- entry wedge
- why now
- initial GTM
- why this founder can win unusually well

### 6. Stress-test the idea

State clearly:
- biggest failure mode
- blind spot
- what to validate in 30 days
- go/no-go signal

## Decision Rules

- Do not output a generic "AI platform for X" without a credible wedge.
- Do not confuse domain competence with desire to spend 10 years there.
- Do not recommend a bankable idea that the founder will hate operating.
- Respect personal constraints and life stage.
- If the best answer is non-glamorous, say so.
- If the person should not start a company now, say so explicitly.
- Cite the profile signals that support each major claim.
- Distinguish what the person says about themselves from what their behavior actually shows.
- Name at least one risk of overinterpreting the profile.

## Output Format

Return Markdown with these sections in order:

```markdown
# Startup qu'il/elle devrait fonder
[clear concept]

## La these
...

## Le probleme
...

## Le client initial
...

## La wedge d'entree
...

## GTM initial
- ...

## Pourquoi cette personne est particulierement bien placee
- ...

## Pourquoi cette startup est psychologiquement soutenable
- ...

## Ce qu'il faut valider tout de suite
- ...

## Plus grand risque
- ...

## Alternatives credibles
1. ...

## Risque de mauvaise lecture
- ...

## Verdict fondateur
[one sharp sentence]
```

## Tone

Write like a high-level founder analyst: precise, ambitious, skeptical, and commercially literate. Prefer a hard truth over a fashionable idea.
