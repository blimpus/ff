accepted_positions = {'rb', 'qb', 'flex', 'te', 'k', 'dst'}
def switch(position):
    position = position.lower()
    if position not in accepted_positions:
        print("entered value does not match a valid position. Valid positions are rb, qb, te, k, dst, flex")
        exit(1)
    return "https://www.fantasypros.com/nfl/rankings/"+position+".php"