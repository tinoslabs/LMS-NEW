from django.contrib import admin
from .models import Level

# Register your models here.

from.models import Teacher_ProfilePermission,Teacher,Course,VideoModels,UserCourses,Categories,CourseResource

admin.site.register(Teacher_ProfilePermission) 
admin.site.register(Teacher) 
admin.site.register(Level)
admin.site.register(Course)
admin.site.register(VideoModels)
admin.site.register(UserCourses)
admin.site.register(Categories)
admin.site.register(CourseResource)