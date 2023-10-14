---
title: "Marrying Qt and Tracing message output"
date: 2023-10-14
draft: true
tags:
- Qt
- Rust
---

Do you have a mixed of Qt and Rust in your project, and dislike how your logs mismatch? Do you want one single source of truth, so it's easier to redirect to a file or other destination? I've been hitting my head against this problem, and developed a novel solution for marrying the two. It's even possible to transfer information like the source file and line!

As mentioned previously in my [Obscure Qt post on logging]({{< ref "obscure-qt3" >}}), the default logging format for Qt isn't that great in the first place. Not to mention, it looks really out of place when mixing in logs from [Tracing](https://crates.io/crates/tracing) in the Rust parts of the code:

```bash
2023-10-04T12:33:21.310435Z DEBUG physis::gamedata: Extracting file file="exd/Item_41000_en.exd"
Uploading imgui font size 512 x 64
false true true
Looking up "Hyur" "Midlander" "Male"
2023-10-04T12:33:21.405104Z DEBUG physis::gamedata: Extracting file file="chara/equipment/e0000/model/c0101e0000_top.mdl"
Uploading imgui font size 512 x 64
false false true
```

The Qt logger looks basic compared to the default formatting of the Tracing crate. But what if we try to marry their output together? If I want to do some advanced operations like redirecting it all to a file, then it becomes easier as we're only dealing with one log!

In this case the final application is Qt based, so I think the best course of action is to shove everything through their logger. Going in the other direction might be an interesting future project :-)

## Piping messages from Tracing into Qt

First we'll want to set up a C function for use by our application. You can use your favorite FFI crate, but in this example we'll just use good ol' `extern "C"` Let's begin by defining a `LogCallback` type. It will take a [QtMsgType](https://doc.qt.io/qt-6/qtlogging.html#QtMsgType-enum), the message, file and line.

```rust
#[repr(i8)]
pub enum QtMsgType {
    Debug = 0,
    Warning = 1,
    Critical = 2,
    Fatal = 3,
    Info = 4,
}

type LogCallback = unsafe extern "C" fn(QtMsgType, *const c_char, *const c_char, i32);

#[no_mangle]
pub unsafe extern "C" fn setup_logging(callback: LogCallback) {
    tracing_subscriber::registry().with(CustomLayer {
        callback
    }).init();
}
```

Now it's time to define `CustomLayer`. As hinted above, it's a struct with one member: the callback. The trait we'll implement is [Layer<S>](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/layer/trait.Layer.html).

```rust
pub struct CustomLayer {
    callback: LogCallback,
}

impl<S> Layer<S> for CustomLayer
    where
        S: tracing::Subscriber,
{
    fn on_event(
        &self,
        event: &tracing::Event<'_>,
        _ctx: tracing_subscriber::layer::Context<'_, S>,
    ) {
        ...
    }
}
```

Getting the message content is a bit complex due to how Tracing works. We need to implement the [Visit](https://docs.rs/tracing/latest/tracing/field/trait.Visit.html) trait which and it's up to you to decide how to format each field. For this example we'll simply append each field into one big string.

```rust
struct CustomVisitor<'a> {
    string: &'a mut String,
}

impl tracing::field::Visit for CustomVisitor<'_> {
    fn record_debug(&mut self, field: &tracing::field::Field, value: &dyn std::fmt::Debug) {
        write!(self.string, "{} = {:?} ", field.name(), value).unwrap();
    }
}
```

Here we implement the [record_debug](https://docs.rs/tracing/latest/tracing/field/trait.Visit.html#tymethod.record_debug) and print each field via the [Display trait](https://doc.rust-lang.org/std/fmt/trait.Display.html) (`{:?}`). Let's plug it into our `CustomLayer`'s `on_event()`:

```rust
let mut buffer: String = String::new();
let mut visitor = CustomVisitor {
    string: &mut buffer
};
event.record(&mut visitor);
```

In order for the message levels to transfer, let's set up a match case for converting [Tracing's Level](https://docs.rs/tracing/latest/tracing/struct.Level.html) to Qt's. Except Qt doesn't have a  tracing level so we'll map that to `QtMsgType::Debug`.

``` rust
let msg_type = match *event.metadata().level() {
    Level::ERROR => QtMsgType::Critical,
    Level::WARN => QtMsgType::Warning,
    Level::INFO => QtMsgType::Info,
    Level::DEBUG => QtMsgType::Debug,
    Level::TRACE => QtMsgType::Debug
};
```

The final step on the Rust side is to pass the message and relevant information over the FFI layer like so:

```rust
unsafe {
    let file = if let Some(file) = event.metadata().file() {
        CString::new(file).unwrap().into_raw()
    } else {
        null()
    };

    let line = if let Some(line) = event.metadata().line() {
        line as i32
    } else {
        -1
    };

    (self.callback)(msg_type, CString::new(buffer).unwrap().into_raw(), file, line);
}
```

In order to hook this up to the Qt application, we'll write a bit of C++ code which will glue it to the Qt logging:

```cpp
extern "C" void setup_logging(void (*callback) (QtMsgType type, const char*, const char*, int));

void callback(QtMsgType type, const char *message, const char *file, int line) {
    QMessageLogContext context;
    context.file = file;
    context.line = line;

    qt_message_output(type, context, message);
}

int main() {
    setup_logging(callback);

    ...
}
```

There's an undocumented function in the [<QtLogging>](https://doc.qt.io/qt-6/qtlogging.html) header called [qt_message_output](https://codebrowser.dev/qt5/qtbase/src/corelib/global/qlogging.cpp.html#_Z17qt_message_output9QtMsgTypeRK18QMessageLogContextRK7QString) that will format your message and hand it off to the current message handler. If you don't want to depend on that, using [qFormatLogMessage](https://doc.qt.io/qt-6/qtlogging.html#qFormatLogMessage) works as well.

You can view the [full example on git.sr.ht](https://git.sr.ht/~redstrate/logging-qt-and-tracing). Here's the expected output:

```bash
[2023-10-13 21:54:42.765] [info] [src/lib.rs:77] message = something has happened!
[2023-10-13 21:54:42.765] [critical] [src/lib.rs:78] message = something bad has happened!
[2023-10-13 21:54:42.765] [info] [/home/josh/Development/logging-qt-and-tracing/main.cpp:28] Application started up!
```
