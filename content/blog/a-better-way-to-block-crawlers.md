---
title: "A different way to block AI crawlers"
date: 2024-03-26
draft: false
tags:
- Website
- AI
---

I've been asking myself recently: _"Am I really stopping **all** of those pesky AI/LLM crawlers on my site?"_ Maybe you are asking: why do you even need to keep updating your robots.txt? This is a popular topic of discussion lately too, and I even asked it on Mastodon not too long ago:

{{< stoot "mastodon.art" "111025176364115672" >}}

To keep it short, I'll mention the individualistic reason: I personally don't want to contribute to a dataset that I do not benefit from (and even if I did, I would not do so without consent.) And it seems AI/LLM companies are popping up all the time, and existing companies are quickly learning they need their own web crawler to start gobbling up data. Google, Microsoft (through their Bing brand) and so forth are also setting up crawlers specifically for AI/LLM training. It's getting really tiring having to keep up with them, and your robots.txt will soon spiral out of control[^1].

In my usual rounds today, I came across an anonymous comment mentioning there's an alternative way to write it: Block all crawlers and only allow a few. I think I'm going to try this going forward, because really I only care about Google/DuckDuckGo search indexing and I consider other crawlers to be extraneous[^2]. Said robots.txt may look like:

```robots.txt
# Block all user agents, for the whole site
User-agent: *
Disallow: /

# Allow these user agents
User-agent: Googlebot
User-agent: DuckDuckBot

# You can still specify directories you don't want these allowed crawlers to look at
Disallow: /super-secret-directory/
```

If you're FOSS-oriented, here's a couple more user agent strings you may want consider:
* `Mastodon` for Mastodon web previews (or maybe, you actually want to block that to avoid "hugs of death"!)
* `Synapse` for Matrix web previews.

[Someone mentioned on Mastodon](https://tenforward.social/@MindmeshLink/112162944428631550) that it's possible that forks of said software may be unintentionally blocked. However, I think the benefit of not having to update my robots.txt constantly is worth the occasional link preview not showing for my small website. Depending on your size/audience this may too be too big of a hammer. If someone does have a list of FOSS software that only uses crawlers for harmless stuff like [Open Graph](https://ogp.me/) then let me know.

And if you want a fun thing to do: go to your usual popular websites, and see what they block via robots.txt. It can be surprising sometimes!

[^1]: Did you know there's actually a limit to how large your robots.txt can be? [It's usually 500 KiB](https://www.rfc-editor.org/rfc/rfc9309#name-limits).

[^2]: Like, do you _really_ need Google Images indexing your site? What about an Amazon SEO crawler?
