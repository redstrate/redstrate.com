---
title: "Steam Offline Achievements and Why They Sometimes Don't work"
date: 2022-10-05
draft: true
tags:
- Steam
---

If you've been paying attention these last couple of months, the Steam Deck is now in people's hands
and people are starting to discover how bad Steam Offline mode is. Thankfully Valve is improving the situation
in every update but there is one thing they cant fix: Why do some games require you to be online for achievements
and some don't?

## What works

In the best case, the game in question is actually using the Steam API properly, as Steamworks
already keeps a local cache of achievements and stats that will eventually get uploaded back to Steam
once you enter Online Mode again. This is fine, and it's been working this way for years.

## What doesn't work

However, in some cases, it doesn't always end up this way. Let's take for example, Nier Automata
as this is what tipped me off to this issue. I sometimes take my Steam Deck willingly offline because
I share my library with my girlfriend, but remember that this will happen sooner or later on a handheld. I haven't
gotten too far on the PC version of Automata, so I'm still in the beginning part of the game. I enter the Amusement Park and 
beat the boss there, and much to my surprise.... nothing? Now I normally don't get too worked up about achievements, but it's
kind of insane that I earned one, and now I have no easy way to get it back without cheating or restarting the game again. Eugh. Let's figure out what's going on.

## Theory

I have a sneaking suspicion what's going on here, but until I take apart the Nier binary I have no idea yet.

I suspect that before the game records the achievement with Steamworks, it checks whether it's online,
whether through it's through its own game servers (since automata has online services) or through Steamworks. Right now
I'm going to assume it's checking the Steamworks API, so we'll be looking for those API calls. Once it detects
you're not online, it decides to not even record Steam achievements. I have no idea why developers might do this,
since _Steamworks_ already maintains a local cache. This is also made clear in the Steamworks documentation:

INSERT IMAGE

## Reverse Engineering

First, we need to break the Steam DRM. The DRM is quite simple, and it's been broken before. Much more knowledgeable people
have written up about this format, but in short the actual executable is wrapped within a Steam stub that checks whether it's launched through Steam and then decrypts the binary.

I tried Steamless to decrypt the game, but that didn't work, so I opted to dump the binary when the game was running. Then,
I threw the executable into Ghidra:

