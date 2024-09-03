from django.contrib import admin

from student.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Tutorial)
admin.site.register(Topic)
admin.site.register(Attachments)
admin.site.register(MyTutorial)
admin.site.register(Cat)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Response)
admin.site.register(CatSubmit)