---
title: "Using OpenXR without real hardware"
date: 2023-11-30
draft: false
tags:
- OpenXR
- Virtual Reality
- Augmented Reality
---

I'm interested in trying out [OpenXR again, the Khronos VR/AR API](https://www.khronos.org/OpenXR/). It could be called the [Vulkan](https://www.vulkan.org/) of XR and unifies the assorted mess of different APIs used for VR and AR into a unified API, or so it claims. I won't go into detail how to use OpenXR, I'm assuming you already have an application that uses it and have a basic understanding how it works.

Getting to the point, I like to test my software often and I tend to do it on a lot of devices. For VR/AR, I frequently run into cases where I don't have an HMD (Head Mounted Device) handy, like on a laptop. Even with a headset in hand, it's a pain to move around with it on my head, dealing with booting up Steam or Oculus etc. Using real hardware is also out of the question for automated testing!

# Monado

Fortunately there's an answer: [FreeDesktop's Monado](https://monado.freedesktop.org/)! (Not related to the Xenoblade weapon of the same name, unfortunately.) It's a open source OpenXR runtime that implements drivers for many devices like the [HTC Vive](https://www.vive.com/us/) and the [Valve Index](https://www.valvesoftware.com/en/index). For now we don't care about any of that, (as cool as it is.) How can Monado make XR development easier?

Well there's a feature that they don't seem to advertise much: simulating HMDs. There's two ways to accomplish this, the "simulated" or the "remote" driver. We will need to install and setup the Monado runtime though.

# Installing Monado

Installing it is a little messy because it's not packaged in a lot of Linux distributions. This is a quick guide, and they have [way better instructions than what I could write](https://monado.freedesktop.org/getting-started.html). I used for the [monado` AUR package](https://aur.archlinux.org/packages/monado) and that seemed to work.

On desktop systems there's two ways to use Monado: as a SteamVR driver or standalone via `monado-service`. In my testing I used it as a SteamVR driver. Run this command to add Monado as a driver:

```bash
$ ~/.steam/steam/steamapps/common/SteamVR/bin/vrpathreg.sh adddriver /usr/share/steamvr-monado
```

You probably don't want to have it as installed as a SteamVR driver all the time though, so run this command when you're done playing around:

```bash
$ ~/.steam/steam/steamapps/common/SteamVR/bin/vrpathreg.sh removedriver /usr/share/steamvr-monado
```

Here's [the guide on how to use Monado standalone with it's own OpenXR runtime](https://monado.freedesktop.org/getting-started.html#service). I find that it emits way more verbose logs than running through SteamVR, and you need to use it if you want to get proper graphical bindings for the simulated devices.

# Simulated Driver

The "simulated" driver which does exactly what it says on the tin. It advertises a HMD and some controllers so your application has something to connect to, and it's possible to run parts of your code without expensive hardware.

To use the simulated driver, disconnect any real HMDs and other devices and OpenXR should fall back to it. If it doesn't, your build probably doesn't have this driver built. When running your application Monado should dump some information in the stdout including the names of the devices, like "Simulated HMD".

If you're using the Monado runtime, `xrGetInstanceProperties` will say the runtime is "monado". If you're using SteamVR to launch Monado, the runtime will be reported as "SteamVR/OpenXR" but the system name via `xrGetSystemProperties` should say "monado".

There's one issue with this driver: it's incredibly simple and you can't configure it at all. It simulates two controllers and an HMD, but you can't change any of it at runtime. But there's another driver that Monado provides that's better than the simulated driver, let's check that out too!

# Remote Driver

This is a souped up version of the "simulated" driver. You can do some fancy stuff like changing the values of the HMD and controllers in a GUI. To use the remote driver, there's two ways to do it. One way is using a config file at `~/.config/monado/config_v0.json` with these contents:

```json
{
        "active": "remote",
        "remote": {
                "version": 0,
                "port": 4242
        }
}
```

You can also use `P_OVERRIDE_ACTIVE_CONFIG=remote` to activate it as well, but I don't think you can configure the port (it defaults to 4242.)

This tells Monado to activate the "remote" driver, and start listening on the configured port. After running your application (and keep it running, obviously) launch `monado-gui` and click the "Remote" button and you'll notice lots of fun boxes to spin and buttons to push.

That's all good and great, but I couldn't figure out an easy way to control it outside of the GUI. It looks like Monado has an internal API for remote devices but that's not exposed to consumers. Anyway, I hope this helps and/or inspires someone with their VR projects! ☺️
