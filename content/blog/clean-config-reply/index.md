---
title: "Getting a clean config directory, with KConfigXT!"
date: 2023-10-08
draft: false
tags:
- KDE
- Qt
- CPlusPlus
- Open Source
---

This is a sort-of reply to [Herzenschein's blog post](https://rabbitictranslator.com/kconfig/) from a few months ago. He goes over how to tell [KConfig](https://api.kde.org/frameworks/kconfig/html/) put it's files into app-specific folders instead of dumping them into the garbage bin of `~/.config`. He noted that he hasn't touched [KConfigXT](https://develop.kde.org/docs/features/configuration/kconfig_xt/) yet, so this is how to make it work with KConfigXT applications.

However you'll notice by default KConfigXT generates constructors for your configuration class like this:

```cpp
class Config : public KConfigSkeleton
{
  Q_OBJECT
  public:

    Config( QObject *parent );
    ~Config() override;
...
```

That's not useful, and it took me a minute to figure out how to allow KConfigSkeleton and the KConfig compiler to let me pass `AppConfigLocation`. However, the solution is very simple.

First, you need to make sure it's not a `Singleton`. (There's probably a way to make it work with a singleton though.) Make sure that setting is turned off in your `.kcfgc`:

```ini
File=config.kcfg
ClassName=Config
Mutators=true
DefaultValueGetters=true
GenerateProperties=true
Singleton=false
```

And then in your `.kcfg`, modify the `<kcfgfile>` block to add `arg = "true"` instead of hardcoding a filename. It will look something like this:

```xml
<kcfgfile arg="true" />
```

Once you run the compiler again, you'll get a constructor that allows you to pass a KSharedConfig!

```cpp
class Config : public KConfigSkeleton
{
  Q_OBJECT
  public:

    Config( KSharedConfig::Ptr config = KSharedConfig::openConfig() );
    ~Config() override;
...
```

And then you call the usual function:

```cpp
new Config(KSharedConfig::openConfig("myappconfigrc", KConfig::SimpleConfig, QStandardPaths::AppConfigLocation));
```

Now enjoy your configuration file living in it's own directory! Here's the [constructor parameter logic in KConfig](https://invent.kde.org/frameworks/kconfig/-/blob/master/src/kconfig_compiler/KConfigSourceGenerator.cpp?ref_type=heads#L212) which was essential in figuring this out.
