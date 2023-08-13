from django import forms

from app.models import Family, Details

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name', 'birth_date', 'phone']
    
    def clean(self):
        data = self.cleaned_data
        name = data.get("name")
        qs = Family.objects.filter(name__icontains=name)
        if qs.exists():
            self.add_error("name", f"\"{name}\" is already in use. Please pick up another name")
        return data

class FamilyUpdateForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name', 'birth_date', 'phone']


class FamilyDetialsForm(forms.ModelForm):
    class Meta:
        model = Details
        fields = ['car', 'education']


# class FamilyForm(forms.Form):
#     name = forms.CharField()
#     birth_date = forms.DateField()
#     phone = forms.CharField()