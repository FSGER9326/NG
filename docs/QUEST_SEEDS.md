# NG Quest Seed Bank

Reusable quest seeds for filling roads, villages, shrines, farms, ruins, and faction edges in NG's dark low-fantasy borderland.

These are intentionally text-first and data-friendly. Convert them later into JSON quest files, dialogue files, hotspot text, and scenario tests using quest stages, flags, faction reputation, optional skill checks, and optional combat encounters.

## Authoring pattern

A small NG quest should usually have:

1. A human problem before a monster problem.
2. Two plausible explanations before the truth.
3. One reveal that changes the moral shape of the task.
4. A resolution trackable by flags, quest stages, and reputation.
5. A journal line that remembers what the player actually did.

Suggested stage pattern: `not_started -> accepted -> found_clue -> chose_side -> resolved`.

---

## 1. An Honest Grave

**ID:** `honest_grave`  
**Use:** cemetery, road shrine, battlefield ditch, village edge  
**Theme:** dignity is expensive in a starving place.

A gravedigger asks the party to recover a corpse stolen from the pauper pit before dawn. He claims wolves dragged it out. The tracks are human.

**Description:** The dead are meant to be cheap in Wolfpine: a rag shroud, a muttered name, and a spade of wet earth. But someone has stolen a body from the pauper pit, and the gravedigger is afraid to say whose.

**Stages:** `not_started`, `accepted`, `found_tracks`, `learned_identity`, `returned_body`, `hid_truth`, `exposed_truth`

**Branches:** Return the body quietly; sell the identity to someone who needs leverage; burn the corpse if it carries disease or old-faith marks.

**Flags:** `honest_grave_tracks_found`, `honest_grave_identity_known`, `honest_grave_truth_hidden`, `honest_grave_truth_exposed`

**Lines:**

- Gravedigger: "A poor man is owed little here. But he is owed the hole I dug him."
- Corpse thief: "You call it theft. I call it keeping my brother from a ditch full of strangers."
- Journal: "The body was returned to the earth, but not every name returned with it."

---

## 2. The Last Warm Hearth

**ID:** `last_warm_hearth`  
**Use:** inn, refugee cellar, winter road, common house  
**Theme:** survival makes thieves of decent people.

The innkeeper hires the party to catch whoever is stealing firewood from the common store. The thief is heating a hidden cellar full of sick refugees.

**Description:** The common woodpile is shrinking faster than winter can explain. The innkeeper says theft. The guard says rationing. At night, smoke rises from a room that has no door on the village map.

**Stages:** `not_started`, `accepted`, `found_hidden_room`, `reported_refugees`, `protected_refugees`, `resolved`

**Branches:** Report the refugees; pay for the wood; pressure the innkeeper to share heat; evict the refugees and preserve the ration store.

**Flags:** `last_warm_hearth_refugees_found`, `last_warm_hearth_refugees_protected`, `last_warm_hearth_refugees_reported`

**Lines:**

- Innkeeper: "A hearth is mercy until everyone wants a place beside it. Then it is arithmetic."
- Refugee mother: "We stole sticks, not silver. Count that against the children if you must."
- Journal: "The woodpile stopped shrinking. Whether Wolfpine grew warmer depends on whom the party left in the cold."

---

## 3. Black Bread Tithe

**ID:** `black_bread_tithe`  
**Use:** mill, granary, guard store, village square  
**Theme:** law and hunger cannot both be obeyed.

Villagers accuse the miller of cutting ash and husks into the bread. The miller claims the guard has been taking extra tithe for emergency stores.

**Description:** Wolfpine's bread has turned black, gritty, and thin. The villagers spit ash from their teeth and blame the miller. The miller's ledgers say the flour went elsewhere, stamped and sealed by the guard.

**Stages:** `not_started`, `accepted`, `checked_mill`, `found_guard_tithe`, `exposed_miller`, `exposed_guard`, `brokered_ration`

