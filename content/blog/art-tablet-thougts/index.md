---
title: "Art Tablet Thoughts"
date: 2023-06-28
draft: true
summary: "When working on my engine, I wanted to clean up my debug gizmos a bit. The first thing to tackle is drawing bounding boxes!"
tags:
- C++
- Math
series:
- Graphics Dump
---

I've been getting fed up with my current portable art solution. I'm a digital artist, and for a good while I've been using an [iPad Pro](https://www.apple.com/ipad-pro/) + [Procreate](https://procreate.com/)[^1] on the go. That was my only art program for a while, and I had used [Krita](https://krita.org/) before that. When I bought a traditional desktop drawing tablet again, I started using Krita again and used my iPad for travel. Yes, the one featured in my blog series about supporting it under Linux![^2]

I asked on Mastodon for suggestions, and all signs seemed to be pointing towards the Lenovo Yoga series. Some others suggested a Surface but I've heard that those are pretty painful to get running Linux, although run fine after that. My experience with Lenovo is that Linux developers seem to gravitate towards them more, and some of their machines are shipping Linux so I'll bet on them instead of Microsoft.

So I snapped one up yesterday, and played around with it for a bit. All of the drawings featured in the article is done on the tablet, of course. First, let me lament the qualms that I have with my iPad Pro...

# iPad Pro

My usual software on my iPad is Procreate, but it's not what I'd stable. I'm not sure if that's the fault of the iPad itself. As I want to draw in bigger resolutions, it eats up more memory on a tablet that only has 4 gigabytes (and even less available to applications, apparently). Here's a _real_ video of Procreate crashing as I browse my gallery. To it's credit, it doesn't crash that often once you're actually working in the software.

The memory limitations of my iPad model crops up from time to time. It's usually minor stuff like the layers being limited to a certain number, which means I can't use layers freely. I hear that the situation has improved on the more recent, but _more expensive_ iPad models. Whatever, my iPad Pro still works too good for me to think about replacing it with a slightly better model. I only replaced my previous one because I wanted a bigger screen (This was pre-XPPen, so this was my only tablet).

Multitasking is a big ask for this setup, and it's sort of possible but in Apple's own frustrating way. Even though it has a giant 13" screen, it still feels like I need to baby it constantly. And the cherry on top is that if Procreate - or any app crashes - it brings down your _entire session_ which means you need to set up everything you're working on again. This happens more often than I'd like, but thankfully Procreate has excellent auto-saving.

All of these issues are ultimately minor compared to the biggest one - the _file formats_ are different. I work in KRA files (and sometimes ORA, when moving between Drawpile and something else) but it's not a fantastic exchange format for Procreate. Procreate can freely exchange with PSD, but it's annoying to keep converting back and forth when working on a project. Even worse, there's a chance that depending on how big the canvas is, it may not even be openable in Procreate!

I have long lamented that the Procreate gallery structure _sucks_ unless you are exclusively working in Procreate. You can't _sync_ files, you can't _access_ them outside of Procreate's sandbox[^3] and so on. It wouldn't be half bad if I could stick a folder of working PSDs in Nextcloud, and then access them via a file selector like in other iOS applications, but no. I guess 3D face painting is more important to the Procreate team, and I can't blame them - it's a boring task. Who wants to be known as the person who implemented the "file selector"? And yet, it's a boring task that would make artists lives (like mine!) a whole lot easier.

People who use an iPad as their primary device (I know some mutuals use one) might be sweating bullets right now, but there's a reason why I was able to squeeze a decent amount of art from this machine, it _does work_. For me, it's gotten more frustrating as I wanted it to co-exist with my Linux desktop, and my artwork keeps getting more complex. For some, my complaints are non-issues.

# Lenovo Yoga

I really didn't need another beefy and huge business-class machine, I went with a cheaper 13 inch model instead. I did upgrade to the 7000-series AMD processor, 16gb of RAM and the 512 GB internal storage. In my uninformed opinion, soldered 8GB RAM is dead-on-arrival e-waste for anything but web browsing. The base system cost $899 USD, and then I bought a Wacom Ink Plus stylus for 99$ USD. The store I bought it from offered same-day delivery from one of those VC-funded courier delivery services. It looked like a 14-year old dropped it off at my door, not kidding.

When you first pick one up, it's nice and heavy. It's body is made up of plastic and metal, but feels premium. The metal parts play the part, at least - the plastic bits like the screen edges flex and creak. That's pretty nitpicky though, you would never touch these parts when holding the device normally.

