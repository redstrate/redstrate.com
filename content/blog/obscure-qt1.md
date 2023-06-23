---
title: "Obscure Qt: Default choices for DelegateChooser"
date: 2023-04-19
draft: false
tags:
- Qt
series:
- Obscure Qt
---

I decided to start a short series of describing weird, obscure Qt behavior! Because of my new job, I'm working with Qt even more than I did before. As I'm finding new and undocumented behavior, I feel that it's too useful to be posted on something like Mastodon and then forgotten.

A really useful component is the [DelegateChooser](https://doc.qt.io/qt-6/qml-qt-labs-qmlmodels-delegatechooser.html). Say you are building a chat application, and you need to support different types of messages (a regular text message, an image, a location and so on). In order to accomplish this in Qt Quick is to do something like this:

```qml
DelegateChooser {
	role: "type"
	DelegateChoice {
		roleValue: "message"
		
		Label {
			required property string message
		
			text: message
		}
	}
	
	DelegateChoice {
		roleValue: "image"
		
		Image {
			required property string url
			
			source: url
		}
	}
	
	...
}
```

At runtime, Qt Quick will use `role` and check it against every one of the [DelegateChoice](https://doc.qt.io/qt-6/qml-qt-labs-qmlmodels-delegatechoice.html)'s `roleValue`. When it finds a match, it'll choose that component. Really useful stuff!

But today I encountered a different case, where I had a bunch of values in my role but not all of them had to be specialized. In most cases I had one component that's generalized for most of them, but only one or two that needed a different component. Curiously, the Qt documentation does not say how to accomplish something like this:

```cpp
switch(type) {
	case SpecialType:
		return SomeComponent{};
	default:
		return DefaultComponent();
}

```

After doing some digging I found a Qt mailing list from a couple years ago, with some developers discussing what to do about "default" cases for `DelegateChooser`. Someone suggested leaving the `roleValue` empty as a way to support that. And it seems to work in Qt today, albeit undocumented:

```qml
DelegateChooser {
	role: "type"
	DelegateChoice {
		roleValue: "specialType"
		
		Label {		
			text: "I'm a special type!"
		}
	}
	
	// This is the default choice!
	DelegateChoice {		
		Label {
			text: "I'm everyone else..."
		}
	}
}
```
