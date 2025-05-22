from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import  Teacher,Teacher_ProfilePermission,Categories,Lesson,Instructor,Levels,Language,Course,VideoModel,UserCourses,CourseResource,What_u_learn,Requirements,VideoModels,Quiz,QuizResult,Certificate
from adminapp.models import Account
from .forms import Teacher_ProfilePermissionForm,CategoryForm,InstructorForm,LevelForm,LanguageForm,CourseForm,LessonForm,CourseResourceForm,WhatULearnForm,RequirementsForm,VideosForm,QuizForm,QuestionForm
from django.contrib.auth.decorators import login_required
from .decorators import allowed_roles
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models.expressions import Case, Func, Star, Value, When
from django.core.exceptions import FieldError, FullResultSet
from django.db.models.functions.mixins import (
    FixDurationInputMixin,
    NumericOutputFieldMixin,
)
from .models import Teacher, Teacher_ProfilePermission
from teacher.models import UserCourses, Course
from django.db.models import Count



def assign_teacher_permissions(request, user_id):
    account = get_object_or_404(Account, id=user_id)  
    teacher = get_object_or_404(Teacher, user=account)

    if request.method == "POST":
        form = Teacher_ProfilePermissionForm (request.POST)
        if form.is_valid():
            permissions, created = Teacher_ProfilePermission.objects.get_or_create(teacher=teacher)
            
            
            permissions.can_manage = form.cleaned_data['can_manage']
            permissions.can_create = form.cleaned_data['can_create']
            permissions.can_edit = form.cleaned_data['can_edit']
            permissions.can_delete = form.cleaned_data['can_delete']
        
            permissions.manage_categories = form.cleaned_data['manage_categories']
            permissions.create_categories = form.cleaned_data['create_categories']
            permissions.edit_categories = form.cleaned_data['edit_categories']
            permissions.delete_categories = form.cleaned_data['delete_categories']
            
            permissions.manage_Instructor = form.cleaned_data['manage_Instructor']
            permissions.create_Instructor = form.cleaned_data['create_Instructor']
            permissions.edit_Instructor = form.cleaned_data['edit_Instructor']
            permissions.delete_Instructor = form.cleaned_data['delete_Instructor']
            
            permissions.manage_Levels = form.cleaned_data['manage_Levels']
            permissions.create_Levels = form.cleaned_data['create_Levels']
            permissions.edit_Levels = form.cleaned_data['edit_Levels']
            permissions.delete_Levels = form.cleaned_data['delete_Levels']
            
            permissions.manage_Language = form.cleaned_data['manage_Language']
            permissions.create_Language = form.cleaned_data['create_Language']
            permissions.edit_Language = form.cleaned_data['edit_Language']
            permissions.delete_Language = form.cleaned_data['delete_Language']
            
            permissions.manage_Course = form.cleaned_data['manage_Course']
            permissions.create_Course = form.cleaned_data['create_Course']
            permissions.edit_Course = form.cleaned_data['edit_Course']
            permissions.delete_Course = form.cleaned_data['delete_Course']
            
            permissions.manage_Lesson = form.cleaned_data['manage_Lesson']
            permissions.create_Lesson = form.cleaned_data['create_Lesson']
            permissions.edit_Lesson = form.cleaned_data['edit_Lesson']
            permissions.delete_Lesson = form.cleaned_data['delete_Lesson']
            
            permissions.manage_CourseResource = form.cleaned_data['manage_CourseResource']
            permissions.create_CourseResource = form.cleaned_data['create_CourseResource']
            permissions.edit_CourseResource = form.cleaned_data['edit_CourseResource']
            permissions.delete_CourseResource = form.cleaned_data['delete_CourseResource']
            
            permissions.manage_What_u_learn = form.cleaned_data['manage_What_u_learn']
            permissions.create_What_u_learn = form.cleaned_data['create_What_u_learn']
            permissions.edit_What_u_learn = form.cleaned_data['edit_What_u_learn']
            permissions.delete_What_u_learn = form.cleaned_data['delete_What_u_learn']
            
            permissions.manage_Requirements = form.cleaned_data['manage_Requirements']
            permissions.create_Requirements = form.cleaned_data['create_Requirements']
            permissions.edit_Requirements = form.cleaned_data['edit_Requirements']
            permissions.delete_Requirements = form.cleaned_data['delete_Requirements']
            
            permissions.manage_VideoModels = form.cleaned_data['manage_VideoModels']
            permissions.create_VideoModels = form.cleaned_data['create_VideoModels']
            permissions.edit_VideoModels = form.cleaned_data['edit_VideoModels']
            permissions.delete_VideoModels = form.cleaned_data['delete_VideoModels']
            
            permissions.manage_Quiz = form.cleaned_data['manage_Quiz']
            permissions.create_Quiz = form.cleaned_data['create_Quiz']
            permissions.edit_Quiz = form.cleaned_data['edit_Quiz']
            permissions.delete_Quiz = form.cleaned_data['delete_Quiz']

            permissions.save()

            messages.success(request, f"Permissions assigned successfully to {account.first_name} {account.last_name}.")
            return redirect('teacher_success_page', user_id=user_id)  # Redirect to teacher success page
        else:
            messages.error(request, "Failed to assign permissions. Please check the form.")
    else:
        existing_permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
        form = Teacher_ProfilePermissionForm (instance=existing_permissions)

    return render(request, 'teacher/teacher_roles_form.html', {'form': form, 'user': teacher})



