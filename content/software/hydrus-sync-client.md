---
title: "hydrus-sync-client"
date: 2022-10-12
draft: false
layout: "project"
tags:
- Hydrus
license: GPLv3
source: "https://git.sr.ht/~redstrate/hydrus-sync-client/"
---

Sync hydrus databases using rsync

<!--more-->
---

Ever feel like you need a way to sync Hydrus databases across multiple machines? With `hydrus-sync-client`, you can
easily synchronize your Hydrus database with a rsync server.

This was originally a Bash script that I decided to rewrite in Rust, so please excuse how ugly it is right now :-)

## Process

1. The program first checks the last hostname that synchronized, this is used later to decide whether to sync first.
2. Then the lockfile is checked, if it is locked - the program exits.
3. If the hostnames don't match, we sync the files before launching.
4. Hydrus is launched and you can continue like normal.
5. Once Hydrus is closed, the file synchronization now happens in reverse.
6. Before the program exits, the lockfile is reset and the last hostname is updated.

As long as you ensure you're always using `hydrus-sync-client` to run Hydrus, the sync process is mostly foolproof.