The killer feature of the Yoga series is it's ability to turn from a laptop, into a tablet or a kickstand sorta deal. It's actually really neat, I really like the ability to "kickstand" it wherever I want. The screen and body is thin enough, where in tablet mode it doesn't feel extremely thick. It's definitely more uncomfortable in the hand compared to an iPad, but I think that's a fair trade-off.

## Screen

The screen is nice and bright, but it's only 1920x1200. That's okay though, HiDPI screens would've bumped up the price considerably. Not only that, they're harder on the battery and scaling isn't perfect on Linux. Ideally, it would be something like 4K so it has 200% scaling, which is a bit much. I find using a 1080p screen at this size is fine, my desktop drawing tablet is 1920x1080 at a much bigger size and I don't even mind it there. This screen also had this weird sticky coating at first, but after some touching it was smooth enough for comfortable pen and touch use.

## Keyboard

The keyboard is alright, my biggest complaint is that Fn is where Ctrl usually is for me and I'm not sure why they put it there. That's something I can get used to though. There's a physical ESC key, so that's nice to have at this keyboard size.

## Operating System

The first thing that pops up when booting the machine is Windows 11. No! No! No! I flashed a USB stick with Fedora KDE 38 on it, and wiped the machine. Everything worked out of the box: Display, Wi-Fi, Bluetooth, Touch, Pen... all of it! The keyboard brightness isn't controllable through KDE, I'm guessing something is missing on the kernel side. The firmware looks like it's updatable through fwupd, so Windows will probably never run on this machine ever again.

I'm not sure whether I'm going to stick with Wayland or X11 on this machine, I'm currently on Wayland. The machine is 125% scaling out of the box, something impossible on X11. I could run it on 100% just fine, but then it's becomes really difficult to touch anything. Before you comment about using Wayland despite no color correction, uhm - I don't have any way to properly calibrate my screens anyway. If I had a screen calibrator, that would be a different story :-)

## Screen

One more point about the screen, it doesn't rotate out of the box in KWin. I'm not sure why yet, but that might be future work for me! Instead, I used iio-sensor-proxy and a small Python script (based off of X) and modified it use kscreen-doctor instead of xrandr. And boom, working screen orientation! I'm guessing this is what it looks like when KWin does it, and it feels pretty nice and fast.

The only problem is that if you try to fold it up and rotate it, it might fail. I'm 90% sure this is a hardware issue, there's a switch or sensor that doesn't tell the accelerometer to turn on until the keyboard is folded back that's too slow. You can tell because the keyboard lights switch off after a second.

Tablet mode also doesn't work, but I'm not sure what tells KWin to turn it on. If someone knows, let me know.

## Pen

I picked up a Wacom Ink Plus stylus, and it worked right out of box in Linux. There's one issue though, it has _squiggly lines_! I'm not sure what's at fault here: the pen, the digitizer, the software...? I can play with sample rates with xsetwacom on X11 but that only hides the issue and doesn't solve it.

It's not a huge problem, but kind of annoying that this is even an issue. I did a bunch of precursory searches about this, but didn't turn up much. If you know anything about this issue please let me know.

## Touch

Touch support is pretty good, I can finger drag and zoom out of the box in Krita which is pretty cool. Firefox won't do this unless you have it running Wayland native, after that it works.

## Fingerprint Sensor

Doesn't work out of the box, and honestly don't care enough to make it work right now. I use the fingerprint sensor on my work laptop, and it works so-so. I end up fighting with it more than just entering a password, and the underlying software (PolKit, PAM, etc) doesn't handle my preferred usecase perfectly right now. My ideal workflow is that of Macs, where you can enter a password _or_ a fingerprint and neither is required for the other. A password is required after some time, of course.

[^1]: I also list which programs I used in my gallery :-)
[^2]: If you're wondering how it functions a few months later, it's been great! It's a real dust collector though, even when I don't use it for a day it collects dust like no problem. Software-wise, the kernel module still rebases on recent kernels but I've been putting off upstreaming it. The dials don't work yet, and I have the work laid out in front of me but attempts to get KWin to co-operate haven't worked out too well.
[^3]: Except if you use the export/import functions, and the drag & drop feature. Fortunately, you can select which format Procreate selects when exporting via dragging which is a really nice detail.