def teacher_success(request, user_id=None):
    teacher = None
    permissions = None

    if user_id:
        account = get_object_or_404(Account, id=user_id)
        teacher = get_object_or_404(Teacher, user=account)
        permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()

    return render(request, 'teacher/assign_permisssion.html', {
        'teacher': teacher,
        'permissions': permissions
    })



def edit_teacher_permissions(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    modules = ['Category', 'Instructor', 'Level', 'Language', 'Course', 'Lesson', 'Course Resource', 'Learning Point', 'Requirement', 'Video', 'Quiz']

    if request.method == 'POST':
        for module in modules:
            # Check if permission already exists, else create new
            permission_obj, created = Teacher_ProfilePermission.objects.get_or_create(teacher=teacher)

            # Update permissions based on checkbox values
            permission_obj.can_manage = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.can_create = request.POST.get(f'{module}_create') == 'on'
            permission_obj.can_edit = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.can_delete = request.POST.get(f'{module}_delete') == 'on'
            
            permission_obj.manage_categories = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_categories = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_categories = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_categories = request.POST.get(f'{module}_delete') == 'on'
            
            
            permission_obj.manage_Instructor = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_Instructor = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_Instructor = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_Instructor = request.POST.get(f'{module}_delete') == 'on'
            
            #_Levels
            permission_obj.manage_Levels = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_Levels = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_Levels = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_Levels = request.POST.get(f'{module}_delete') == 'on'
            
            #_Language 
            permission_obj.manage_Language  = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_Language  = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_Language  = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_Levels = request.POST.get(f'{module}_delete') == 'on'
            
            #_Course
            permission_obj.manage_Course  = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_Course = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_Course  = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_Course = request.POST.get(f'{module}_delete') == 'on'
            
            #_Lesson
            permission_obj.manage_Lesson = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_Lesson = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_Lesson  = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_Lesson = request.POST.get(f'{module}_delete') == 'on'
            
            #_CourseResource
            permission_obj.manage_CourseResource = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_CourseResource = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_CourseResource  = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_CourseResource = request.POST.get(f'{module}_delete') == 'on'
            
            #CourseResource
            permission_obj.manage_CourseResource = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_CourseResource = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_CourseResource  = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_CourseResource = request.POST.get(f'{module}_delete') == 'on'
            
            #_What_u_learn
            permission_obj.manage_What_u_learn = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_What_u_learn = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_What_u_learn  = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_What_u_learn = request.POST.get(f'{module}_delete') == 'on'
            
            #_What_u_learn
            permission_obj.manage_What_u_learn = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_What_u_learn = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_What_u_learn  = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_What_u_learn = request.POST.get(f'{module}_delete') == 'on'
            
            #_Requirements
            permission_obj.manage_Requirements = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_Requirements = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_Requirements  = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_Requirements = request.POST.get(f'{module}_delete') == 'on'
            
            #_VideoModels 
            permission_obj.manage_VideoModels  = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_VideoModels  = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_VideoModels   = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_VideoModels  = request.POST.get(f'{module}_delete') == 'on'
            
            #_Quiz 
            permission_obj.manage_Quiz   = request.POST.get(f'{module}_manage') == 'on'
            permission_obj.create_Quiz   = request.POST.get(f'{module}_create') == 'on'
            permission_obj.edit_Quiz    = request.POST.get(f'{module}_edit') == 'on'
            permission_obj.delete_Quiz   = request.POST.get(f'{module}_delete') == 'on'
            
            
            
            permission_obj.save()

        return redirect('teacher_list')  # Or your redirect URL

    # Prepare existing permissions for the form
    # permissions = {}
    # for module in modules:
    permissions= Teacher_ProfilePermission.objects.filter(teacher=teacher).first()

    context = {
        'teacher': teacher,
        'modules': modules,
        'permissions': permissions,
    }
    return render(request, 'teacher/edit_teacher_permissions.html', context)


@login_required
def profile_edit(request):
    user = request.user

    # Get the teacher object for the logged-in user
    teacher = get_object_or_404(Teacher, user=user)
    # Get the teacher's permissions
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()

    # Check edit permission
    if not permissions or not permissions.can_edit:
        messages.error(request, "You do not have permission to edit this profile.")
        return redirect('profile_view')

    if request.method == 'POST':
        # Update fields
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)

        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('teacher_profile_edit')

    return render(request, 'teacher/teacher_profile.html', {'user': user})


