---
title: "Making fail2ban work on systemd Gentoo"
date: 2022-11-03
draft: false
tags:
- Linux
- Gentoo
---

I have been transferring all of my websites and services from my Arch Docker setup to a bare-metal Gentoo box, but
got tripped up when setting up [fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page). 
<!--more-->

By default, the fail2ban config (on Gentoo) is set up like this:

```
[INCLUDES]

#before = paths-distro.conf
before = paths-debian.conf

# The DEFAULT allows a global definition of the options. They can be overridden
# in each jail afterwards.

[DEFAULT]
...
```
(this is the content of `/etc/fail2ban/jail.conf`)

How fail2ban works, is that there are multiple `path-X.conf` files, where X is the distribution fail2ban is installed on. 
There is a couple in there like `paths-arch.conf`, `paths-fedora.conf`, and so on because distributions put files in different
places. However, this _also_ controls how fail2ban reads the log files. On Gentoo systemd systems, fail2ban is configured to read
the syslog instead of the systemd journal which of course doesn't work.

To fix this, simply change the `before` path in your `/etc/fail2ban/jail.local`:

```
[INCLUDES]

before = paths-arch.conf

...
```

I used `paths-arch.conf` since it's a systemd distribution, and it seems to work fine. I plan on modifying the [fail2ban
wiki page](https://wiki.gentoo.org/wiki/Fail2ban) on the Gentoo wiki to mention this, but I wanted to share my discovery here :-)