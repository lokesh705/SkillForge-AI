from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    bio = models.TextField(
        blank=True
    )

    education = models.CharField(
        max_length=200,
        blank=True
    )

    college = models.CharField(
        max_length=200,
        blank=True
    )

    graduation_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    career_goal = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.user.username


class Skill(models.Model):

    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

    LEVEL_CHOICES = [
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    name = models.CharField(
        max_length=100
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default=BEGINNER
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.level}"


class CareerGoal(models.Model):

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    required_skills = models.TextField(
        help_text="Enter skills separated by commas."
    )

    def __str__(self):
        return self.title


class Project(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    technologies = models.CharField(
        max_length=300
    )

    github_url = models.URLField(
        blank=True
    )

    live_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Certification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="certifications"
    )

    name = models.CharField(
        max_length=200
    )

    organization = models.CharField(
        max_length=200
    )

    issue_date = models.DateField(
        null=True,
        blank=True
    )

    certificate_url = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.name


class LearningItem(models.Model):

    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

    STATUS_CHOICES = [
        (NOT_STARTED, "Not Started"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="learning_items"
    )

    skill_name = models.CharField(
        max_length=150
    )

    topic = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    resource_url = models.URLField(
        blank=True
    )

    estimated_hours = models.PositiveIntegerField(
        default=1
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NOT_STARTED
    )

    progress = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.skill_name} - {self.progress}%"