---
title: "Obscure Qt: Qt5 QMap and C++20 Ranges"
date: 2024-10-30
draft: false
tags:
- Qt
series:
- Obscure Qt
summary: "A neat trick for iterating through QMaps in Qt5, if you have access to C++20."
---

I was working on a project that still uses Qt5 and I wanted to port from [Qt's own `foreach` keyword](https://doc.qt.io/qt-6/foreach-keyword.html). In Qt6 it's possible to write code like this:

```cpp
QMap<QString, int> map;
...
for (int value : std::as_const(map))
    cout << value << endl;
```

Unfortunately in Qt5 this is not possible, as it was never implemented. You don't even have [`asKeyValueRange()`](https://doc.qt.io/qt-6/qmap.html#asKeyValueRange)!

You may have seen it before, but someone has already written [a great StackOverflow answer backporting this feature to Qt5](https://stackoverflow.com/questions/8517853/iterating-over-a-qmap-with-for/77994379#77994379). However, this codebase has C++20 available! (Yes, really.) The SO answer needs to add a whole bunch of extra wrapper code, but it's actually possible to use C++ [`for`](https://en.cppreference.com/w/cpp/language/for) by using [`std::ranges::subrange`](https://en.cppreference.com/w/cpp/ranges/subrange):

```cpp
QMap<QString, int> map;
...
for (int value : std::ranges::subrange(map.constBegin(), map.constEnd()))
    cout << value << endl;
```

Take care when porting to ensure the previous `foreach` code didn't depend on a copy of the container. Use `constBegin()`/`constEnd()` when needed to [ensure the container doesn't detach](https://doc.qt.io/qt-6/implicit-sharing.html).
