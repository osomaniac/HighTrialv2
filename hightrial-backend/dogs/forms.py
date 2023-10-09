from django import forms

from .models import Dog

class BreedDogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ('sire', 'dam')
        #maleDogs = forms.ModelChoiceField(label="Male Dogs", queryset=Dog.objects.filter(owner=this.owner, sex="M"))
        name = forms.CharField()
        date = forms.DateInput()

        #males = forms.ModelMultipleChoiceField(queryset=None)
        #females = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        #self.request = kwargs.pop('request')
        self.user = user;
        super(BreedDogForm, self).__init__(*args, **kwargs)
        self.fields['sire'].queryset = Dog.objects.filter(owner=self.user, sex="M")
        self.fields['dam'].queryset = Dog.objects.filter(owner=self.user, sex="F")