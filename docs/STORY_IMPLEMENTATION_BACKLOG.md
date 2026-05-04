# NG Story Implementation Backlog

This backlog converts `docs/STORY_BIBLE.md` into small text-first tasks for the first playable module.

## Immediate content goal

Turn Wolfpine Road, Old Shrine, Captain Renna, Brannoc, and the Missing Caravan quest from prototype beats into the first playable slice of the larger Road Peace mystery.

The first pass should remain small, JSON-driven, and scenario-testable.

## Design order

1. **Ordinary pressure:** missing food, lamp oil, tolls, wagon ruts, dead animals, village panic.
2. **Faction pressure:** Roadwardens, Ash Church, smugglers, rangers, village officials, bandits.
3. **Old-law clues:** Road Peace, corpse law, saint relics, mile-stones, impossible toll evidence.
4. **Companion consequence:** Brannoc reacts to waste, abandoned travelers, cruelty, and practical mercy.

## New or expanded flags

Suggested flags for early implementation:

```text
wolfpine.shrine_seen_blood
wolfpine.shrine_seen_toll_disc
wolfpine.shrine_seen_dead_mule
wolfpine.shrine_found_hidden_ledger_niche
wolfpine.caravan_manifest_erased_name
wolfpine.caravan_relic_known
wolfpine.food_returned_to_village
wolfpine.food_sold_or_diverted
wolfpine.survivor_spared
wolfpine.survivor_executed
wolfpine.survivor_public_trial_promised
wolfpine.renna_ledger_pressure_known
wolfpine.renna_trust_low
wolfpine.renna_trust_high
wolfpine.brannoc_guilt_hint_1
wolfpine.brannoc_disapproved_waste
wolfpine.brannoc_disapproved_cruelty
wolfpine.brannoc_respected_practical_mercy
road_peace.first_failure_seen
corpse_law.first_violation_seen
church.reliquary_attention_raised
blackfen.smuggler_route_hint_known
```

## Missing Caravan quest stages

Suggested expanded stages:

```text
not_started
accepted
found_wreck
found_shrine_clue
found_erased_manifest_name
found_survivor
learned_relic_cargo
reported_clue
chose_food_disposition
chose_survivor_disposition
completed_renna_order
completed_public_truth
completed_smuggler_disposition
completed_church_disposition
```

The exact stage count can be smaller in the first pass. Prefer fewer reliable stages plus flags over one brittle linear quest chain.

## Captain Renna dialogue tasks

Renna should remain useful, compromised, and believable.

Add branches for:

- food urgency: why the caravan matters beyond payment
- law pressure: what she can and cannot do without proof
- falsified ledgers: she has hidden losses to prevent panic and keep escorts funded
- caravan-guard player reaction: already started; expand into a practical professional exchange
- shrine clue report: toll disc, dead mule, fresh ruts, hidden ledger niche
- survivor disposition: execute quietly, public trial, roadwarden custody, let the party decide
- relic custody: Renna wants the box controlled but may not know what it is

Useful Renna line direction:

> I can hang a thief and sleep. I can hang a hungry father and still sleep, if the road stays open. What I cannot do is hang a story. Bring me proof with a neck attached.

## Brannoc companion tasks

Brannoc should become the first emotional test of the party's methods.

Add branches or future banters for:

- recognizing caravan discipline mistakes
- reacting badly if the player wastes food or burns useful goods
- reacting badly to theatrical cruelty
- approving practical mercy when it preserves life or information
- showing discomfort around abandoned passengers, locked wagons, or trapped survivors
- hinting that he once left people behind during a raid

First personal arc seed:

```text
brannoc_guilt_arc = hidden
brannoc_guilt_hint_1 = set after survivor/abandoned-traveler clue
brannoc_guilt_hint_2 = set after village witness recognizes him
brannoc_confession_available = set after enough trust or pressure
```

## Old Shrine content tasks

The Old Shrine should become the first durable mystery node.

Hotspot expansions:

- cracked saint-stone inspection
- dead mule inspection
- toll disc inspection
- fresh wagon ruts inspection
- hidden ledger niche inspection
- pine roots through carved law text inspection

Possible skill/tag checks:

- `perception`: notice ruts stop too cleanly
- `lore` or future `religion`: saint carving has legal wording, not prayer wording
- `survival` or ranger tag: mule was opened after death, not killed by wolves
- `background.caravan_guard`: caravan spacing was wrong before the ambush
- `class.scout`: tracks show two groups after the raid

First old-law clue:

> The toll disc is not beside the dead mule. It has been pressed into the eye socket with a thumb, as if someone paid passage for the carcass after it fell.

## Wolfpine Village pressure tasks

Add NPC or dialogue seeds for:

- hungry miller or baker demanding returned flour
- priest arguing the shrine evidence must be sealed
- reeve afraid of public panic and forged ledgers
- child informant selling caravan rumors for food
- smuggler contact offering medicine or transport at a criminal price
- grieving family whose missing relative may be the erased manifest name

Village should feel like a place where telling the truth can start a riot.

## Faction data tasks

When faction JSON is introduced, start with these IDs:

```text
roadwardens
grey_rangers
ash_church
blackfen_free_company
sainted_lance
baronial_houses
rat_crown
borrowed
```

Early reputation changes:

- returning food to village: `roadwardens +`, `wolfpine_village +`, possible `blackfen_free_company -`
- giving relic to church: `ash_church +`, possible `grey_rangers -`
- hiding relic: `ash_church -`, possible future companion reactions
- public trial: `wolfpine_village mixed`, `roadwardens mixed`, `ash_church situational`
- quiet execution: `roadwardens +`, Brannoc/paladin reactions depend on context

## Scenario tests to add

Add scenario files only after the data exists.

Suggested tests:

```text
tests/scenarios/wolfpine_shrine_toll_disc.json
tests/scenarios/wolfpine_food_returned_to_village.json
tests/scenarios/wolfpine_survivor_spared.json
tests/scenarios/wolfpine_survivor_executed.json
tests/scenarios/brannoc_reacts_to_cruelty.json
tests/scenarios/renna_relic_custody_branch.json
```

Each scenario should verify a small number of flags, quest stages, and visible/hidden dialogue choices.

## Writing constraints

- Keep each dialogue node short enough for iteration.
- Make each choice reveal character, change state, or gather useful information.
- Avoid lore dumps unless the player has earned a technical explanation through clue collection.
- Add one memorable concrete image per scene: a stamped toll disc, wet flour, a split mule, a child's dirty hand, a paladin washing blood, a ranger sewing a boot.
- Use violence and gore as evidence or consequence, not filler.

## First recommended implementation patch

1. Expand `missing_caravan` quest stages cautiously.
2. Add Old Shrine hotspot branches for toll disc, dead mule, and hidden ledger niche.
3. Add one Renna report branch for the toll disc.
4. Add one Brannoc reaction flag for needless cruelty or food waste.
5. Add one scenario test that proves the toll-disc clue sets `road_peace.first_failure_seen`.
