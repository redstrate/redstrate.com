---
title: "Astra & Novus Status Update: December 2023"
date: 2023-12-30
draft: false
tags:
- Open Source
- FFXIV
- Modding
toc: true
series:
- Astra & Novus Status Update
---

I achieved two huge goals this month, which conclude a year (and a few months) of development on both [Astra](https://xiv.zone/astra) & [Novus](https://xiv.zone/novus). This also includes a few things I did in November, but it wasn't much so it didn't deserve it's own post.

# Astra

I did more boring code cleanup work in preparation for a new stable release next year, and I also sat down and pumped out a proper Steam Deck version:

{{< tube "https://tube.ryne.moe/videos/embed/1c13620c-2cfd-4d81-be4a-8429ed184c1b" >}}

This is all contained within a [Flatpak](https://flatpak.org)! Unlike the previous and janky versions you may have used before this doesn't punch a gigantic hole in the sandbox to run Wine. The overall setup has improved now, in the final release you should be able to this on the Steam Deck:

1. Download Astra from [Discover](https://apps.kde.org/discover/).
2. Open it once to install the compatibility tool for Steam.
3. Launch FFXIV in Game Mode to launch and patch the game.

There's a bit more work to be done, but the general experience is working now which I'm really happy about. For example, the patcher needs to be more resistant to network drops and users possibly putting it into sleep mode.

For the longest time I've been putting off automatic Wine mangement (ala [Bottles](https://usebottles.com/), [XIVLauncher.Core](https://github.com/goatcorp/XIVLauncher.Core), etc) because I thought it would be too much work. It turns out the opposite is true, it was incredibly easy to support and has numerous benefits such as the Flatpak being more secure. It's still possible to use your system Wine of course, but the built-in one is now the default!

## Steamwrap

Astra needs to use [Steamworks](https://partner.steamgames.com/doc/sdk) for some current and future functionality. For example, to set the correct Steam app ID[^1] and eventually to grab the login ticket for Steam account users. However this is problematic, because you _can't_ easily redistribute the Steamworks SDK[^2]! If I were to build the Flatpak on Flathub CI in the future, it would be almost impossible to because I couldn't point it towards a SDK installation...

{{< stoot "mastodon.art" "111610316310852487" >}}

So I asked on Mastodon about a possible solution to my condumdrum, and [@NotNite](https://notnite.com/) pointed me to [SteamShim](https://github.com/icculus/steamshim):

{{< stoot "coolmathgam.es" "111610324997249357" >}}

This is genius, it's basically pushing all of the parts that connect to the proprietary Steamworks bits to a separate process. That process can also start from another executable that could be compiled separately, which is what I did to create [Steamwrap](https://github.com/redstrate/steamwrap). It's basic at the moment and doesn't have IPC yet, but can be expanded in the future.

So my plan is to build binaries for Linux (ones that are compatible with the Steam Linux Runtime, of course) and upload them to the Astra distribution server. I want to do that during the build process, hopefully.

# Novus

Working glTF import/export is here! After a year of development, Novus can possibly replace [TexTools](https://github.com/TexTools/FFXIV_TexTools_UI) for certain model tasks, completely native on Linux:

{{< tube "https://tube.ryne.moe/videos/embed/d59aa248-7e29-4543-ae9c-797bd11c8628" >}}

Yes, it even reloads [Penumbra](https://github.com/xivdev/Penumbra) when you import models... neat! The import/export is almost done, save for a few very weird bugs when loading some vertex data. I've been hammering out fixes though, and I'm confident I can get it to a "good enough" state. Big thanks to [Xande](https://github.com/xivdev/Xande), [Lumina](https://github.com/NotAdam/Lumina), [xivModdingFramework](https://github.com/TexTools/xivModdingFramework) and the rest of the FFXIV modding community for their open source implementations I could reference!

If you're curious about the implementation, the source code for importing is [here](https://github.com/redstrate/novus/tree/main/parts/mdl/mdlimport.cpp) and exporting is [here](https://github.com/redstrate/novus/tree/main/parts/mdl/mdlexport.cpp). The model I/O is part of the [Physis source tree](https://github.com/redstrate/physis/tree/main/src/model.rs).

# 2024 Goals

As I said on Mastodon, now that model import/export is working I want to work towards my next "big goal" for 2024:

{{< stoot "mastodon.art" "111604695264870943" >}}

Of course I can avoid lots of pain by "recreating" the shaders, but that sounds too easy! I'm really excited to start digging into this, even if I don't complete it I still want to learn.

See you in the next status update!

[^1]: This might not be needed, but I'm still doing it anyway. I think it's because Game Mode already thinks the game we launched *is* FFXIV, regardless of what program is actually launched. This is a different situation compared to XIVLauncher.Core, which launches FFXIV separately.

[^2]: You're not supposed to, because it requires you to explicitly agree to a Steamworks Developer agreement. There's no public downloads for the SDK either, of course. This doesn't stop Valve from intentionally/unintentionally [shipping parts of the SDK in Proton, I guess](https://github.com/ValveSoftware/Proton/tree/proton_8.0/lsteamclient).

{{< series-nav "ffxiv-oct2023" >}}