@login_required
def profile_delete(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.can_delete:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')

    if request.method == "POST":
        # Check if the confirmation checkbox is checked
        if 'confirm_delete' in request.POST:
            user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('register')  # Redirect to home or login page
        else:
            messages.error(request, "Please confirm the deletion before proceeding.")
            return redirect('profile_view')

    return render(request, 'confirm_delete.html', {'user': user})


#category

@login_required
@allowed_roles(['admin_and_instructor'])
def add_category(request):
    
    user = request.user
    
    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_categories:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            category, created = Categories.objects.get_or_create(
                name=form.cleaned_data['name'],
                defaults={'icon': form.cleaned_data['icon']}
            )
            if created:
                messages.success(request, "Category added successfully!")
            else:
                messages.info(request, "Category already exists.")
            return redirect('category_list')
    else:
        form = CategoryForm()
        if request.user.roles == 'Teacher':
            template_name = 'teacher/category/add_category.html'
        else:
            template_name = 'admin/add_category.html'
            
    return render(request, template_name, {'form': form})



@login_required
@allowed_roles(['admin_and_instructor'])   #for restricting student
def category_list(request):
    user = request.user
    
    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_categories:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    categories = Categories.objects.all()
    if request.user.roles == 'Teacher':
        template_name = 'teacher/category/category_list.html'
    else:
        template_name = 'admin/category_list.html'
    
    return render(request, template_name, {'categories': categories})


@login_required
@allowed_roles(['admin_and_instructor'])
def update_category(request, category_id):
    category = get_object_or_404(Categories, id=category_id)  # Fetch the category object
    
    user = request.user
    
    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_categories:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        # Initialize the form with POST data, FILES, and bind it to the category instance
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()  # Save the updated data to the database
            messages.success(request, "Category updated successfully!")
            return redirect('category_list')
    else:
        # Pre-fill the form with the current category instance
        form = CategoryForm(instance=category)
        if request.user.roles == 'Teacher':
            template_name = 'teacher/category/update_category.html'
        else:
            template_name = 'admin/update_category.html'
    return render(request, template_name, {'form': form, 'category': category})


def delete_category(request, category_id):
        
    user = request.user
    
    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_categories:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    category = get_object_or_404(Categories, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('category_list')


# create_instructor


@login_required
def create_instructor(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_Instructor:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        # Check if the logged-in user already has an Instructor profile
        if Instructor.objects.filter(user=request.user).exists():
            messages.error(request, "You already have an instructor profile.")
            return redirect('create_instructor')  # Replace with your desired page

        form = InstructorForm(request.POST, request.FILES)
        if form.is_valid():
            instructor = form.save(commit=False)
            instructor.user = request.user 
            instructor.save()
            messages.success(request, "Instructor profile created successfully!")
            return redirect('InstructorListView') 
        else:
            messages.error(request, "Please correct the errors below.")
            return redirect('create_instructor')
    else:
        form = InstructorForm()

    return render(request, 'teacher/instructor/teacher_form.html', {'form': form})

class InstructorListView(LoginRequiredMixin, ListView):
    
    model = Instructor
    template_name = 'teacher/instructor/teacher_details.html'
    context_object_name = 'instructor'
    paginate_by = 10

    def get_queryset(self):
        # Filter instructors based on the logged-in user
        return Instructor.objects.filter(user=self.request.user)
    
    
@login_required
def update_instructor(request):
    # Fetch the instructor profile of the logged-in user
    instructor = get_object_or_404(Instructor, user=request.user)
    
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_Instructor:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')

    if request.method == 'POST':
        form = InstructorForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor profile updated successfully!")
            return redirect('InstructorListView')  # Replace with your desired page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InstructorForm(instance=instructor)

    return render(request, 'teacher/instructor/update_teacher.html', {'form': form})


@login_required
def delete_instructor(request):
    # Fetch the instructor profile of the logged-in user
    instructor = get_object_or_404(Instructor, user=request.user)
    
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_Instructor:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    instructor.delete()
    messages.success(request, "Instructor profile deleted successfully!")
    return redirect('InstructorListView')  # Replace with your desired page



#level


def level_list(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_Levels:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    levels = Levels.objects.all()
    return render(request, 'teacher/level/level_list.html', {'levels': levels})

# Add new Level
def add_level(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_Levels:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == "POST":
        form = LevelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('level_list')
    else:
        form = LevelForm()
    return render(request, 'teacher/level/add_level.html', {'form': form})


# Update Level
def update_level(request, pk):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_Levels:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    level = get_object_or_404(Levels, pk=pk)
    if request.method == "POST":
        form = LevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            return redirect('level_list')
    else:
        form = LevelForm(instance=level)
    return render(request, 'teacher/level/update_level.html', {'form': form})


def delete_level(request, pk):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_Levels:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    level = get_object_or_404(Levels, pk=pk)
    level.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('level_list')


# Add new Level
@login_required
def add_language(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_Language:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('language_list')
    else:
        form = LanguageForm()
    return render(request, 'teacher/language/add_language.html', {'form': form})



def language_list(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_Language:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    language = Language.objects.all()
    return render(request, 'teacher/language/language_list.html', {'language': language})


def update_language(request, pk):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_Language:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    language = get_object_or_404(Language, pk=pk)
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            return redirect('language_list')
    else:
        form = LanguageForm(instance=language)
    return render(request, 'teacher/language/update_language.html', {'form': form})


def delete_language(request, pk):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_Language:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    level = get_object_or_404(Language, pk=pk)
    level.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('language_list')
# END LANGUAGE 






# START COURSE

class Coalesce(Func):
    """Return, from left to right, the first non-null expression."""

    function = "COALESCE"

    def __init__(self, *expressions, **extra):
        if len(expressions) < 2:
            raise ValueError("Coalesce must take at least two expressions")
        super().__init__(*expressions, **extra)

    @property
    def empty_result_set_value(self):
        for expression in self.get_source_expressions():
            result = expression.empty_result_set_value
            if result is NotImplemented or result is not None:
                return result
        return None

    def as_oracle(self, compiler, connection, **extra_context):
        # Oracle prohibits mixing TextField (NCLOB) and CharField (NVARCHAR2),
        # so convert all fields to NCLOB when that type is expected.
        if self.output_field.get_internal_type() == "TextField":
            clone = self.copy()
            clone.set_source_expressions(
                [
                    Func(expression, function="TO_NCLOB")
                    for expression in self.get_source_expressions()
                ]
            )
            return super(Coalesce, clone).as_sql(compiler, connection, **extra_context)
        return self.as_sql(compiler, connection, **extra_context)


class Aggregate(Func):
    template = "%(function)s(%(distinct)s%(expressions)s)"
    contains_aggregate = True
    name = None
    filter_template = "%s FILTER (WHERE %%(filter)s)"
    window_compatible = True
    allow_distinct = False
    empty_result_set_value = None

    def __init__(
        self, *expressions, distinct=False, filter=None, default=None, **extra
    ):
        if distinct and not self.allow_distinct:
            raise TypeError("%s does not allow distinct." % self.__class__.__name__)
        if default is not None and self.empty_result_set_value is not None:
            raise TypeError(f"{self.__class__.__name__} does not allow default.")
        self.distinct = distinct
        self.filter = filter
        self.default = default
        super().__init__(*expressions, **extra)

    def get_source_fields(self):
        # Don't return the filter expression since it's not a source field.
        return [e._output_field_or_none for e in super().get_source_expressions()]

    def get_source_expressions(self):
        source_expressions = super().get_source_expressions()
        if self.filter:
            return source_expressions + [self.filter]
        return source_expressions

    def set_source_expressions(self, exprs):
        self.filter = self.filter and exprs.pop()
        return super().set_source_expressions(exprs)

    def resolve_expression(
        self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False
    ):
        # Aggregates are not allowed in UPDATE queries, so ignore for_save
        c = super().resolve_expression(query, allow_joins, reuse, summarize)
        c.filter = c.filter and c.filter.resolve_expression(
            query, allow_joins, reuse, summarize
        )
        if summarize:
            # Summarized aggregates cannot refer to summarized aggregates.
            for ref in c.get_refs():
                if query.annotations[ref].is_summary:
                    raise FieldError(
                        f"Cannot compute {c.name}('{ref}'): '{ref}' is an aggregate"
                    )
        elif not self.is_summary:
            # Call Aggregate.get_source_expressions() to avoid
            # returning self.filter and including that in this loop.
            expressions = super(Aggregate, c).get_source_expressions()
            for index, expr in enumerate(expressions):
                if expr.contains_aggregate:
                    before_resolved = self.get_source_expressions()[index]
                    name = (
                        before_resolved.name
                        if hasattr(before_resolved, "name")
                        else repr(before_resolved)
                    )
                    raise FieldError(
                        "Cannot compute %s('%s'): '%s' is an aggregate"
                        % (c.name, name, name)
                    )
        if (default := c.default) is None:
            return c
        if hasattr(default, "resolve_expression"):
            default = default.resolve_expression(query, allow_joins, reuse, summarize)
            if default._output_field_or_none is None:
                default.output_field = c._output_field_or_none
        else:
            default = Value(default, c._output_field_or_none)
        c.default = None  # Reset the default argument before wrapping.
        coalesce = Coalesce(c, default, output_field=c._output_field_or_none)
        coalesce.is_summary = c.is_summary
        return coalesce

    @property
    def default_alias(self):
        expressions = self.get_source_expressions()
        if len(expressions) == 1 and hasattr(expressions[0], "name"):
            return "%s__%s" % (expressions[0].name, self.name.lower())
        raise TypeError("Complex expressions require an alias")

    def get_group_by_cols(self):
        return []

    def as_sql(self, compiler, connection, **extra_context):
        extra_context["distinct"] = "DISTINCT " if self.distinct else ""
        if self.filter:
            if connection.features.supports_aggregate_filter_clause:
                try:
                    filter_sql, filter_params = self.filter.as_sql(compiler, connection)
                except FullResultSet:
                    pass
                else:
                    template = self.filter_template % extra_context.get(
                        "template", self.template
                    )
                    sql, params = super().as_sql(
                        compiler,
                        connection,
                        template=template,
                        filter=filter_sql,
                        **extra_context,
                    )
                    return sql, (*params, *filter_params)
            else:
                copy = self.copy()
                copy.filter = None
                source_expressions = copy.get_source_expressions()
                condition = When(self.filter, then=source_expressions[0])
                copy.set_source_expressions([Case(condition)] + source_expressions[1:])
                return super(Aggregate, copy).as_sql(
                    compiler, connection, **extra_context
                )
        return super().as_sql(compiler, connection, **extra_context)

    def _get_repr_options(self):
        options = super()._get_repr_options()
        if self.distinct:
            options["distinct"] = self.distinct
        if self.filter:
            options["filter"] = self.filter
        return options

@login_required
def add_course(request):
    
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_Course:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, user=request.user)  # Pass user to the form
        if form.is_valid():
            course = form.save(commit=False)
            instructor = Instructor.objects.filter(user=request.user).first()  # Fetch the current instructor
            if instructor:
                course.author = instructor
                course.save()
                messages.success(request, "Course added successfully!")
                return redirect('course_list')
            else:
                messages.error(request, "You are not an instructor. Please contact the admin.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CourseForm(user=request.user)  # Pass user to the form
    
    instructor = Instructor.objects.filter(user=request.user).first()
    return render(request, 'teacher/course/add_course.html', {'form': form, 'instructor': instructor})

@login_required
def course_list(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_Course:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    # Filter courses where the author is the currently logged-in user
    courses = Course.objects.filter(author__user=request.user)
    return render(request, 'teacher/course/course_list.html', {'courses': courses})

class Sum(FixDurationInputMixin, Aggregate):
    function = "SUM"
    name = "Sum"
    allow_distinct = True


def get_course_data(course_id, user=None):
    """
    
    Retrieves course details, lessons, and video progress. used in course_detail and WATCH_COURSE
    
    """
    course = get_object_or_404(Course, pk=course_id)
    course_time_duration = VideoModel.objects.filter(course=course).aggregate(sum=Sum('time_duration'))
    lessons = course.lesson_set.annotate(total_duration=Sum('videomodel__time_duration'))

    category = Categories.objects.all().order_by('id')[0:6] #category on nav bar 

    check_enroll = None
    

    if user and user.is_authenticated:
        check_enroll = UserCourses.objects.filter(user=user, course=course).first()
        
    return {
        'course': course,
        'course_time_duration': course_time_duration,
        'lessons': lessons,
        'check_enroll': check_enroll,
        'category':category
    }


def course_detail(request, course_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_Course:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    course_data = get_course_data(course_id, request.user)   # another function, place just above
    return render(request, 'teacher/course/course-details.html', course_data)

@login_required
def update_course(request, course_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_Course:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
        # print(course.author)
        # print(form)
    return render(request, 'teacher/course/update_coruse.html', {'form': form,'course':course})

@login_required
def delete_course(request, course_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_Course:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})




# Add a lesson
@login_required
def add_lesson(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_Lesson:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson added successfully!")
            return redirect('lesson_list')
    else:
        form = LessonForm(user = request.user)
    return render(request, 'teacher/lesson/add_lesson.html', {'form': form})

# Display all lessons
@login_required
def lesson_list(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_Lesson:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    try:
        auther = Instructor.objects.get( user = request.user)
        my_course = Course.objects.filter(author = auther)
        lessons = Lesson.objects.filter(course__in= my_course)
        return render(request, 'teacher/lesson/lesson_list.html', {'lessons': lessons})
    except:
        return render(request, 'teacher/lesson/lesson_list.html')
    

# Update a lesson
def update_lesson(request, lesson_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_Lesson:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated successfully!")
            return redirect('lesson_list')
    else:
        form = LessonForm(instance=lesson, user = request.user)
    return render(request, 'teacher/lesson/update_lesson.html', {'form': form})

# Delete a lesson
def delete_lesson(request, lesson_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_Lesson:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, "Lesson deleted successfully!")
    return redirect('lesson_list')


# START Course Resources
def add_course_resource(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_CourseResource:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        form = CourseResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource added successfully!")
            return redirect('resource_list')
    else:
        form = CourseResourceForm(user = request.user)
    return render(request, 'teacher/course_resource/add_resource.html', {'form': form})


def resource_list(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_CourseResource:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    try:
        auther = Instructor.objects.get( user = request.user)
        my_courses = Course.objects.filter(author = auther)
        resource = CourseResource.objects.filter(course__in= my_courses)
        context = {'resources' : resource}
    except:
        context = {'resources' : None}
    return render(request, 'teacher/course_resource/resource_list.html', context)

@login_required
def update_course_resource(request, resource_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_CourseResource:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    resource = get_object_or_404(CourseResource, id=resource_id)
    if request.method == 'POST':
        form = CourseResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource updated successfully!")
            return redirect('resource_list')
    else:
        form = CourseResourceForm(instance=resource, user = request.user)
    return render(request, 'teacher/course_resource/update_resource.html', {'form': form})

@login_required
def delete_course_resource(request, resource_id):
    
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_CourseResource:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    resource = get_object_or_404(CourseResource, id=resource_id)
    resource.delete()
    messages.success(request, "Resource deleted successfully!")
    return redirect('resource_list')



#what u learn

def add_what_u_learn(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_What_u_learn:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        form = WhatULearnForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Points learned added successfully!")
            return redirect('what_u_learn_list')
    else:
        form = WhatULearnForm()
    return render(request, 'teacher/what_u_learn/add_what_u_learn.html', {'form': form})


def what_u_learn_list(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_What_u_learn:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    what_u_learn_entries = What_u_learn.objects.all()
    return render(request, 'teacher/what_u_learn/what_u_learn_list.html', {'what_u_learn_entries': what_u_learn_entries})


def update_what_u_learn(request, entry_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_What_u_learn:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    entry = get_object_or_404(What_u_learn, id=entry_id)
    if request.method == 'POST':
        form = WhatULearnForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Points learned updated successfully!")
            return redirect('what_u_learn_list')
    else:
        form = WhatULearnForm(instance=entry)
    return render(request, 'teacher/what_u_learn/update_what_u_learn.html', {'form': form})


def delete_what_u_learn(request, entry_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_What_u_learn:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        entry = get_object_or_404(What_u_learn, id=entry_id)
        entry.delete()
        messages.success(request, "Points learned deleted successfully!")
    return redirect('what_u_learn_list')




def add_requirement(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_Requirements:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        form = RequirementsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Requirement added successfully!")
            return redirect('requirement_list')
    else:
        form = RequirementsForm(user = request.user)
    return render(request, 'teacher/requirement/add_requirement.html', {'form': form})

def requirement_list(request):
    
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_Requirements:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    try:
        auther = Instructor.objects.get( user = request.user)
        my_courses = Course.objects.filter(author = auther)
        requirement = Requirements.objects.filter(course__in= my_courses)
        context = {'requirements' : requirement}
    except:
        context = {'requirements' : None}
    return render(request, 'teacher/requirement/requirement_list.html', context)

def update_requirement(request, requirement_id):
    requirement = get_object_or_404(Requirements, id=requirement_id)
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_Requirements:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        form = RequirementsForm(request.POST, instance=requirement)
        if form.is_valid():
            form.save()
            messages.success(request, "Requirement updated successfully!")
            return redirect('requirement_list')
    else:
        form = RequirementsForm(instance=requirement, user = request.user)
    return render(request, 'teacher/requirement/update_requirement.html', {'form': form})

def delete_requirement(request, requirement_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_Requirements:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    requirement = get_object_or_404(Requirements, id=requirement_id)
    if request.method == 'POST':
        requirement.delete()
        messages.success(request, "Requirement deleted successfully!")
    return redirect('requirement_list')    




# Create a video
def create_video(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_VideoModels:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        form = VideosForm(request.POST, request.FILES,user=request.user )
        if form.is_valid():
            form.save()
            messages.success(request, "Video added successfully!")
            return redirect('view_video')
    else:
        print('video not added')
        form = VideosForm(user = request.user)
    return render(request, 'teacher/video/create_video.html', {'form': form})

# list a video
def view_video(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_VideoModels:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    try:
        auther = Instructor.objects.get( user = request.user)
        print("Instructor:", auther)
        my_course = Course.objects.filter(author = auther)
        print("Courses for instructor:", my_course)
        videos = VideoModels.objects.filter(course__in = my_course)
        print("Videos for courses:", videos)
        context = {'videos' : videos}
    except:
        context = {'videos' : None}
        print("No instructor found or error in fetching videos")
    return render(request, 'teacher/video/view_video.html', context)

# update a video
def video_update(request, video_id):
    video = get_object_or_404(VideoModels, id=video_id)
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_VideoModels:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        form = VideosForm(request.POST, request.FILES, instance=video,user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Video updated successfully!")
            return redirect('view_video')
    else:
        form = VideosForm(instance=video, user = request.user)
    return render(request, 'teacher/video/video_update.html', {'form': form})

# Delete a video
def delete_videos(request, video_id):
    video = get_object_or_404(VideoModels, id=video_id)
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_VideoModels:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        video.delete()
        messages.success(request, "Video deleted successfully!")
    return redirect('view_video')

#quez
def create_quiz(request):
    # course = get_object_or_404(Course, id=course_id)
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_Quiz:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save()  # Save the quiz instance
            return redirect('add_questions', quiz_id=quiz.id)  # Redirect to the page to add questions
    else:
        quiz_form = QuizForm(user = request.user)
    return render(request, 'teacher/quiz/create_quiz.html', {'quiz_form': quiz_form})


def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz,id=quiz_id)
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_Quiz:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, quiz=quiz)  # Pass quiz to the form
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz  # Explicitly set the quiz for the question
            question.save()
            return redirect('add_questions', quiz_id=quiz.id)  # Redirect to add another question or finish
    else:
        question_form = QuestionForm(initial={'quiz': quiz}, quiz=quiz)  # Pre-fill the quiz field and limit queryset    
    return render(request, 'teacher/quiz/add_questions.html', {'question_form': question_form, 'quiz': quiz})


def list_quiz(request):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_Quiz:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    try:
        auther = Instructor.objects.get( user = request.user)
        my_courses = Course.objects.filter(author = auther)
        quizzes = Quiz.objects.filter(course__in= my_courses)
        
        
        context = {'quizzes' : quizzes}
    except:
        context = {'quizzes' : None}
    
    
    return render(request, 'teacher/quiz/list_quiz.html', context)

def delete_quiz(request,quiz_id):
    
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.delete_Quiz:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    quiz = get_object_or_404(Quiz,id=quiz_id)
    quiz.delete()
    messages.success(request, "Quiz deleted successfully!")
    return redirect('list_quiz')

def edit_quiz(request,quiz_id):
    quiz = get_object_or_404(Quiz,id=quiz_id)
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.edit_Quiz:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance = quiz )
        if quiz_form.is_valid():
            quiz_form.save()
            messages.success(request, "Quiz edited successfully!")
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm( instance = quiz, user = request.user )
    return render(request, 'teacher/quiz/edit_quiz.html', {'quiz_form':quiz_form} )




def get_quiz_results_for_course(request, quiz_id):
    # Step 1: Get the quiz for the given course (assuming there's one quiz per course)
    quiz = get_object_or_404(Quiz, id=quiz_id) 
    
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.manage_Quiz:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    quiz_results = QuizResult.objects.filter(quiz=quiz).select_related('quiz')

    return render(request, 'teacher/quiz/quiz_results.html', {'quiz_results':quiz_results} )

def verify_result(request, quiz_result_id):
    user = request.user

    teacher = get_object_or_404(Teacher, user=user)
    permissions = Teacher_ProfilePermission.objects.filter(teacher=teacher).first()
    
    if not permissions or not permissions.create_Language:
        messages.error(request, "You do not have permission to delete this profile.")
        return redirect('profile_view')
    
    quiz_result = get_object_or_404(QuizResult, id=quiz_result_id)
    certificate_obj, created =  Certificate.objects.get_or_create(
                quiz_result = quiz_result,
                verified = True,
            )
    print('reached')
    return redirect('quiz_results', quiz_id = quiz_result.quiz.id)


def get_top_instructors():
    top_instructors = (
        Account.objects.filter(role='instructor')
        .annotate(course_count=Count('instructor__course'))
        .order_by('-course_count')[:4]
    )
    return top_instructors



