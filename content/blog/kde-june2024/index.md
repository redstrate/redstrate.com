---
title: "My work in KDE for June 2024"
date: 2024-06-27
draft: false
tags:
- Linux
- Open Source
- KDE
- Qt
toc: true
series:
- My Work in KDE
---

Welcome back! I skipped last month because I was busy with other stuff, and I didn't have much to discuss anyway.

# Akademy

I'm finalizing my travel plans for Akademy 2024, I'll also be attending QtCS in Wurzburg as well. At the time of writing, the program has not been announced yet. So I'm not sure if I'm giving a talk yet, but fingers crossed 🤞

# Art on Wayland

A common problem with artists inquiring about the KDE Wayland session is that a lot of information is passed down. Some of the information is clearly out of date, and it just spreads. On top of that, factual information is scattered across multiple wiki pages, forum posts, and chat messages. I wrote up a nice long page (personally maintained by me, mind) at https://artonwayland.redstrate.com/. If all goes well, I hope to retire this page in a year or two.

In terms of actual software, as you probably heard - gsetwacom was created by Peter as a xsetwacom-esque replacement on GNOME. I created our own, called ktabletconfig. I personally don't have a use for this tool, but I wanted to create it anyway. I hope it serves someone well!

# Plasma

Merged the tablet tester: https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/1970

Explain what left-handed mode does in the tablet kcm, because even I didn't know: https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/2300

Rebased and merged Aki Sakurai's "map to workspace" feature: https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/2304

Fixed the wrong aspect ratio for the output item: https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/2305

# Tokodon

Improved wording and capitalization, again: https://invent.kde.org/network/tokodon/-/merge_requests/499

Merged support for quoted posts: https://invent.kde.org/network/tokodon/-/merge_requests/483

I've also been working on a metrics page, since Mastodon lacks this kind of feature (and it usually is supplanted by closed source solutions like MastoMetrics.) This is entirely client-side and it uses the publicly available information that anyone can access[^1]. You can perform the same ritual with a little bit of Python. Or sit there with a spreadsheet and dedicate some time clicking...

To prevent hammering the server because Tokodon has to download all of your public posts, the process is not automatic and requires a button press to sync again. The post data is saved in a local database and never leaves your computer[^2]. I'm hoping that promotion teams find this useful. I'm also vehemently against user-specific metrics, so there's no stupid stuff like "these are a list of users who liked your post the most". That's just invasive. The metrics database only stores the post ID, the numeric statistics and the post content.

# Krita

Fix the "DEV BUILD" badge going to a 404: https://invent.kde.org/graphics/krita/-/merge_requests/2171

Fix the lag in the tablet tester when using it with a S-Pen on Android: https://invent.kde.org/graphics/krita/-/merge_requests/2172

Multiple small improvements for the S-Pen on Android: https://invent.kde.org/graphics/krita/-/merge_requests/2170

# NeoChat

Fixed the map showing up even though no locations were shared: https://invent.kde.org/network/neochat/-/merge_requests/1763 and also fixed copyright link activation.

Fixed the QR code not showing up in the account page: https://invent.kde.org/network/neochat/-/merge_requests/1765

Added a focus border to the appearance page modes, which helps users who need keyboard navigation: https://invent.kde.org/network/neochat/-/merge_requests/1764 (it was navigtable before, you just would have no idea which one was selected)

Removed room member highlight on click: https://invent.kde.org/network/neochat/-/merge_requests/1766

Added basic keyboard navigation for the server selection: https://invent.kde.org/network/neochat/-/merge_requests/1768

Fixed keyboard navigation in the space drawer: https://invent.kde.org/network/neochat/-/merge_requests/1769

Fixed keyboard navigation on search pages: https://invent.kde.org/network/neochat/-/merge_requests/1767

# HIG

I did some small editing to the new HIG, such as re-arranging some text and adding better links to Qt docs.

# Other

Added a generic "translate" icon we can now use in applications: https://invent.kde.org/frameworks/breeze-icons/-/merge_requests/382

Fixed keyboard navigation for Kirigami Add-on's FormComboBoxDelegate: https://invent.kde.org/libraries/kirigami-addons/-/merge_requests/248 which should help every KDE application that uses them.

{{< series-nav "kde-jan2024" "kde-march2024" >}}

[^1]: Because the tool only downloads public posts. These are usually accessible via web browser.

[^2]: To quell any fears, this is only stores your *public* posts. So in the case that someone manages to leak your database, it only contains (possibly outdated) public information.
