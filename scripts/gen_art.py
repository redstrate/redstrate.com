import os
import shutil
import json


def write_field(f, key, value):
    f.write(key + ": " + value + "\n")


def parse_art_json(output_directory, filename, json_file):
    json_data = json.load(json_file)

    year = None

    if "date" in json_data:
        if "-" in json_data["date"]:
            year = int(json_data["date"].split('-')[0])
        else:
            year = int(json_data["date"])

    base_directory = os.path.join(art_output_directory, str(year))
    if not os.path.exists(base_directory):
        os.mkdir(base_directory)

    with open(os.path.join(base_directory, filename) + '.md', 'w') as f:
        f.write('---\n')

        if "title" in json_data:
            write_field(f, 'title', json_data["title"])

        if "date" in json_data:
            if "-" in json_data["date"]:
                write_field(f, 'date', json_data["date"])
            else:
                write_field(f, 'date', str(json_data["date"]) + '-01-01')
                write_field(f, 'excludefeed', "true")

        write_field(f, 'layout', 'art-detail')
        write_field(f, 'filename', '/art/' + filename + '.webp')

        if "alt_text" in json_data:
            write_field(f, 'alt_text',
                        "\"" + json_data["alt_text"].replace('\n', '').replace('"', '\\"') + "\"")

        write_field(f, 'slug', filename)

        if "characters" in json_data:
            f.write("characters:\n")
            for character in json_data["characters"]:
                f.write("- " + character + "\n")

        if "tags" in json_data:
            f.write("arttags:\n")
            for tag in json_data["tags"]:
                f.write("- " + tag.lower() + "\n")

        if "nsfw" in json_data:
            write_field(f, 'nsfw', str(json_data["nsfw"]).lower())

        if "mastodon_url" in json_data:
            write_field(f, 'mastodon_url', json_data["mastodon_url"])

        if "pixiv_url" in json_data:
            write_field(f, 'pixiv_url', json_data["pixiv_url"])

        if "newgrounds_url" in json_data:
            write_field(f, 'newgrounds_url', json_data["newgrounds_url"])

        if "program" in json_data:
            write_field(f, 'program', json_data["program"])

        f.write('---\n')

        if "description" in json_data:
            f.write(json_data["description"])
            f.write('\n')

        return year


art_data_directory = '../art'
art_output_directory = '../content/art'

shutil.rmtree(art_output_directory)
os.mkdir(art_output_directory)

collected_years = set()

for filename in os.listdir(art_data_directory):
    f = os.path.join(art_data_directory, filename)

    if os.path.isfile(f):
        filename_without_ext = os.path.splitext(filename)[0]

        with open(f, "r") as file:
            collected_years.add(parse_art_json(art_output_directory, filename_without_ext, file))

for year in collected_years:
    with open(os.path.join(art_output_directory, str(year), '_index.md'), 'w') as f:
        f.write('---\n')

        write_field(f, 'title', str(year))
        write_field(f, 'layout', 'gallery')
        write_field(f, 'json', 'art')
        write_field(f, 'thumbnails', 'true')
        write_field(f, 'selectedyear', str(year))

        f.write('---\n')

with open('../data/art-config.json', 'r') as f:
    json_data = json.load(f)

    featured_pieces = json_data["featured"]

with open(art_output_directory + '/_index.md', 'w') as f:
    f.write('---\n')

    write_field(f, 'title', 'Art')
    write_field(f, 'layout', 'art')

    write_field(f, 'summary', 'My personal art gallery.')

    f.write('aliases:\n')
    f.write('- /gallery\n')

    f.write('featured:\n')
    for piece_name in featured_pieces:
        piece_path = os.path.join(art_data_directory, piece_name + ".json")
        with open(piece_path, 'r') as piecef:
            json_data = json.load(piecef)

            f.write("- filename: " + piece_name + '.webp\n')
            f.write('  date: ' + json_data["date"] + '\n')
            f.write('  title: ' + json_data["title"] + '\n')

    f.write('years:\n')
    for year in reversed(list(collected_years)):
        f.write('- ' + str(year) + '\n')

    f.write('---\n')
