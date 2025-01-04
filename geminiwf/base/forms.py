#  so as we are creating room, so the value of from should be the rooms parameter's values
from .models import Room, qubePredictionModel
from django.forms import ModelForm


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name']

# fields all : i am taking all the fields ( params ) of the class ROOM model like the hsot , etc etc, in future i can excute and take the specified like [' name',' topic'] etc


class QubePredictionForm(ModelForm):
    class Meta:
        model = qubePredictionModel
        fields = ['user_text_prompt', 'user_prediction_model1',
                  'user_prediction_model2', 'user_input_file']