**Branches:** Side with the guard; side with the miller; expose both; quietly alter the ledgers to keep the peace.

**Flags:** `black_bread_mill_checked`, `black_bread_guard_tithe_known`, `black_bread_ration_brokered`

**Lines:**

- Miller: "I can grind wheat or I can grind lies. Lately the village buys both."
- Quartermaster: "A hungry guard drops his spear. A dropped spear feeds bandits. Tell me where the grain should go."
- Journal: "The bread changed hands before it changed color. The party decided whose hunger counted first."

---

## 4. The Bell That Rings Twice

**ID:** `bell_rings_twice`  
**Use:** watchtower, chapel bell, gatehouse, night event  
**Theme:** warning and conspiracy sound the same in the dark.

The village warning bell has rung twice on false alarms. A third false alarm will empty the guardhouse long enough for a theft, escape, or attack.

**Description:** Once means danger. Twice means panic. The old bell has rung twice this week with nothing beyond the wall but rain and pines. The guards laugh too loudly when asked who had the rope.

**Stages:** `not_started`, `accepted`, `checked_bell_rope`, `caught_signal`, `stopped_theft`, `used_signal`

**Branches:** Stop the signal; follow it to a smuggling route; replace the signal to ambush the conspirators; frame another faction.

**Flags:** `bell_rope_inspected`, `bell_signal_identified`, `bell_conspiracy_stopped`, `bell_conspiracy_used`

**Lines:**

- Bell keeper: "A bell does not lie. It only repeats the hand that pulls it."
- Young guard: "When it rings, everyone looks outward. That is the only part of the plan I understood."
- Journal: "The bell fell silent, but the village did not become safer simply because it stopped hearing danger."

---

## 5. The Dog That Knew the Road

**ID:** `dog_knew_road`  
**Use:** road, farmstead, caravan aftermath, missing person  
**Theme:** loyalty can outlive the person it served.

A wounded dog appears at the village gate each dawn, then flees when followed. It leads the party to a survivor, corpse, hidden cache, or ambush site.

**Description:** Every dawn, a mud-caked dog limps to the south gate and whines until someone throws a stone. Then it turns back toward the pines, looking over its shoulder as if men are wiser than dogs.

**Stages:** `not_started`, `accepted`, `found_blood_marker`, `found_master`, `saved_survivor`, `buried_master`, `resolved`

**Branches:** Save a survivor; find and bury a corpse; keep the dog as camp flavor; abandon or sell the dog for a harsh reputation consequence.

**Flags:** `dog_followed`, `dog_master_found`, `dog_survivor_saved`, `dog_vigil_ended`

**Lines:**

- Gate child: "He does not bark at us anymore. Just looks disappointed."
- Dying survivor: "The fool beast came back? I told him to run. He never learned any command worth knowing."
- Journal: "The dog stopped returning to the gate. For once, that was a mercy."

---

## 6. Soot on the Prayer Cloth

**ID:** `soot_prayer_cloth`  
**Use:** old shrine, chapel dispute, village grove, roadside marker  
**Theme:** faith is shelter until someone needs kindling.

Someone burned old-faith prayer cloths tied near a roadside shrine. The priest blames heretics. The old-faith keeper blames the priest. Beneath the ash is a signal mark.

**Description:** The shrine trees wear black knots where red prayer cloths used to hang. The priest calls it purification. The old keeper calls it desecration. Beneath the ash, one cloth did not burn.

**Stages:** `not_started`, `accepted`, `found_unburned_cloth`, `questioned_priest`, `questioned_keeper`, `revealed_mark`, `resolved`

**Branches:** Blame the priest; blame the keeper; reveal the signal system; preserve the signal secretly for a faction path.

**Flags:** `soot_cloth_found`, `soot_signal_revealed`, `soot_priest_blamed`, `soot_keeper_blamed`

**Lines:**

