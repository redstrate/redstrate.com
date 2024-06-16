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

Welcome back! I skipped last month because I was busy with other stuff and didn't have anything to show.

# Plasma

Merged the tablet tester: https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/1970

Explain what left-handed mode does in the tablet kcm, because I didn't even know: https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/2300

Rebased and merged Aki's "map to workspace" feature: https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/2304

Fixed the wrong aspect ratio for the output item: https://invent.kde.org/plasma/plasma-desktop/-/merge_requests/2305

# Tokodon

Improved wording and capitalization, again: https://invent.kde.org/network/tokodon/-/merge_requests/499

Merged support for quoted posts: https://invent.kde.org/network/tokodon/-/merge_requests/483

# Krita

Fix the "DEV BUILD" badge going to a 404: https://invent.kde.org/graphics/krita/-/merge_requests/2171

Fix the lag in the tablet tester when using it with a S-Pen on Android: https://invent.kde.org/graphics/krita/-/merge_requests/2172

Multiple small improvements to the S-Pen on Android: https://invent.kde.org/graphics/krita/-/merge_requests/2170

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

