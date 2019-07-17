from django.contrib import admin
from .models import Alumno, QuestionColb,  OptionColb, TestColb, \
                    OptionCard, ParCard, TestCard

# Register your models here.
admin.site.register(Alumno)
admin.site.register(QuestionColb)
admin.site.register(OptionColb)
admin.site.register(TestColb)
admin.site.register(OptionCard)
admin.site.register(ParCard)
admin.site.register(TestCard)