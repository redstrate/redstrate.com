# redstrate.com

[![builds.sr.ht status](https://builds.sr.ht/~redstrate/redstrate.com.svg)](https://builds.sr.ht/~redstrate/redstrate.com?)

This is the source code of my personal website hosted at [redstrate.com](https://redstrate.com/).

## Building

You need [Hugo](https://gohugo.io/installation/) (extended edition) to build the site, and optionally Python to run miscellaneous scripts.

To build the site, just run `hugo` and the built site will appear in `public`.

```
$ cd redstrate.com
$ hugo
```

For quick development, Hugo has a built-in HTTP server that auto-reloads on changes:

```
$ cd redstrate.com
$ hugo server
```

### Art

The art gallery is defined via JSON (in `art`, and other directories in site root) and uses Python to generate the front-matter Markdown files that Hugo consumes. To refresh the gallery, re-run `scripts/gen_art.py`.

## License

![License](https://licensebuttons.net/l/by-sa/3.0/88x31.png)

The content of this website is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). There may be other copyrighted works showcased on this website that are licensed differently.

The Hugo themes of this website is licensed under the MIT license.
