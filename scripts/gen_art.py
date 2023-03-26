import os
import shutil
import json


def write_field(f, key, value):
    f.write(key + ": " + value + "\n")


def parse_art_json(title, year, date, nsfw, original_filename, filename, json_file):
    with open(original_filename + '.md', 'w') as f:
        print(json_file)
        json_data = json.load(json_file)
        print(json_data)

        f.write('---\n')

        if "title" in json_data:
            write_field(f, 'title', json_data["title"])
        else:
            if title is not None:
                write_field(f, 'title', title)

        write_field(f, 'layout', 'art-detail')
        write_field(f, 'filename', '/art/' + filename + '.webp')

        if "alt_text" in json_data:
            write_field(f, 'alt_text',
                        "\"" + json_data["alt_text"].replace('\n', '').replace('"', '\\"') + "\"")

        if "date" in json_data:
            if "-" in json_data["date"]:
                write_field(f, 'date', json_data["date"])
            else:
                write_field(f, 'date', str(json_data["date"]) + '-01-01')
                write_field(f, 'excludefeed', "true")
        else:
            if date is None:
                write_field(f, 'date', str(year) + '-01-01')
                write_field(f, 'excludefeed', "true")
            else:
                split = date.split("-")
                month = split[0]
                day = split[1]

                write_field(f, 'date', str(year) + '-' + month.zfill(2) + "-" + day.zfill(2))

        write_field(f, 'slug', filename)

        if "characters" in json_data:
            f.write("characters:\n")
            for character in json_data["characters"]:
                f.write("- " + character + "\n")

        if "tags" in json_data:
            f.write("arttags:\n")
            for tag in json_data["tags"]:
                f.write("- " + tag.lower() + "\n")

        if  "nsfw" in json_data:
            write_field(f, 'nsfw', str(json_data["nsfw"]).lower())

        if "mastodon_url" in json_data:
            write_field(f, 'mastodon_url', json_data["mastodon_url"])

        if "pixiv_url" in json_data:
            write_field(f, 'pixiv_url', json_data["pixiv_url"])

        if "newgrounds_url" in json_data:
            write_field(f, 'newgrounds_url', json_data["newgrounds_url"])

        f.write('---\n')

        if "description" in json_data:
            f.write(json_data["description"])
            f.write('\n')

def parse_art_piece(json, year, date, nsfw):
    filename_without_ext = os.path.splitext(json["filename"])[0]

    with open(art_output_directory + "/" + filename_without_ext + '.md', 'w') as f:
        f.write('---\n')

        write_field(f, 'slug', filename_without_ext)

        if "title" in json.keys():
            write_field(f, 'title', json['title'])
            write_field(f, 'alt_text', json['title'])

        if date is None:
            write_field(f, 'date', str(year) + '-01-01')
            write_field(f, 'excludefeed', "true")
        else:
            split = date.split("-")
            month = split[0]
            day = split[1]

            write_field(f, 'date', str(year) + '-' + month.zfill(2) + "-" + day.zfill(2))

        write_field(f, 'layout', 'art-detail')
        write_field(f, 'filename', '/art/' + json['filename'])

        if nsfw is not None:
            write_field(f, 'nsfw', str(nsfw).lower())

        f.write('---\n')


art_data_directory = '../art'
art_output_directory = '../content/art'

shutil.rmtree(art_output_directory)
os.mkdir(art_output_directory)

with open('../data/art.json', 'r') as f:
    art_data = json.load(f)

    collected_years = set()

    for category in art_data["categories"]:
        for year in category["years"]:
            collected_years.add(year["year"])

    for year in collected_years:
        new_dir_path = os.path.join(art_output_directory, str(year))
        os.mkdir(new_dir_path)

        with open(new_dir_path + '/_index.md', 'w') as f:
            f.write('---\n')

            write_field(f, 'title', str(year) + ' Art')
            write_field(f, 'layout', 'gallery')
            write_field(f, 'json', 'art')
            write_field(f, 'thumbnails', 'true')
            write_field(f, 'selectedyear', str(year))

            f.write('---\n')

    with open(art_output_directory + '/_index.md', 'w') as f:
        f.write('---\n')

        write_field(f, 'title', 'Art')
        write_field(f, 'layout', 'art')

        write_field(f, 'summary', 'My personal art gallery.')

        f.write('aliases:\n')
        f.write('- /gallery\n')

        f.write('featured:\n')
        for piece_name in art_data["featured"]:
            for category in art_data["categories"]:
                for year in category["years"]:
                    for piece in year["pieces"]:
                        filename_without_ext = os.path.splitext(piece["filename"])[0]

                        if filename_without_ext == piece_name:
                            f.write('- filename: ' + piece["filename"] + '\n')
                            f.write('  date: ' + piece["date"] + '\n')
                            f.write('  year: ' + str(year["year"]) + '\n')
                            f.write('  title: ' + piece["title"] + '\n')

        f.write('years:\n')
        for year in reversed(list(collected_years)):
            f.write('- ' + str(year) + '\n')

        f.write('---\n')

    num_eno = 0
    num_noneno = 0
    num_json = 0

    for category in art_data["categories"]:
        for year in category["years"]:
            for piece in year["pieces"]:
                filename_without_ext = os.path.splitext(piece["filename"])[0]

                path = os.path.join(art_data_directory, filename_without_ext + ".eno")
                json_path = os.path.join(art_data_directory, filename_without_ext + ".json")

                nsfw = None
                if "nsfw" in piece.keys():
                    nsfw = piece["nsfw"]

                title = None
                if "title" in piece.keys():
                    title = piece["title"]

                if os.path.isfile(json_path):
                    num_json = num_json + 1
                    with open(json_path, "r") as file:
                        print(file)
                        if "date" in piece.keys():
                            parse_art_json(title, year["year"], piece["date"], nsfw,
                                           art_output_directory + "/" + filename_without_ext, filename_without_ext,
                                           file)
                        else:
                            parse_art_json(title, year["year"], None, nsfw, art_output_directory + "/" + filename_without_ext,
                                           filename_without_ext, file)
                else:
                    if os.path.isfile(path):
                        num_eno = num_eno + 1
                        with open(path) as f:
                            if "date" in piece.keys():
                                parse_art(title, year["year"], piece["date"], nsfw,
                                          art_output_directory + "/" + filename_without_ext, filename_without_ext,
                                          f.read())
                            else:
                                parse_art(title, year["year"], None, nsfw,
                                          art_output_directory + "/" + filename_without_ext, filename_without_ext,
                                          f.read())
                    else:
                        num_noneno = num_noneno + 1
                        if "date" in piece.keys():
                            parse_art_piece(piece, year["year"], piece["date"], nsfw)
                        else:
                            parse_art_piece(piece, year["year"], None, nsfw)

    total = num_eno + num_json + num_noneno

    print("Art coverage: {}/{}".format(num_eno + num_json, total))
    print("# of JSON: {}/{}".format(num_json, total))
    print("# of ENO: {}/{}".format(num_eno, total))