- Old keeper: "They think cloth is what we tied there. It was grief. It was thanks. It was names."
- Priest: "I burned nothing holy. That is the difference between us."
- Journal: "The shrine kept its branches. What hung from them afterward depended on whose truth survived the fire."

---

## 7. The Widow's Toll

**ID:** `widows_toll`  
**Use:** bridge, ford, broken road, roadside camp  
**Theme:** grief can become law if no one challenges it.

A widow demands tolls at a broken bridge where her husband died repairing it. Travelers call her mad. The toll money pays armed men to keep a worse predator away.

**Description:** The bridge is half rope, half prayer, and entirely hers. The widow takes coin from every cart that crosses. Those who refuse find the far bank watched by men with bows.

**Stages:** `not_started`, `accepted`, `learned_husband_story`, `found_hired_bows`, `broke_toll`, `legitimized_toll`, `redirected_toll`

**Branches:** End the toll and lose protection; keep the toll and anger travelers; replace hired bows with guard patrols; repair the bridge at cost.

**Flags:** `widows_toll_husband_known`, `widows_toll_bows_found`, `widows_toll_ended`, `widows_toll_reformed`

**Lines:**

- Widow: "The bridge took my husband. Until it pays me back, everyone pays me first."
- Hired bowman: "Laugh if you like. Her coin spends. Her grief does not ask twice."
- Journal: "The bridge still crossed the water. The question was whether it also crossed the line between justice and grief."

---

## 8. Spoiled Medicine

**ID:** `spoiled_medicine`  
**Use:** healer, caravan crate, plague house, apothecary  
**Theme:** mercy without competence still kills.

Medicine from a delayed shipment is making patients worse. The healer begs the party to prove sabotage before the village turns on her.

**Description:** The medicine arrived late, warm, and sour beneath the cork. The healer swears her measures are clean. The sick swear they were better before she helped them.

**Stages:** `not_started`, `accepted`, `checked_crates`, `found_storage_fault`, `found_sabotage`, `saved_patients`, `exposed_culprit`

**Branches:** Blame the healer; blame the caravan handler; reveal unavoidable spoilage; use an old-faith remedy and risk social backlash.

**Flags:** `spoiled_medicine_crates_checked`, `spoiled_medicine_sabotage_known`, `spoiled_medicine_patients_saved`

**Lines:**

- Healer: "When I fail, they call it murder. When hunger fails them, they call it winter."
- Patient: "Do not bring me another bottle unless it remembers what mercy tastes like."
- Journal: "The medicine did not become less bitter when the party learned why it failed."

---

## 9. A Knife in the Ledger

**ID:** `knife_in_ledger`  
**Use:** counting house, guard office, merchant stall, smuggler route  
**Theme:** paperwork can kill from a distance.

A clerk asks the party to recover a stolen ledger. The ledger contains debt records, bribe lists, false grain weights, or names of informers.

**Description:** The clerk's hands shake too much for a man who lost only paper. His ledger is gone, and with it every quiet arrangement that keeps Wolfpine pretending to be lawful.

**Stages:** `not_started`, `accepted`, `found_empty_lockbox`, `found_ledger`, `read_ledger`, `returned_ledger`, `sold_ledger`, `burned_ledger`

**Branches:** Return it sealed; read and blackmail; give it to the guard; burn it to free debtors and destroy evidence.

**Flags:** `knife_ledger_found`, `knife_ledger_read`, `knife_ledger_returned`, `knife_ledger_burned`

**Lines:**

- Clerk: "Ink looks harmless until you notice whose blood it saves for later."
- Debtor: "If my name is in that book, then I am still chained to a man too weak to hold a rope."
- Journal: "The ledger changed hands, and so did the power to decide which debts were real."

---

## 10. Ashes for the Orchard

**ID:** `ashes_for_orchard`  
**Use:** farm, old orchard, blight, sacred grove  
**Theme:** saving the harvest may mean killing what people worship.

An orchard is blighted. The farmer wants the trees burned before the rot spreads. The old-faith keeper says the oldest tree is sacred and must not be cut.

