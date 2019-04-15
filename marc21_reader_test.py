from Marc21_reader import marc21_reader

marc21 = marc21_reader.get_marc21('sample_data/000055275.marc')
records = marc21_reader.get_records(marc21)

author = marc21_reader.get_author(records)
print(author)