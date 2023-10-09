import csv
import json
import random

breedObjDict = {}
breedStr = "Pumi.json"

jsonFile = open(breedStr, "r")
breedObj = json.load(jsonFile)

breedModel = breedObj["model"]
breedPK = breedObj["pk"]
breedFields = breedObj["fields"]

    

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
    print(nameList)
    nameList = [i for i in nameList if i is not None]
    print(nameList)

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

def getNewGenetics(genetics, nonFoundations):
    selectedGenetics = {}
    for alele in genetics.keys():
        goodChoice = False;
        while(not goodChoice):
            geneChoice = getAleleChoice(alele, genetics[alele]);
            if nonFoundations != None:
                goodChoice = verifySingleChoice(alele, geneChoice, nonFoundations);
            else:
                goodChoice = True
        selectedGenetics[alele] = geneChoice
    if nonFoundations != None:
        checkJointChecks(selectedGenetics, genetics, nonFoundations)
    return selectedGenetics;

def getAleleChoice(alele, aleleOptions):
    chosenAleles = []
    choiceList = getWeightedList(aleleOptions)
    chosenAleles.append(random.choice(choiceList))
    chosenAleles.append(random.choice(choiceList))
    chosenAleles.sort()
    colorChoice = chosenAleles[0] + "/" + chosenAleles[1]
    return colorChoice;

def checkJointChecks(selectedGenetics, genetics, nonFoundations):
    if("joint" in nonFoundations):
            jointChecks = nonFoundations["joint"]
            for toCheck in jointChecks:
                aleleOne, aleleTwo = toCheck.split('/')
                checks = jointChecks[toCheck]
                if aleleOne in selectedGenetics.keys():
                    if aleleTwo in selectedGenetics.keys():
                        choiceOne = selectedGenetics[aleleOne]
                        choiceTwo = selectedGenetics[aleleTwo]
                        if(choiceOne in checks):
                            selectedGenetics[aleleTwo] = verifyJointChoice(aleleTwo, choiceOne, choiceTwo, checks, genetics)

def verifyJointChoice(aleleTwo, choiceOne, choiceTwo, checks, choiceList):
    badChoice = True
    while(badChoice):
        if(choiceTwo in checks[choiceOne]):
            choiceTwo = getAleleChoice(aleleTwo, choiceList[aleleTwo])
        else:
            badChoice = False
    return choiceTwo

def verifySingleChoice(alele, geneChoice, nonFoundations):
    if(alele in nonFoundations):
        if not (geneChoice in nonFoundations[alele]):
            return True    
    else:
        return True
    return False

def getWeightedList(aleleOptions):
    choiceList = []
    for opt in aleleOptions:
        tempList = []
        tempList = [opt] * int(aleleOptions[opt])
        choiceList += tempList
    return choiceList;

def createFoundationDog(dogBreedFields, dogInfoFields):
    newDog = {}
    print("Creating Foundation Dog...")
    newDog['name'] = dogInfoFields['dogName']
    newDog['kennel'] = dogInfoFields['kennelName']
    newDog['sex'] = dogInfoFields['sex']
    newDog['breed'] = dogBreedFields["breedName"]
    newDog['color'] = ""
    newDog['genetics'] = {}
    colorGenetics = dogBreedFields.get("colorGeneticFlags")
    traitGenetics = dogBreedFields.get("traitGeneticFlags")
    nonFoundations = dogBreedFields.get("nonFoundations")
    phenotypeNames = dogBreedFields.get("phenotypeNames")
    dominanceValues = dogBreedFields.get("dominanceValues")

    if colorGenetics is not None:
        selectedColorGenetics = getNewGenetics(colorGenetics, nonFoundations)
        """selectedColorGenetics = {
            'k': 'kbr/ky',
            'a': 'ay/a',
            'e': 'E/e',
            'b': 'b/b',
            'd': 'D/d'
        }"""
        selectedColorName = getColorName(selectedColorGenetics, phenotypeNames, dominanceValues)
        newDog['genetics']['colorGenetics'] = selectedColorGenetics
        newDog['color'] = selectedColorName
    else:
        newDog['genetics']['colorGenetics'] = None

    if traitGenetics is not None:
        selectedTraitGenetics = getNewGenetics(traitGenetics, nonFoundations)
        newDog['genetics']['traitGenetics'] = selectedTraitGenetics
    else:
        newDog['genetics']['traitGenetics'] = None    
    return newDog

dogName = "Lirai"
kennelName = "Rhythm Pumik"
dogSex = "Male"
print("Welcome to High Trial's Import System")
"""createDogResponse = input("Would you like to create a new dog? (y/n) ")
if(createDogResponse not in ('y','Y')):
    exit()
else:
    print()
    print("Great! Let's get some information about your new dog.")
    correct = False
    dogName = "Lirai"
    kennelName = "Rhythm Pumik"
    dogSex = "Male"
    
    while not correct:
        dogName = input("What would you like your dog's registered name to be? ")
        correctResponse = input("Is " + dogName +" the correct name? (y/n) ")
        if(correctResponse in ('Y','y')):
            correct = True
        else:
            print("Okay, let's try again.")
            print()
    print("Great name choice!")
    correct = False
    while not correct:
        dogSex = input("What sex would you like "  + dogName + " to be? (male/female) ")
        correctResponse = input("Is " + dogSex +" the correct sex? (y/n) ")
        if(correctResponse in ('Y','y')):
            correct = True
        else:
            print("Okay, let's try again.")
            print()
    print("Great! ", dogName, " will be a ", dogSex, ".")
    correct = False
    while not correct:
        kennelName = input("What is your kennel name? ")
        correctResponse = input("Is " + kennelName +" the correct name? (y/n) ")
        if(correctResponse in ('Y','y')):
            correct = True
        else:
            print("Okay, let's try again.")
            print()
    print("Great! ", dogName, " will be registered to ", kennelName, ".")
    print("Sit tight while we create your new import!")
    print()
    print("--------------------------------------------------------")
    print()
    """
dogInfoFields = {'dogName': "Lirai", 'kennelName': "Rhythm Kennel", 'sex': "Male"}
dog = createFoundationDog(breedFields, dogInfoFields)
print("--------------------------------------------------------")
print("Name: ", dog['name'])
print("Breed: ", dog['breed'])
print("Sex: ", dog['sex'])
print("Color Name: ", dog['color'])
print("Color Genetics: ", dog['genetics']['colorGenetics'])
print("Owned by: ", dog['kennel'])
print("--------------------------------------------------------")
print()

dogJson = json.dumps(dog)
jsonFile = open("Dog4.json", "w")
jsonFile.write(dogJson)
jsonFile.close()

dogInfoFields = {'dogName': "Bella", 'kennelName': "Rhythm Kennel", 'sex': "Female"}
dog = createFoundationDog(breedFields, dogInfoFields)
print("--------------------------------------------------------")
print("Name: ", dog['name'])
print("Breed: ", dog['breed'])
print("Sex: ", dog['sex'])
print("Color Name: ", dog['color'])
print("Color Genetics: ", dog['genetics']['colorGenetics'])
print("Owned by: ", dog['kennel'])
print("--------------------------------------------------------")
print()

dogJson = json.dumps(dog)
jsonFile = open("Dog3.json", "w")
jsonFile.write(dogJson)
jsonFile.close()

"""
breedObjList.append(breedObjDict)

breedJson = json.dumps(breedObjList)
jsonFile = open("breeds.json", "w")
jsonFile.write(breedJson)
jsonFile.close()
"""

