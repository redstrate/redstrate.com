---
title: "Retrospective of three years of self-hosting"
date: 2023-03-27
draft: false
summary: "I've been hosting my own infrastructure for almost three years now!"
---

This website has been running almost non-stop [since November 2020](https://web.archive.org/web/20201101074137/https://redstrate.com/), according to archive.org. Since then, I have been running this website and related services myself - not physically but still taking care of admin tasks.[^1]

I wanted to go over some of the services I run, break down the costs, etc. Maybe it will give you some ideas of what you could do yourself!

## E-mail

Probably one of the biggest thing people will say _not_ to self-host. However, in my experience this has probably been one of the easiest. I'm not sure when I exactly started using my own email servers - I believe sometime in 2021 - but it's been almost painless. Of course it's a double-edged sword, if I lose any important email that's directed towards my inbox that's on me - but it's also _really_ cool to be able to say "Hey, I can be reached at josh@redstrate.com!"[^2]

One thing to note is make sure to do business with a hosting provider that doesn't block SMTP ports, to save yourself pain later[^3]. Hetzner for example doesn't block the port and I've had zero trouble with them in terms of using their servers for hosting my email.

## Matrix

I use my own [Matrix](https://matrix.org) server probably more than my own e-mail, because I love chatrooms! Hosting your own server is mostly painless - as long as you have enough system resources. If you can, I highly suggest doing so - not just for the good of the federation but also because it enables lots of cool things like using your own appservices. I have [heisenbridge](https://github.com/hifi/heisenbridge) to act as my IRC bouncer for example, something that wouldn't be easy with someone else's homeserver.

The same bragging right from e-mail applies here too, since matrix handles are made up of the domain name.

## Websites

My personal website has always been static or statically generated, and need very little maintenance. Since my websites are small and receive very little traffic, I'm able to host them all on the same box. Since I control the server, I can do cool stuff like [automatically updating Rust docs](https://docs.xiv.zone/docs/physis/) for my physis crate [from sourcehut](https://git.sr.ht/~redstrate/physis/tree/main/item/.build.yml#L12) using rsync. I also use builds.sr.ht [to update this website too](https://git.sr.ht/~redstrate/redstrate.com/tree/master/item/.build.yml#L17), once I'm done developing a blog post I simply just commit to the repository and after a minute or so it's live on the Internet!

## Nextcloud

[Nextcloud](https://nextcloud.com/) is probably the most useful thing I have, and I highly recommend using it, even if you don't self-host it. It replaces Google Drive, Apple Calendar/Contacts - everything! I use it to sync my personal contacts, calendar, files, bookmarks and more. Although the web interface is a little slow, I can't deny it's been really helpful and reliable over the years.

## Other services

Here's a quick rundown of some of the other notable services I self-host and use:
* [PeerTube](https://joinpeertube.org/) for when I rarely upload videos.
* [Invidious](https://github.com/iv-org/invidious) so I can avoid giving Google any more of my data.[^4]
* [Isso](https://isso-comments.de/) for website comments.
* [Vaultwarden](https://github.com/dani-garcia/vaultwarden) for a self-hosted Bitwarden (password vault).
* [Owncast](https://owncast.online/) for livestreaming, you can do this on PeerTube now though.

## Cost

For all of these services, Hetzner only charges me ~€40 a month - but that's overkill depending on how many services you actually plan to run.[^5] I also have a couple of domains, which are bought through Porkbun which costs me maybe another $50 USD a year. So in total, it would be about ~$60 USD a month to run everything.

For the cost of a typical AAA game each month, to provide me with reliable, open source services I can use everyday? It's very much worth it for me, at the very least to keep my sysadmin skills in check!

[^1]: Eventually I would like to move onto my own server hardware, internet provider and power/ventilation/space willing.

[^2]: Of course you can use the alias feature in your favorite email provider, but it's always cool to learn how to correctly set up MX records and Postfix yourself. Stuff other people don't really appreciate, but cool to me.

[^3]: It is possible to still self-host email even if you can't send SMTP directly, I used to use GMail as a forwarder while I was still on DigitalOcean. In my opinion, while it works it definitely complicates things and it's easier just to host your mailserver on a host that doesn't block the ports.

[^3]: Some people might point out that Invidious is moot here if I'm the only one using the server - well you're right! Ideally, other people should be using the server to muddle the data.

[^4]: In all honestly, this box is probably overkill even for the services I run right now. Eventually I would like to run heavier stuff on the box, so it's nice to have the headroom because moving servers is a pain.
