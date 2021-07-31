import mohacdex.db, sqlalchemy, sqlalchemy.orm

dmax_moves = {
    "normal": "max-strike",
    "fire": "max-flare",
    "water": "max-geyser",
    "grass": "max-overgrowth",
    "electric": "max-lightning",
    "ice": "max-hailstorm",
    "fighting": "max-knuckle",
    "poison": "max-ooze",
    "ground": "max-quake",
    "flying": "max-airstream",
    "psychic": "max-mindstorm",
    "bug": "max-flutterby",
    "rock": "max-rockfall",
    "ghost": "max-phantasm",
    "dragon": "max-wyrmwind",
    "dark": "max-darkness",
    "steel": "max-steelspike",
    "fairy": "max-starfall",
    "status": "max-guard"
}

engine = sqlalchemy.create_engine("sqlite:////home/kyeugh/code/serfetchdex/mohacdex.db")
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()
pokemon = session.query(mohacdex.db.Pokemon).order_by(mohacdex.db.Pokemon.order).all()

with open("/home/kyeugh/code/mohacdex/mohacdex/db/data/pokemon_moves_max_new.csv", 'w') as outfile:
    outfile.write("pokemon_identifier,move_identifier\n")
    for mon in pokemon:
        print(f"Writing {mon.identifier}... ", end='')
        types = []
        movesets = [[item for sublist in mon.levelup_moves.values() for item in sublist], mon.machine_moves, mon.tutor_moves, mon.egg_moves]
        for moveset in movesets:
            if moveset:
                for move in moveset:
                    print(move.identifier)
                    if move.damage_class == "status" and "status" not in types:
                        types.append("status")
                    elif move.type not in types:
                        types.append(move.type)
        if types:
            types.sort(key={k:v for v,k in enumerate(dmax_moves.keys())}.get)
            for item in types:
                outfile.write(f"{mon.identifier},{dmax_moves[item]}\n")
        print(f"Wrote {mon.identifier}")