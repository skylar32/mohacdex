import argparse
import csv
import pkg_resources
import mohacdex.db
from sqlalchemy import create_engine

def load(connection):
    print("Creating tables...")
    mohacdex.db.Base.metadata.create_all(connection)
    print("Loading tables...")
    for table in mohacdex.db.Base.metadata.sorted_tables:
        print("\tLoading {}.csv ... ".format(table.name), end='', flush=True)
        load_table(table, connection)
        print("OK", flush=True)

def load_table(table, connection):
    csv_path = "data/{}.csv".format(table.name)
    csv_path = pkg_resources.resource_filename(__name__, csv_path)
    try:
        with open(csv_path, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            rows = list(validate_rows(table, reader))
            connection.execute(table.insert(), rows)
    except FileNotFoundError:
        print("File not found: {}.csv".format(table.name))

def validate_rows(table, reader):
    for row in reader:
        for column_name, value in row.items():
            column = table.c[column_name]

            if value == '' and column.nullable:
                row[column_name] = None
            elif value == 'True':
                row[column_name] = True
            elif value == 'False':
                row[column_name] = False
            
        yield row

def reload(connection):
    print("Dropping tables...")
    mohacdex.db.Base.metadata.drop_all(connection)
    load(connection)

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'database', help="SQLA URI for the database."
    )
    subparsers = parser.add_subparsers(title="commands")

    # load
    load_parser = subparsers.add_parser(
        'load', help="Builds the database from scratch."
    )
    load_parser.set_defaults(func=load)

    # reload
    reload_parser = subparsers.add_parser(
        'reload', help="Destroys and then rebuilds the database."
    )
    reload_parser.set_defaults(func=reload)

    return parser

def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)
    engine = create_engine(args.database)

    with engine.begin() as connection:
        args.func(connection)
