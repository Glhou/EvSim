

def chooseBestsPorts(generators, radius, nbBest):
    choosedPorts = []
    inRange = []
    # search for a generator in the radius to be the default one
    for generator in generators:
        if generator['dist'] < radius:
            inRange.append(generator)
    if not inRange:
        return []
    generatorPriceInRange = [generator['price'] for generator in inRange]
    generatorPriceInRange = sorted(generatorPriceInRange)[
        :min(nbBest, len(generatorPriceInRange))]
    for generator in inRange:
        if generator['price'] in generatorPriceInRange:
            choosedPorts.append(generator['port'])
    return choosedPorts
