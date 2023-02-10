import enolib
import os
import shutil
import json

def write_field(f, key, value):
    f.write(key + ": " + value + "\n")

def parse_art(title, year, date, nsfw, original_filename, filename, file):
    with open(original_filename + '.md', 'w') as f:
        document = enolib.parse(file)

        f.write('---\n')

        if title is not None:
            write_field(f, 'title', title)

        write_field(f, 'layout', 'art-detail')
        write_field(f, 'filename', '/art/' + filename + '.webp')
        write_field(f, 'alt_text', "\"" + document.field('Alt Text').required_string_value().replace('\n','') + "\"")

        if date is None:
            write_field(f, 'date', str(year) + '-01-01')
            write_field(f, 'excludefeed', "true")
        else:
            split = date.split("-")
            month = split[0]
            day = split[1]

            write_field(f, 'date', str(year) + '-' + month.zfill(2) + "-" + day.zfill(2))

        write_field(f, 'slug', filename)

        f.write("characters:\n")
        for character in document.list('Characters').items():
            f.write("- " + character.required_string_value() + "\n")

        f.write("arttags:\n")
        for tag in document.list('Tags').items():
            f.write("- " + tag.required_string_value().lower() + "\n")

        if nsfw is not None:
            write_field(f, 'nsfw', str(nsfw).lower())

        f.write('---\n')

        if document.optional_field('Description'):
            f.write(document.field('Description').required_string_value())
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

    for category in art_data["categories"]:
        for year in category["years"]:
            for piece in year["pieces"]:
                filename_without_ext = os.path.splitext(piece["filename"])[0]

                path = os.path.join(art_data_directory, filename_without_ext + ".eno")

                nsfw = None
                if "nsfw" in piece.keys():
                    nsfw = piece["nsfw"]

                title = None
                if "title" in piece.keys():
                    title = piece["title"]

                if os.path.isfile(path):
                    num_eno = num_eno + 1
                    with open(path) as f:
                        if "date" in piece.keys():
                            parse_art(title, year["year"], piece["date"], nsfw, art_output_directory + "/" + filename_without_ext, filename_without_ext, f.read())
                        else:
                            parse_art(title, year["year"], None, nsfw, art_output_directory + "/" + filename_without_ext, filename_without_ext, f.read())
                else:
                    num_noneno = num_noneno + 1
                    if "date" in piece.keys():
                        parse_art_piece(piece, year["year"], piece["date"], nsfw)
                    else:
                        parse_art_piece(piece, year["year"], None, nsfw)

    print("Art coverage: {}/{}".format(num_eno, num_eno + num_noneno));

