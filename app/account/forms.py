from django import forms
from village.models import Village
from account.models import Midwife, Cadre
from posyandu.models import Posyandu


class AssignVillageToMidwifeForm(forms.ModelForm):
    villages = forms.ModelMultipleChoiceField(
        queryset=Village.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control selectpicker", "data-live-search": "true"}
        ),
        required=False,
    )

    class Meta:
        model = Midwife
        fields = []  # Fields dari Midwife yang ingin diubah, jika ada.

    def save(self, commit=True):
        midwife = self.instance
        midwife.villages.set(self.cleaned_data["villages"])  # Update Many-to-Many
        if commit:
            midwife.save()
        return midwife


class AssignPosyanduToCadreForm(forms.ModelForm):
    cadre_posyandus = forms.ModelMultipleChoiceField(
        queryset=Posyandu.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control selectpicker", "data-live-search": "true"}
        ),
        required=False,
    )

    class Meta:
        model = Cadre
        fields = []  # Fields dari Cadre yang ingin diubah, jika ada.

    def save(self, commit=True):
        cadre = self.instance
        cadre.cadre_posyandus.set(
            self.cleaned_data["cadre_posyandus"]
        )  # Update Many-to-Many
        if commit:
            cadre.save()
        return cadre
