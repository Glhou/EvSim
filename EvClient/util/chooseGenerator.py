

def choose(generators, radius):
    choosed = None
    # search for a generator in the radius to be the default one
    for generator in generators:
        if generator['dist'] < radius:
            choosed = generator
    if choosed == None:
        return -1
    for generator in generators:
        if generator['dist'] < radius:
            if generator['price'] < choosed['price']:
                choosed = generator
    return choosed['port']
