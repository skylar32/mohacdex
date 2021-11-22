# mohacdex
a human-readable pokémon database that doesn't include the junk i don't care about. i mostly made this for my own purposes (and to eventually serve as the backbone for a fanmon website application), so it may have limited utility to you depending on your purposes. if that's the case, maybe check out [porydex](https://github.com/CatTrinket/porydex) (after which this database is modelled), or  [pokéapi](https://pokeapi.co/).

## installation
```sh
$ pip install virtualenv
$ virtualenv venv
$ venv/bin/activate
$ pip install .
$ mohacdex sqlite:///mohacdex.db load
```
this will create a new file, mohacdex.db, in the base directory of the repository. note that as long as the virtual environment is activated, the `mohacdex` command may be used anywhere, and the database file may be created anywhere and with any name you please. it will be assumed that all mohacdex operations from this point on are performed from within the virtual environment.

## usage
```python
import mohacdex.db
import sqlalchemy, sqlalchemy.orm

engine = sqlalchemy.create_engine("sqlite:////path/to/mohacdex.db")
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

galarian_farfetchd = session.query(mohacdex.db.Pokemon).filter(mohacdex.db.Pokemon.identifier=="farfetchd-galar").one()
print(galarian_farfetchd.abilities["hidden_ability"].name) # Scrappy
```
i've written this code with the objective of making it as human-readable as possible—sometimes at the expense of efficiency—so for more details, i encourage you to poke around at the [models](mohacdex/db/schema)!
