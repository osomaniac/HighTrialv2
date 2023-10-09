import random

def getColorName(selectedColorGenetics, phenotypeNames, dominanceValues):
    colorName = ""
    tempNameList = []
    colorDict = {}
    aIsActive = False;
    doubleMerle = False;

    for aleleKey, genetics in selectedColorGenetics.items():
        aleleOne, aleleTwo = genetics.split("/")
        if aleleKey in phenotypeNames.keys():
            colorDict[aleleKey] = None;
            tempNameDict = phenotypeNames[aleleKey]
            if(dominanceValues[aleleKey].index(aleleOne) > dominanceValues[aleleKey].index(aleleTwo)):
                if(aleleTwo in tempNameDict.keys()):
                    colorDict[aleleKey] = aleleTwo
            elif (dominanceValues[aleleKey].index(aleleOne) < dominanceValues[aleleKey].index(aleleTwo)):
                if(aleleOne in tempNameDict.keys()):
                    colorDict[aleleKey] = aleleOne
            else:
                if(aleleOne in tempNameDict.keys()):
                    if(aleleOne == "M"):
                        doubleMerle = True
                    colorDict[aleleKey] = aleleOne

    for key in phenotypeNames.keys():
        if key != "joints":
            if key in colorDict.keys() and colorDict[key] != None:
                if key == 'k':
                    aIsActive = True;
                    if colorDict[key] != "seeA":
                        tempNameList.append(phenotypeNames[key][colorDict[key]])
                elif aIsActive:
                    if colorDict[key] != 'a':
                        tempNameList.append(phenotypeNames[key][colorDict[key]])
                elif key:
                    tempNameList.append(phenotypeNames[key][colorDict[key]])
    nameList = list(set(tempNameList))
    nameList = [i for i in nameList if i is not None]
    if phenotypeNames['e']['e'] in nameList:
        colorName += phenotypeNames['e']['e']
        return colorName
    elif phenotypeNames['e']['Em'] in nameList:
        colorName += phenotypeNames['e']['Em'] + " "
    if phenotypeNames['b']['b'] in nameList and phenotypeNames['d']['d'] in nameList:
        colorName += phenotypeNames['joints']['b/d'] + " "
    elif phenotypeNames['m']['M'] in nameList and phenotypeNames['d']['d'] in nameList:
        colorName += phenotypeNames['joints']["d/M"] + " "
    elif phenotypeNames['m']['M'] in nameList and phenotypeNames['b']['B'] in nameList:
        colorName += phenotypeNames['joints']["B/M"] + " "
    elif phenotypeNames['b']['b'] in nameList:
        colorName += phenotypeNames['b']['b'] + " "
    elif phenotypeNames['d']['d'] in nameList:
        colorName += phenotypeNames['d']['d'] + " "
    elif not (phenotypeNames['a']['ay'] in nameList and aIsActive):
        colorName += phenotypeNames['b']['B'] + " "
    if phenotypeNames ['m']['M'] in nameList:
        colorName += phenotypeNames['m']['M'] + " "
    if phenotypeNames['s']['Sp'] in nameList:
        colorName += phenotypeNames['s']['Sp'] + " "
    if aIsActive:
        if phenotypeNames['a']['at'] in nameList:
            if phenotypeNames['k']['kbr'] in nameList:
                colorName += "with " + phenotypeNames['k']['kbr'] + " " + phenotypeNames['a']['at']
            else:
                colorName += "with " + phenotypeNames['a']['at']
        elif phenotypeNames['a']['ay'] in nameList:
            if phenotypeNames['k']['kbr'] in nameList:
                colorName += phenotypeNames['k']['kbr']
            else:
                colorName += phenotypeNames['a']['ay']
    return colorName


def breedDogs (dam, sire, breedDict):
    print(dam)
    print(sire)
    breed = dam['breed']
    phenotypeNames = breedDict['fields']['phenotypeNames']
    dominanceValues = breedDict['fields']['dominanceValues']
    litterMin = breedDict['fields']['litterMin']
    litterMax = breedDict['fields']['litterMax']

    damGenetics = dam['genetics']['colorGenetics']
    sireGenetics = sire['genetics']['colorGenetics']

    litterSize = random.randint(litterMin, litterMax)

    puppyList = []
    count = 1
    for puppy in range(litterSize):
        puppyGenetics = {}
        for alele in damGenetics.keys():
            puppyGenes = []
            damGenes = damGenetics[alele].split("/")
            puppyGenes.append(random.choice(damGenes))
            sireGenes = sireGenetics[alele].split("/")
            puppyGenes.append(random.choice(sireGenes))
            puppyGenes.sort()
            puppyGenetics[alele]= puppyGenes[0] + "/" + puppyGenes[1]
        colorName = getColorName(puppyGenetics, phenotypeNames, dominanceValues)
        puppy = getPuppyDict(count, colorName, puppyGenetics)
        count += 1
        puppyList.append(puppy)
    return puppyList

def getPuppyDict(count, colorName, colorGenetics):
    puppyDict = {}
    sexList = ["M","F"]
    puppyDict['name'] = "Puppy #" + str(count)
    puppyDict['sex'] =  random.choice(sexList)
    puppyDict['breed'] = "Pumi"
    puppyDict['color'] = colorName
    puppyDict['genetics'] = {'colorGenetics': colorGenetics, 'traitGenetics': None}
    return puppyDict
