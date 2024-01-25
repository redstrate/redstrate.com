---
title: "Quick thoughts on Apple's DMA changes"
date: 2024-01-25
draft: false
tags:
- Apple
---

So today Apple has [released information on how iOS will soon be DMA-compliant](https://www.apple.com/newsroom/2024/01/apple-announces-changes-to-ios-safari-and-the-app-store-in-the-european-union/). We don't know *everything*, to be clear. They said more details will come soon but this gives us a good enough idea.

(Note that this is written from the perspective of a US citizen, and these changes do not apply in my country.)

# Background

If you somehow haven't been following the DMA news lately, here's a quick rundown. The European Union is cracking down on "gatekeepers" - basically companies that "gatekeep" their respective platforms from 3rd parties. This includes Apple, of course. They have been pretty stringent on side loading and 3rd party payment processing and is the pinnacle gatekeeper. The DMA or "Digitial Markets Act" sets some ground rules to force these gatekeepers to follow.

You can read more about it [here](https://digital-markets-act.ec.europa.eu/index_en).

# Apple's Changes

What's really cool is the kinds of changes Apple is forced to do, and it's really interesting as a long-time iOS user. I suggest reading [this Apple developer page](https://developer.apple.com/support/dma-and-apps-in-the-eu/) instead of the press releases and other journalism as it's concise enough and has a nice FAQ at the bottom we'll reference later.

Here's a quick breakdown of what they're changing in iOS:
* Alternative marketplaces (*NOT* sideloading in general, basically another person must do it through their marketplace.)
* Alternative browser engines
* Alternative payment methods, along with alternatives to Apple Pay
* New default app controls (like for browsers)
* "Interoperability" requests (basically requesting Apple to create an API for a previously inaccessible device feature)
* Some new business terms in the EU

Some of the stuff is obvious and fantastic, but the two most interesting ones is the "alternative browser engines" and "interoperability requests" to me. If you aren't aware, every browser on iOS is Safari - no seriously *all* of them. Firefox and Chrome are just Safari, for example. I think this is a fantastic change, but it comes with some caveats - the browsers must be "approved" by Apple first. Hm. They claim it's for security reasons and that's kind of the "gotcha" in a lot of these DMA changes. Interoperability requests is also very interesting, it's vague but basically you can ask for Apple to add new APIs for stuff you want to use (like NFC?) and they will review it on a case-by-case basis. I wonder how that will be used in the future?

# What about the US?

This is all well and great, but how does these DMA changes affect us Americans? Well guess what they don't! Before we get into Apple's "why" (and the true "why") let's go over which DMA changes come over to other countries. Here's the list:

Yeah you read that right, none of that is leaving the EU - at least for now. Here's Apple's reasoning as to why:

> Apple is not offering these changes outside of the EU **because this is not the safest system for our users**. We’ve been very clear about [new](https://www.apple.com/privacy/docs/Building_a_Trusted_Ecosystem_for_Millions_of_Apps.pdf) [threats](https://www.apple.com/newsroom/2023/05/app-store-stopped-more-than-2-billion-in-fraudulent-transactions-in-2022/) the DMA [introduces](https://www.youtube.com/watch?v=f0Gum8UkyoI) — including increased risks for malware, fraud and scams, illicit and objectionable content, and reduced ability for Apple to respond to and remove malicious apps. The changes required by the DMA also involve new technologies and processes that are untested and may require further development.
>
> At Apple, we've always built every innovation on a crucial foundation: the trust of our users. And we’ve never taken that trust for granted. That’s why — from our operating systems to the App Store — we build in privacy and security protections from the ground up. We review apps and app updates to help make sure they’re transparent about the data they collect, to identify malware and fraud, and to uphold standards for quality and performance that meet our users’ expectations.
>
> In the EU, **the Digital Markets Act requires us to make changes to a formula that has served users and developers exceptionally well** — changes that introduce new options, but also new risks. The changes we’re sharing represent Apple’s work to comply with the law and to help reduce new privacy and security risks the DMA creates for our users.

(Bolding is by me, not Apple.)

In short, Apple's reasoning is that it's clearly "not safe". This is really weird when you think about macOS which has all of these same options (default browser choice, alternative browser engines and marketplaces) and yet has not turned into complete hellscape like they're claiming? They also say that they will implement "malware checks" before installing 3rd party applications, and a lot of these changes must be reviewed before developers can take advantage of them. I don't know if Apple is selling themselves short or not, they can't seem to make up their mind.

In my eyes, the reason is clear - it's because they *hate* these changes and will do everything in their power to stop them. These changes leaving the EU would be "game over" for them and their stranglehold on doing business. I bet they will fight it to hell and back if American politicians start singing praises of the DMA and start implementing similar rulings. It's as simple as that, in my opinion - regardless of their true reasoning.

---

By the way, as a quick tangent to end this on: I was [an "app developer" for them once]({{< ref "breaking-even" >}}). To be clear, a macOS app developer but the App Store experience is mostly the same. They are quick to defend and "white knight" these app developers in said DMA changes, apparently. The App Store has served me so well, right? Kinda, because even though I sold a bunch of copies of my application, I ended up _losing_ money because Apple's chunk of the pie ate up all of that. Didn't really feel like Apple was really helping in any way, other than sucking up my money. (By the way, Apple makes way, way more money than I could ever earn.)

Not to mention the absolutely inane and usually non-productive app review process on their App Stores, why are these problems suddenly not mentioned on their site? These kinds of observations might poke holes in their narrative, I guess.
