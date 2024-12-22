#  so as we are creating room, so the value of from should be the rooms parameter's values
from .models import Room
from django.forms import ModelForm


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

# fields all : i am taking all the fields ( params ) of the class ROOM model like the hsot , etc etc, in future i can excute and take the specified like [' name',' topic'] etc
