---
title: "Matrix Update"
date: 2022-06-29
draft: false
---

If any Matrix admins are reading this, I have a quick update at what's happening to my two old matrix servers: redstrate.com and ryne.moe. These servers are now _defunct_ and if you are seeing any users from them, I recommend either blacklisting the servers on an ACL or just kicking them - but there's no current Synapse server actually backing them so they shouldn't be able to perform any actions anyway.

A user tipped me off a month ago or so that my last server (ryne.moe) was being a home to over _12,000_ bot accounts which I didn't even notice, due to a lapse in my own configuration. While I enabled SSO, and disabled password login - I unfortunately forgot to disable _registration_ which enabled all of those bot accounts to be collected in the first place. What's worse, is that so much time has passed that the database file is pretty much useless - sitting at over _40 gigabytes_ and the server is extremely slow to do anything with. So, I decided the best course of action is to just give up on that domain and move on. I'm terribly sorry if your room was affected by my adopted bots, I hope to not make that same mistake twice :-)

Thankfully I keep backups of both servers, hopefully my old @redstrate handles will be leaving all of the rooms I'm in, else I would be kept as a ghost user. Unfortunately I cannot do the same to the bot users, because processing 12,000 users will take an extremely long time. Right now both domains do not respond to matrix requests, and the synapse servers are turned off so fortunately nothing is left exploitable. In the future I would love to see a feature in the Matrix spec to mark a domain as "defunct" _without_ having to still run a synapse server, maybe some kind of json file I can place somewhere.
