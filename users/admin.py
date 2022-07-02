from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Country, Department, TypeEvent, Position, Event, RolesEvent


#for form inline ManyToMany Member
class RolesEventMemberInLine(admin.TabularInline):
    model = RolesEvent
    extra = 1
    list_display = ('member_event','user_type','hourse_work', )
    fieldsets = (
        (None, {'fields': ('member_event','user_type','hourse_work',)}),)

#for form inline ManyToMany prepare
class RolesEventPrepareInLine(admin.TabularInline):
    model = RolesEvent
    extra = 1
    list_display = ('member_event','user_type','hourse_work', )
    fieldsets = (
        (None, {'fields': ('member_event','user_type','hourse_work',)}),)



@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = ('email','first_name','last_name', 'position', 'is_staff', 'is_active','image_tag','country','department',)
    list_filter = ('email', 'is_active',)
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {'fields': ('image_tag','first_name','last_name','email','position','country','department','doctor','rescuer_kkp','category_b_driver','aut_to_drive_emergency_vehicles','aut_to_drive_foundation_vehicles','camp_counselor','maltese_instructor')}),
        ('Permissions and password', {'fields': ('password','is_staff', 'is_active', )}),
    )
    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('first_name','email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    inlines = [RolesEventMemberInLine]
    inlines = [RolesEventPrepareInLine]


    #list_display = ['event',]
    #readonly_fields=('department',)
    

    # def has_delete_permission(self, request, obj=None):
    #     return False

@admin.register(Position)
class CommentAdmin(admin.ModelAdmin):
    model = Position


    #list_display = ('position_name',)
    #readonly_fields=('position_name',)
    # def has_delete_permission(self, request, obj=None):
    #     return False

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ('country',)


    #readonly_fields=('country',)
    # def has_delete_permission(self, request, obj=None):
    #     return False

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = ('department',)


    #readonly_fields=('department',)
    # def has_delete_permission(self, request, obj=None):
    #     return False

@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    model = TypeEvent


    # list_display = ('types',
    # 'added_by',)
    # fieldsets = ((None, {'fields': ('types',)})),
    # def has_delete_permission(self, request, obj=None):
    #     return False
    

    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         obj.added_by = request.user
    #     super().save_model(request, obj, form, change)


    #list_display = ('user_type', 'hourse_work')
    #readonly_fields=('department',)

    # def has_delete_permission(self, request, obj=None):
    #     return False

