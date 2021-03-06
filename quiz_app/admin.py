from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(MCQOptions)
admin.site.register(FillInTheBlank)
admin.site.register(Progress)
admin.site.register(StudentQuestion)
# Register your models here.
