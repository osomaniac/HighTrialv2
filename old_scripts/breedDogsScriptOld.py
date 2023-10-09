import json
import random
from . import getColorNameScript

dogOneFile = open("Dog1.json", "r")
dogOneObj = json.load(dogOneFile)

dogTwoFile = open("Dog2.json", "r")
dogTwoObj = json.load(dogTwoFile)

dogOneName = dogOneObj["name"]
dogTwoName = dogTwoObj["name"]

breed = dogOneObj["breed"]
breedFilePath = breed + ".json"
breedFile = open(breedFilePath, "r")
breedObj = json.load(breedFile)
phenotypeNames = breedObj["fields"]["phenotypeNames"]
dominanceValues = breedObj["fields"]["dominanceValues"]

dogOneGenetics = dogOneObj["genetics"]["colorGenetics"]
dogTwoGenetics = dogTwoObj["genetics"]["colorGenetics"]

if(dogOneObj["sex"] == dogTwoObj["sex"]):
    print("Uh oh! You can't breed two dogs of the same sex.")
    exit()

print(f"Let's breed {dogOneName} and {dogTwoName}...")
print("---------------------------------------")
print()
litterSize = random.randint(2,8)
print(f"Bella had {litterSize} puppies!")
print()
for puppy in range(litterSize):
    print(f"Puppy {puppy + 1}:")
    puppyGenetics = {}
    for alele in dogOneGenetics.keys():
        puppyGenes = []
        dogOneGenes = dogOneGenetics[alele].split("/")
        puppyGenes.append(random.choice(dogOneGenes))
        dogTwoGenes = dogTwoGenetics[alele].split("/")
        puppyGenes.append(random.choice(dogTwoGenes))
        puppyGenes.sort()
        puppyGenetics[alele] = puppyGenes[0] + "/" + puppyGenes[1]
    print(f"Genetics: {puppyGenetics}")
    colorName = getColorNameScript.getColorName(puppyGenetics, phenotypeNames, dominanceValues)
    print(f"Color: {colorName}")
    print()
