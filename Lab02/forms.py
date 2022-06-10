from .models import Sportsman, City, Team, Trainer
from django.forms import DateField, DateInput, DateTimeInput, FloatField, IntegerField, ModelForm, TextInput, widgets


class SportsmanForm(ModelForm):
    class Meta:
        model = Sportsman
        fields = ["sportsman_name", "date_of_birth", "sex", "weight", "grade", "trainer", "team", "city"]
