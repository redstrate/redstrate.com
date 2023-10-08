---
title: "Obscure Qt: Customizing the log messages"
date: 2023-10-08
draft: false
tags:
- Qt
series:
- Obscure Qt
---

If you've worked with Qt for a while, you're probably well aware of how basic the default log formatting is.

```bash
Lorem ipsum dolor sit amet, consectetur...
Login error
qt.accessibility.atspi: Error in contacting registry: "org.freedesktop.DBus.Error.Disconnected" "Not connected to D-Bus server"
```

In the case of the last error, it's happens to be categorized and is marked as much. There isn't much to work with though! Compare this to other logging frameworks, such as Rust's [tracing crate](https://crates.io/crates/tracing).

```bash
2023-10-04T12:33:21.142204Z DEBUG your::application: Login Error
2023-10-04T12:33:21.152001Z DEBUG your::application: Lorem ipsum dolor sit amet, consectetur...
```

That's the default formatting it gives you out of the box! (It also [rightfully boasts about that fact](https://github.com/tokio-rs/tracing#in-applications).) It gives us the timestamp, the message level (Debug, Info, etc) and the category.

To give Qt's messages the same treatment, take a look at the [documentation for qSetMessagePattern](https://doc.qt.io/qt-6/qtlogging.html#qSetMessagePattern). This function allows you to tweak the message formatting to include some very useful data (that should be included by default, in my opinion.) For setting it as the default for applications not under your control (or don't want to modify the source code for), this pattern can be set via the `QT_MESSAGE_PATTERN` environment variable.

Apart from the expected `%{type}` and `%{category}` there's some interesting variables. One is printing the application name (`%{appname}`), useful if you're tearing apart an application that might merge output from other Qt applications. There's also `%{threadid}` and `%{qthreadptr}` which can be useful instead of print debugging the current thread. To figure out what specific place in your code printed a statement, you can use `%{file}`, `%{function}` and `%{line}`. When it comes to C++ code, it does what you expect it to:

```bash
/home/foo/bar/src/main.cpp 131 main: It's time to go!
^                          ^   ^
|                          |   |
%{file}              %{line}   %{function}
```

What's really cool though is that QML code also supports these variables! Here's a `console.log` from a JavaScript block:

```bash
qrc:/qt/qml/org/your/application/Main.qml 106 expression for onCompleted: Hello!
```

If you're not in the presence of a QML debugger, you can now track down those pesky messages you have hidden away in your giant QML codebase! I used this recently to figure [out the location of a Kalendar bug](https://invent.kde.org/pim/merkuro/-/merge_requests/410) after hunting down the JavaScript function that emitted an error message. Unfortunately the `%{backtrace}` variable only spews out backtraces in C++ and you'll have a backtrace that starts and ends in the JavaScript engine usually.
