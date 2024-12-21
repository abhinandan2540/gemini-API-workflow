from django.contrib import admin
from .models import TextModelHistory, ImageModelHistory, interactiveChatHistory, QubeVisionImgHistory, QubeVideoModelHistory
from .models import QubeAudioModelHistory, QubeCodeModelHistory
from .models import qubeCommunityTopic, qubeCommunityRoom, qubeCommunityMessage


admin.site.register(TextModelHistory),
admin.site.register(ImageModelHistory),
admin.site.register(interactiveChatHistory)
admin.site.register(QubeVisionImgHistory)
admin.site.register(QubeVideoModelHistory)
admin.site.register(QubeAudioModelHistory)
admin.site.register(QubeCodeModelHistory)
admin.site.register(qubeCommunityRoom)
admin.site.register(qubeCommunityTopic)
admin.site.register(qubeCommunityMessage)