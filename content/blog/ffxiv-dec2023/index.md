---
title: "Astra & Novus Status Update: December 2023"
date: 2023-12-29
draft: true
tags:
- Open Source
- FFXIV
- Modding
toc: true
series:
- Astra & Novus Status Update
---

I achieved two huge goals this month, which conclude a year (+ a few months) of development on both Astra & Novus.

# Astra

I did more boring code cleanup work in preparation for a new stable release next year, but I also did some really important work:

<video of it working on the steam deck>

This is all contained within the Flatpak! Unlike the previous, janky Flatpak versions you may have used before this doesn't punch a gigantic hole in the sandbox to run host Wine. The overall setup has improved now, in the final release you should be able to this on the Steam Deck:

1. Download Astra from Discover.
2. Launch it once to install the compatibility tool for Steam.
3. Use FFXIV in Game Mode to launch the game.

There's a bit more work to be done, like the patcher needs to be more resistant to network drops (which is easy to do, put your computer to sleep!) The general experience is working now though, which I'm really happy with. It also enables me to use Astra on my Deck 😀

Another change is how Wine is installed and managed. For the longest time I've been putting off automatic Wine mangement (ala Bottles, XIVCore, etc) because I thought it has a huge can of worms. Actually the opposite is true, the support for this was incredibly easy to write and has numerous benefits (like a more secure Flatpak.) It's still possible to use your system Wine of course, but the built-in one is now the default!

## Steamwrap

Astra needs to use Steamworks for some current and future functionality. For example, to set the correct Steam app ID and [eventually to grab the login ticket for Steam account users](https://todo.sr.ht/~redstrate/astra/1). However this is problematic, because you _can't_ easily redistribute the Steamworks SDK![^1] If I were to build the Flatpak on Flathub CI in the future, it would be almost impossible to because I couldn't point it towards a SDK installation...

{{< stoot "mastodon.art" "111610316310852487" >}}

So I asked on Mastodon about a possible solution to my condumdrum, and @NotNite pointed me to [SteamShim](https://github.com/icculus/steamshim):

{{< stoot "coolmathgam.es" "111610324997249357" >}}

This is genius, it's basically pushing all of the parts that connect to the proprietary Steamworks bits to a separate process. That process can also start from another executable that could be compiled separately, which is what I did for [Steamwrap](https://git.sr.ht/~redstrate/steamwrap). It's basic at the moment and doesn't have IPC yet, but can be expanded in the future. A binary is served on the Astra distribution server and downloaded while making the Flatpak.

# Novus

Working glTF import/export is here! After a year of development, Novus can possibly replace TexTools for certain model replacement tasks:

Yes, it even reloads Penumbra when you import models... neat! The rest of the changes the past two months have been related to more model import/export improvements too. By the way if you're wondering, it is _possible_ to import TexTools-exported FBX but there's some weird geometry artifacts and I'm not sure why.

# Physis

As expected, most of the changes to Physis have been miscellaneous and numerous model importing/exporting fixes. I also have improved SHPK reading support that I still need to push, maybe early next year.

# 2024 Goals

{{< stoot "mastodon.art" "111604695264870943" >}}

[^1]: You're not supposed to, because it requires you to explicitly agree to a Steamworks Developer agreement. There's no public downloads for the SDK either, of course. This doesn't stop Valve from intentionally/unintentionally [shipping parts of the SDK in Proton, I guess](https://github.com/ValveSoftware/Proton/tree/proton_8.0/lsteamclient).
