from django.forms import ModelForm
from base.models import qubeCommunityRoom


class RoomForm(ModelForm):
    class Meta:
        model = qubeCommunityRoom
        fields = '__all__'
