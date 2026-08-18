from django.contrib import admin
from .models import (
    Profile,
    Skill,
    CareerGoal,
    Project,
    Certification,
    LearningItem,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'college',
        'graduation_year',
        'career_goal',
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'level',
        'created_at',
    )

    list_filter = (
        'level',
    )

    search_fields = (
        'name',
        'user__username',
    )


@admin.register(CareerGoal)
class CareerGoalAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
    )

    search_fields = (
        'title',
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'technologies',
        'created_at',
    )

    search_fields = (
        'title',
        'technologies',
        'user__username',
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'organization',
        'user',
        'issue_date',
    )

    search_fields = (
        'name',
        'organization',
        'user__username',
    )


@admin.register(LearningItem)
class LearningItemAdmin(admin.ModelAdmin):
    list_display = (
        'skill_name',
        'user',
        'status',
        'progress',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'skill_name',
        'user__username',
    )