---
title: "Opening KAddressBook Addresses With KDE Marble"
date: 2022-02-01
draft: false
tags:
- KDE
aliases:
- /articles/opening-kaddressbook-addresses-with-kde-marble/
---

This is probably the most specific use case I'll ever post on this blog :-p I noticed whenever I click an address in [KAddressBook](https://apps.kde.org/kaddressbook/), it opens it in [OpenStreetMap](https://www.openstreetmap.org/) in your web browser by default. Huh? <!--more-->

**Edit:** Recent Plasma versions now have the ability to select KDE Marble as the default maps application, and KAddressBook dropped support for setting the "Show Address" function like as pictured below. However, KDE Marble still lacks a way to properly decode addresses, making this functionality useless still. I will further update the article once I find a workaround, or I contribute something upstream.

But I learned that [KDE Marble](https://marble.kde.org/) exists, a native KDE app that's basically just FOSS Google Earth (the cool old version, I think it's called [Google Earth Pro](https://www.google.com/earth/versions/#earth-pro)?) Anyway, for some reason KAddressBook cannot open addresses with KDE Marble out of the box. Weird, right? So, I thought this would be a cool scripting exercise, and this is the solution I came up with:

1. We set the "Show Address" to open an "External Application", this is where we'll call our python script `geo.py`:

![KAddressBook settings](/blog/img/kaddressbook-settings.png)

The full command is:

```marble --latlon "$(python geo.py ""%s %l %r %c"")" --distance 0 --map "earth/openstreetmap/openstreetmap.dgml"```

2. Then we have a python script, using [GeoPy](https://geopy.readthedocs.io/en/stable/) and [Nominatim](https://nominatim.org/) (a free service run by OpenStreetMap, perfect since it's free, FOSS, and most importantly has reasonable rate limits for our personal use)


```
from geopy.geocoders import Nominatim
from geopy import Point
import sys

args = " ".join(sys.argv[1:])

geolocator = Nominatim(user_agent="kdemarble")
loc = geolocator.geocode(" ".join(sys.argv[1:]))
p = Point(loc.latitude, loc.longitude)
print(p.format(deg_char='°', min_char='\'', sec_char=''))
```

3. Then, simply click an address in KAddressBook, and it'll open up in KDE Marble!

## More Details

This is actually quite interesting, as I would think KAddressBook would have this functionality out of the box, however it is more work than you might think it is. First, KAddressBook stores the address of your contacts literally, like a string - it stores the Address, Region, and Location separately (this is the `%s`, `%l`, `%r` variables as shown above). However, KDE Marble only accepts longitude and latitude as command line arguments.

So this is where Nominatim comes in, which as said before - is a service run by OpenStreetMap. Its API is extremely simple, which is perfect. I originally tried to only do this in Shell and CURL, but it turned out to be much easier just to use GeoPy and Python.

![KDE Marble without the extra arguments](/blog/img/kdemarble-faraway.png)

Then, you'll notice if you don't add any extra arguments to Marble, it'll open up super far away and also in a weird default view that's not suitable for viewing addresses. Luckily, the developers already added some nice arguments to allow us to change this default behavior:

` --distance 0 --map "earth/openstreetmap/openstreetmap.dgml"`

This will set the initial distance to "0 km" and also changes the map view to OpenStreetMap, perfect!

![KDE Marble in it's ideal view for streets](/blog/img/kdemarble-fixed.png)
