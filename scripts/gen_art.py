import enolib
import os
import shutil
import json

def write_field(f, key, value):
    f.write(key + ": " + value + "\n")

def parse_art(title, year, date, original_filename, filename, file):
    with open(original_filename + '.md', 'w') as f:
        document = enolib.parse(file)

        f.write('---\n')

        write_field(f, 'title', title)
        write_field(f, 'layout', 'art-detail')

        if date is None:
            write_field(f, 'date', str(year) + '-01-01')
            write_field(f, 'excludefeed', "true")
        else:
            split = date.split("-")
            month = split[0]
            day = split[1]

            write_field(f, 'date', str(year) + '-' + month.zfill(2) + "-" + day.zfill(2))

        write_field(f, 'slug', filename)

        f.write("tags:\n")
        for character in document.list('Characters').items():
            f.write("- " + character.required_string_value().lower() + "\n")

        f.write('---\n')

        f.write('![')
        f.write(document.field('Alt Text').required_string_value())
        f.write('](/art/')
        f.write(filename)
        f.write('.webp)\n')

        f.write('## Commentary\n')

        f.write(document.field('Description').required_string_value())
        f.write('\n')

        f.write('## Characters\n')

        for character in document.list('Characters').items():
            f.write('* [' + character.required_string_value() + '](' + '/tags/' + character.required_string_value().lower() + ')\n')

def parse_art_piece(json, year, date):
    filename_without_ext = os.path.splitext(json["filename"])[0]

    with open(art_output_directory + "/" + filename_without_ext + '.md', 'w') as f:
        f.write('---\n')

        write_field(f, 'slug', filename_without_ext)

        if "title" in json.keys():
            write_field(f, 'title', json['title'])

        if date is None:
            write_field(f, 'date', str(year) + '-01-01')
            write_field(f, 'excludefeed', "true")
        else:
            split = date.split("-")
            month = split[0]
            day = split[1]

            write_field(f, 'date', str(year) + '-' + month.zfill(2) + "-" + day.zfill(2))

        write_field(f, 'layout', 'art-detail')

        f.write('---\n')

        f.write('![')
        f.write('](/art/')
        f.write(json["filename"])
        f.write(')\n')

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

    for category in art_data["categories"]:
        for year in category["years"]:
            for piece in year["pieces"]:
                filename_without_ext = os.path.splitext(piece["filename"])[0]

                path = os.path.join(art_data_directory, filename_without_ext + ".eno")

                if os.path.isfile(path):
                    with open(path) as f:
                        if "date" in piece.keys():
                            parse_art(piece["title"], year["year"], piece["date"], art_output_directory + "/" + filename_without_ext, filename_without_ext, f.read())
                        else:
                            parse_art(piece["title"], year["year"], None, art_output_directory + "/" + filename_without_ext, filename_without_ext, f.read())
                else:
                    if "date" in piece.keys():
                        parse_art_piece(piece, year["year"], piece["date"])
                    else:
                        parse_art_piece(piece, year["year"], None)