**Description:** The orchard smells sweet in the wrong way. Black syrup leaks from the oldest trunks, and the apples fall soft enough to burst in the hand. The farmer has stacked kindling. The keeper has brought prayer cords.

**Stages:** `not_started`, `accepted`, `found_blight_source`, `consulted_keeper`, `burned_orchard`, `saved_sacred_tree`, `contained_blight`

**Branches:** Burn all trees; save the sacred tree; cut only infected limbs; discover poison or a corpse under the roots.

**Flags:** `orchard_blight_source_found`, `orchard_burned`, `orchard_sacred_tree_saved`, `orchard_blight_contained`

**Lines:**

- Farmer: "A holy tree feeds no child if every apple rots black."
- Old keeper: "Your hunger lasts a season. That root held this hill before your grandfather had a name."
- Journal: "The orchard was saved, burned, or spared. None of those words meant the same thing to everyone beneath it."

---

## 11. The Quiet Deserter

**ID:** `quiet_deserter`  
**Use:** barn, shrine, guard cell, bandit camp  
**Theme:** cowardice and conscience often wear the same face.

A deserter is hiding near the village. The guard wants him hanged. The bandits want him silenced. He claims he fled after seeing who really attacked a caravan, patrol, or hamlet.

**Description:** The deserter has slept three nights under wet hay, breathing through his sleeve when patrols pass. He admits he ran. He will not say from whom until someone promises he will live long enough to finish the sentence.

**Stages:** `not_started`, `accepted`, `found_deserter`, `heard_testimony`, `turned_in_deserter`, `hid_deserter`, `used_testimony`

**Branches:** Turn him in; hide him; force public testimony; sell him to people who want the truth buried.

**Flags:** `quiet_deserter_found`, `quiet_deserter_testimony_heard`, `quiet_deserter_hidden`, `quiet_deserter_turned_in`

**Lines:**

- Deserter: "Call me coward. I have been called worse by men who stayed and did what they were told."
- Guard: "If every frightened man gets a story, no rope in Wolfpine will ever be long enough."
- Journal: "The deserter's life became less important than the truth he carried, which is how small people are often used by large events."

---

## 12. Bloodless Hunt

**ID:** `bloodless_hunt`  
**Use:** sheepfold, forest edge, hunter camp, village rumor  
**Theme:** a village prefers a beast it can kill.

Sheep vanish from locked pens without blood. Hunters blame a clever wolf. The culprit is a starving family, a trained dog, a guard racket, or an old tunnel.

**Description:** Three sheep vanished behind a latched gate, and not one drop of blood marked the straw. The hunters swear it was a wolf. The shepherd swears wolves have not learned knots.

**Stages:** `not_started`, `accepted`, `checked_pen`, `followed_tracks`, `found_culprit`, `killed_beast`, `spared_culprit`, `resolved`

**Branches:** Kill a wolf to satisfy the village; expose human thieves; feed the starving culprits secretly; discover a tunnel to a future area.

**Flags:** `bloodless_pen_checked`, `bloodless_true_culprit_found`, `bloodless_false_wolf_killed`, `bloodless_culprit_spared`

**Lines:**

- Shepherd: "A wolf leaves blood. A neighbor leaves excuses."
- Hunter: "People pay faster when you bring back teeth. They ask fewer questions too."
- Journal: "The sheep stopped vanishing. Whether the village learned why was another matter."

---

## Implementation notes

Good first candidates for JSON conversion:

1. `dog_knew_road`: mostly hotspot/dialogue flags, emotionally strong, low system cost.
2. `black_bread_tithe`: uses faction reputation and dialogue branches, good village politics test.
3. `soot_prayer_cloth`: extends old-faith content and shrine interactions.
4. `bloodless_hunt`: can start non-combat and later gain an encounter or tunnel area.

When converting a seed, add one quest JSON file, one or two NPC dialogue files, area hotspot entries, and a scenario covering at least one completion path.
