---
title: "Follow-up: Move to Sourcehut"
date: 2022-04-26
draft: false
tags:
- GitHub
- sourcehut
---

This is a follow-up post to my blog post detailing the changes I've made to how my source code is hosted. Basically, I'm trying to
move away from GitHub for my primary code hosting to a (in my opinion, better suited for me) platform. After some deliberation, I
ultimately landed on sourcehut, and plan to detail the benefits I've gained, and the things I've losted. Hint, it works pretty well,
so I'm excited to dig into my new workflow :-)

First, I wanted to cover the topic of migrating stuff to sourcehut - which is probably what you're going to do if you had a bunch
of repositories hosted elsewhere (Github, Gitlab, etc) like me. Unfortunately, **sourcehut's HTTPS migration breaks your repository**.
Yes, I should get around to reporting this, but it's pretty bad. Basically, it looks like it clones your repository fine, but once
you actually try to do any git operations it fails to pickup on the refs. Very weird, but I ended up writing my own sourcehut
migration scripts here. This also includes remote fixups, because I push to multiple mirrors for most of the repositories I maintain.

I also want to cover sourcehut's website functionality, compared to GitHub and GitLab. It's important to note that this is extremely
biased, as I do not like GitHub's features basically trending towards being more of a "social media site". The addition of the "For you"
tab pretty much solidifies my idea that this is what it's going to end up being, so there's that. sourcehut on the other hand, is
a programmer oriented first and foremost. This is most obvious in the UI, which is textbook definition of "minimally functional" -
this is not a bad thing to me, which is clear if you're on this website right now.

Despite this, there is still a certain charm to how simple this website functions - and browsing the sourcecode is very similiar
to minimal git interfaces like cgit and gitweb which I very much enjoy. However, it's at this point where sourcehut starts exceeding
GitHub in certain aspects that I very much appreciate. An example of this is the Projects feature - which allows you to organize
source code repositories, mailing lists, issue trackers and stuff into a concise page. Here's an example of what it looks like
for Astra:

This is extremely useful as it allows me to organize my projects into what they are - projects. Compare this to GitHub where
repository **is** a project and in my opinion this makes way more sense to me. Unfortunately, I have not tried out most of
sourcehut's features such as the mailing lists, issue trackers, build server etc but I'm already impressed by the speed of the
site and the ease of use.
