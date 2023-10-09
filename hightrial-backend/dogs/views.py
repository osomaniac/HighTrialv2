from django.shortcuts import render, redirect
from .models import Dog, Kennel, ColorGenetics, Wallet, Litter, User
from .forms import BreedDogForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import DogSerializer
from scripts import breedDogsScript


# Create your views here.
class DogsView(viewsets.ModelViewSet):
    serializer_class = DogSerializer
    queryset = Dog.objects.all()

@login_required
def editDog(request, dog_id):
    dog = Dog.objects.get(id=dog_id);
    context = {'dog':dog}
    return render(request, 'dogs/edit-dog.html', context)

def dogs(request):
    dogs = Dog.objects.all()
    context = {'dogs':dogs}
    return render(request, 'dogs/dogs.html', context)

def dog(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    sex = dog.sex
    puppies = []
    if (sex == "M"):
        puppies.append(Dog.objects.filter(sire=dog))
    else:
        puppies.append(Dog.objects.filter(dam=dog))
    litters = []
    litterIds = []
    if puppies:
        puppies = puppies[0]
        for puppy in puppies:
            if puppy:
                if(puppy.litter.id not in litterIds):
                    if(sex == "M"):
                        partner = puppy.dam
                    else:
                        partner = puppy.sire
                    breeder = puppy.litter.breeder
                    litterIds.append(puppy.litter.id)
                    litters.append({"id":puppy.litter.id, "partner":partner, "breeder":breeder})
    colorGenetics = ColorGenetics.objects.filter(dog=dog_id).first()
    colorGenetics = colorGenetics.__dict__
    colorString = GetColorString(colorGenetics)
    context = {'dog':dog, 'colorString': colorString, 'litters':litters}
    return render(request, 'dogs/dog.html', context)

def litter(request, litter_id):
    puppies = Dog.objects.filter(litter=litter_id)
    samplePuppy = puppies.first()
    dam = samplePuppy.dam
    sire = samplePuppy.sire
    litter = Litter.objects.get(id=litter_id)
    breeder = litter.breeder
    context = {'puppies':puppies, 'sire':sire, 'dam':dam, 'breeder':breeder}

    return render(request, 'dogs/litter.html', context)

@login_required
def breedDogs(request):
    #femaleDogs = Dog.objects.filter(sex="F")
    #maleDogs = Dog.objects.filter(sex="M")
    #context = {'maleDogs':maleDogs, 'femaleDogs': femaleDogs}
    if request.method != 'POST':
        form = BreedDogForm(user=request.user)
    else:
        form = BreedDogForm(data=request.POST, user=request.user)
        if form.is_valid():
            sire = request.POST.get('sire')
            dam = request.POST.get('dam')
            #newDog = form.save(commit=False)
            #form.save()
            return redirect('dogs_app:view-litter', sire_id=sire, dam_id=dam)
    return render(request, 'dogs/breed-dogs.html', {"form":form})


def breedingResults(request, sire_id, dam_id):
    litter = Litter.objects.create(breeder_id = request.user.id)
    sire = Dog.objects.get(id=sire_id)
    dam = Dog.objects.get(id=dam_id)
    sireDict = generateDogDict(sire)
    damDict = generateDogDict(dam)
    breedDict = getPumiDict()
    puppyList = breedDogsScript.breedDogs(damDict, sireDict, breedDict)
    for puppy in puppyList:
        puppyGenetics = puppy['genetics']['colorGenetics']
        puppyObj = Dog.objects.create(name=puppy['name'], owner=request.user, sire=sire, dam=dam, sex=puppy['sex'], color=puppy["color"],litter=litter)
        colorObj = ColorGenetics.objects.create(dog=puppyObj, kAlele=puppyGenetics['k'], aAlele=puppyGenetics['a'], eAlele=puppyGenetics['e'], bAlele=puppyGenetics['b'], dAlele=puppyGenetics['d'], sAlele=puppyGenetics['s'], mAlele=puppyGenetics['m'])
    context = {'sire':sire, 'dam':dam, 'puppyList': puppyList}
    return render(request, 'dogs/litter.html', context)

def GetColorDict(colorGenetics):
    colorDict = {}
    colorDict["k"] = colorGenetics.kAlele
    colorDict["a"]  = colorGenetics.aAlele
    colorDict["e"]  = colorGenetics.eAlele
    colorDict["b"]  = colorGenetics.bAlele
    colorDict["d"]  = colorGenetics.dAlele
    colorDict["s"]  = colorGenetics.sAlele
    colorDict["m"]  = colorGenetics.mAlele
    return colorDict

def GetColorString(colorGenetics):
    colorString = ""
    colorString += colorGenetics['kAlele'] + " "
    colorString += colorGenetics['aAlele'] + " " 
    colorString += colorGenetics['eAlele'] + " "
    colorString += colorGenetics['bAlele'] + " "
    colorString += colorGenetics['dAlele'] + " "
    colorString += colorGenetics['sAlele'] + " "
    colorString += colorGenetics['mAlele'] 
    return colorString

def generateDogDict(dog):
    dogDict = {}
    owner = dog.owner
    kennel = Kennel.objects.filter(owner=owner).first()
    genetics = ColorGenetics.objects.filter(dog=dog).first()
    dogDict['name'] = dog.name
    dogDict['kennel'] = kennel.name
    dogDict['sex'] = dog.sex
    dogDict['breed'] = "Pumi"
    dogDict['color'] = dog.color
    dogDict['genetics'] = {'colorGenetics': GetColorDict(genetics), 'traitGenetics': None}
    return dogDict;

def getPumiDict ():
    pumiDict = {
            "model": "hightrial.breed",
            "pk": 1,
            "fields": {
                "breedName": "Pumi",
                "litterMin": 2,
                "litterMax": 8,
                "colorGeneticFlags": {
                    "k": {
                        "KB": 45,
                        "ky": 50,
                        "kbr": 5
                    },
                    "a": {
                        "ay": 40,
                        "at": 50,
                        "a": 10
                    },
                    "e": {
                        "e": 20,
                        "E": 75,
                        "Em": 5
                    },
                    "b": {
                        "B": 80,
                        "b": 20
                    },
                    "d": {
                        "D": 90,
                        "d": 10
                    }
                },
                "traitGeneticFlags": None,
                "nonFoundations": {
                    "k": [
                        "kbr/kbr",
                        "kbr/ky"
                    ],
                    "b": [
                        "b/b"
                    ],
                    "d": [
                        "d/d"
                    ],
                    "joint": {
                        "k/a": {
                            "ky/ky": [
                                "at/at",
                                "a/at",
                                "at/ay"
                            ]
                        }
                    }
                },
                "phenotypeNames": {
                    "k": {
                        "ky": "seeA",
                        "kbr": "Brindle"
                    },
                    "a": {
                        "ay": "Sable",
                        "at": "Tan Points",
                        "a": "Black"
                    },
                    "e": {
                        "e": "White",
                        "Em": "Masked"
                    },
                    "b": {
                        "B": "Grey",
                        "b": "Brown"
                    },
                    "d": {
                        "D": "Grey",
                        "d": "Grey-born"
                    },
                    "m":{
                        "M": None
                    },
                    "s":{
                        "Sp": None
                    },
                    "joints": {
                        "b/d": "Lilac"
                    }
                },
                "dominanceValues": {
                    "k": [
                        "KB",
                        "kbr",
                        "ky"
                    ],
                    "a": [
                        "at",
                        "ay",
                        "a"
                    ],
                    "e": [
                        "E",
                        "Em",
                        "e"
                    ],
                    "b": [
                        "B",
                        "b"
                    ],
                    "d": [
                        "D",
                        "d"
                    ],
                    "s" : [
                        "S",
                        "sp",
                        "s"
                    ],
                    "m" : [
                        "M",
                        "m"
                    ]
                }
            }
        }
    return pumiDict