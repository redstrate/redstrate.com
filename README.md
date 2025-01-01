# redstrate.com

This is the source code of my personal website hosted at [redstrate.com](https://redstrate.com/).

## Building

You need [Hugo](https://gohugo.io/installation/) (extended edition) to build the site. To build the site, just run `hugo` and the built site will appear in `public`.

```
$ cd redstrate.com
$ hugo
```

For quick development, Hugo has a built-in HTTP server that auto-reloads on changes:

```
$ cd redstrate.com
$ hugo server
```

### Gallery System

The galleries are defined via JSON, located under `data`. The files are rarely edited by hand, I use [Redai](https://codeberg.org/redstrate/Redai) to edit these. The JSON is read by Hugo when the site is built via [Content adapters](https://gohugo.io/content-management/content-adapters/).

## Contributing

Fixes for content errors like typos are appreciated, along with general fixes to the site like a broken image link.

## License

![License](https://licensebuttons.net/l/by-sa/3.0/88x31.png)

The content of this website is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). There may be other copyrighted works showcased on this website that are licensed differently.

The Hugo themes of this website is licensed under the MIT license.
