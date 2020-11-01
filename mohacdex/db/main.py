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
        print("\tLoading {}.csv".format(table.name))
        load_table(table, connection)

def load_table(table, connection):
    csv_path = "data/{}.csv".format(table.name)
    csv_path = pkg_resources.resource_filename(__name__, csv_path)
    try:
        with open(csv_path, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            rows = [row for row in reader]
            connection.execute(table.insert(), rows)
    except FileNotFoundError:
        print("File not found: {}.csv".format(table.name))

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
