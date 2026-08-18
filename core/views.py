from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import (
    Profile,
    Skill,
    CareerGoal,
    Project,
    Certification,
    LearningItem,
)


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(request, "home.html")


# =========================================================
# SIGNUP
# =========================================================

def signup_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not username or not email or not password:

            messages.error(
                request,
                "Please fill in all required fields."
            )

            return render(
                request,
                "signup.html"
            )

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "signup.html"
            )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return render(
                request,
                "signup.html"
            )

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "An account with this email already exists."
            )

            return render(
                request,
                "signup.html"
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. Please log in."
        )

        return redirect("login")

    return render(
        request,
        "signup.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("home")


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    skills_count = Skill.objects.filter(
        user=request.user
    ).count()

    learning_items_count = LearningItem.objects.filter(
        user=request.user
    ).count()

    completed_items_count = LearningItem.objects.filter(
        user=request.user,
        status=LearningItem.COMPLETED
    ).count()

    projects_count = Project.objects.filter(
        user=request.user
    ).count()

    certifications_count = Certification.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        "dashboard.html",
        {
            "profile": profile,
            "skills_count": skills_count,
            "learning_items_count": learning_items_count,
            "completed_items_count": completed_items_count,
            "projects_count": projects_count,
            "certifications_count": certifications_count,
        }
    )


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        profile.bio = request.POST.get(
            "bio",
            ""
        ).strip()

        profile.education = request.POST.get(
            "education",
            ""
        ).strip()

        profile.college = request.POST.get(
            "college",
            ""
        ).strip()

        profile.career_goal = request.POST.get(
            "career_goal",
            ""
        ).strip()

        graduation_year = request.POST.get(
            "graduation_year",
            ""
        ).strip()

        if graduation_year:

            try:

                profile.graduation_year = int(
                    graduation_year
                )

            except ValueError:

                messages.error(
                    request,
                    "Graduation year must be a valid number."
                )

                return render(
                    request,
                    "profile.html",
                    {
                        "profile": profile
                    }
                )

        else:

            profile.graduation_year = None

        profile.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )


# =========================================================
# SKILLS
# =========================================================

@login_required
def skills_view(request):

    skills = Skill.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "skills.html",
        {
            "skills": skills
        }
    )


@login_required
def add_skill_view(request):

    if request.method != "POST":
        return redirect("skills")

    name = request.POST.get(
        "name",
        ""
    ).strip()

    level = request.POST.get(
        "level",
        Skill.BEGINNER
    )

    if not name:

        messages.error(
            request,
            "Please enter a skill name."
        )

        return redirect("skills")

    valid_levels = [
        Skill.BEGINNER,
        Skill.INTERMEDIATE,
        Skill.ADVANCED,
    ]

    if level not in valid_levels:
        level = Skill.BEGINNER

    existing_skill = Skill.objects.filter(
        user=request.user,
        name__iexact=name
    ).first()

    if existing_skill:

        messages.warning(
            request,
            f"{name} is already in your skills."
        )

        return redirect("skills")

    Skill.objects.create(
        user=request.user,
        name=name,
        level=level
    )

    messages.success(
        request,
        f"{name} added successfully."
    )

    return redirect("skills")


@login_required
def delete_skill_view(
    request,
    skill_id
):

    if request.method != "POST":
        return redirect("skills")

    try:

        skill = Skill.objects.get(
            id=skill_id,
            user=request.user
        )

    except Skill.DoesNotExist:

        messages.error(
            request,
            "Skill not found."
        )

        return redirect("skills")

    skill_name = skill.name

    skill.delete()

    messages.success(
        request,
        f"{skill_name} deleted successfully."
    )

    return redirect("skills")


# =========================================================
# CAREER
# =========================================================

@login_required
def career_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    career_goals = CareerGoal.objects.all().order_by(
        "title"
    )

    return render(
        request,
        "career.html",
        {
            "profile": profile,
            "career_goals": career_goals,
        }
    )


@login_required
def set_career_goal_view(request):

    if request.method != "POST":
        return redirect("career")

    career_id = request.POST.get(
        "career_goal"
    )

    if not career_id:

        messages.error(
            request,
            "Please select a career goal."
        )

        return redirect("career")

    try:

        career_goal = CareerGoal.objects.get(
            id=career_id
        )

    except CareerGoal.DoesNotExist:

        messages.error(
            request,
            "Selected career goal was not found."
        )

        return redirect("career")

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    profile.career_goal = career_goal.title

    profile.save()

    messages.success(
        request,
        f"Career goal set to {career_goal.title}."
    )

    return redirect("career")


# =========================================================
# SKILL GAP ANALYSIS
# =========================================================

@login_required
def skill_gap_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    user_skills = Skill.objects.filter(
        user=request.user
    ).order_by("name")

    matched_skills = []
    missing_skills = []
    required_skills = []

    career = None

    if profile.career_goal:

        try:

            career = CareerGoal.objects.get(
                title=profile.career_goal
            )

        except CareerGoal.DoesNotExist:

            career = None

    if career:

        required_skills = [
            skill.strip()
            for skill in career.required_skills.split(",")
            if skill.strip()
        ]

        user_skill_names = {
            skill.name.strip().lower()
            for skill in user_skills
        }

        for required_skill in required_skills:

            if required_skill.lower() in user_skill_names:

                matched_skills.append(
                    required_skill
                )

            else:

                missing_skills.append(
                    required_skill
                )

    total_required = len(
        required_skills
    )

    total_matched = len(
        matched_skills
    )

    total_missing = len(
        missing_skills
    )

    if total_required > 0:

        match_percentage = round(
            (
                total_matched
                / total_required
            ) * 100
        )

    else:

        match_percentage = 0

    return render(
        request,
        "skill_gap.html",
        {
            "profile": profile,
            "career": career,
            "user_skills": user_skills,
            "required_skills": required_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "total_required": total_required,
            "total_matched": total_matched,
            "total_missing": total_missing,
            "match_percentage": match_percentage,
        }
    )


# =========================================================
# LEARNING ROADMAP
# =========================================================

@login_required
def roadmap_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    career = None

    if profile.career_goal:

        try:

            career = CareerGoal.objects.get(
                title=profile.career_goal
            )

        except CareerGoal.DoesNotExist:

            career = None

    missing_skills = []

    if career:

        required_skills = [
            skill.strip()
            for skill in career.required_skills.split(",")
            if skill.strip()
        ]

        user_skill_names = {
            skill.name.strip().lower()
            for skill in Skill.objects.filter(
                user=request.user
            )
        }

        for required_skill in required_skills:

            if required_skill.lower() not in user_skill_names:

                missing_skills.append(
                    required_skill
                )

    for skill_name in missing_skills:

        existing_item = LearningItem.objects.filter(
            user=request.user,
            skill_name__iexact=skill_name
        ).first()

        if not existing_item:

            LearningItem.objects.create(
                user=request.user,
                skill_name=skill_name,
                topic=f"{skill_name} Fundamentals",
                description=(
                    f"Learn the fundamentals of "
                    f"{skill_name} and build practical "
                    f"knowledge through hands-on practice."
                ),
                estimated_hours=5,
                status=LearningItem.NOT_STARTED,
                progress=0
            )

    if career:

        LearningItem.objects.filter(
            user=request.user
        ).exclude(
            skill_name__in=missing_skills
        ).delete()

    roadmap_items = LearningItem.objects.filter(
        user=request.user
    ).order_by(
        "created_at"
    )

    total_items = roadmap_items.count()

    completed_items = roadmap_items.filter(
        status=LearningItem.COMPLETED
    ).count()

    if total_items > 0:

        roadmap_percentage = round(
            (
                completed_items
                / total_items
            ) * 100
        )

    else:

        roadmap_percentage = 0

    return render(
        request,
        "roadmap.html",
        {
            "profile": profile,
            "career": career,
            "roadmap_items": roadmap_items,
            "total_items": total_items,
            "completed_items": completed_items,
            "roadmap_percentage": roadmap_percentage,
        }
    )


@login_required
def update_learning_progress_view(
    request,
    item_id
):

    if request.method != "POST":
        return redirect("roadmap")

    try:

        item = LearningItem.objects.get(
            id=item_id,
            user=request.user
        )

    except LearningItem.DoesNotExist:

        messages.error(
            request,
            "Learning item not found."
        )

        return redirect("roadmap")

    progress_value = request.POST.get(
        "progress",
        "0"
    )

    try:

        progress = int(
            progress_value
        )

    except ValueError:

        progress = 0

    progress = max(
        0,
        min(
            progress,
            100
        )
    )

    item.progress = progress

    if progress == 100:

        item.status = LearningItem.COMPLETED

    elif progress > 0:

        item.status = LearningItem.IN_PROGRESS

    else:

        item.status = LearningItem.NOT_STARTED

    item.save()

    messages.success(
        request,
        f"{item.skill_name} progress updated to {progress}%."
    )

    return redirect("roadmap")


# =========================================================
# PROJECTS
# =========================================================

@login_required
def projects_view(request):

    projects = Project.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "projects.html",
        {
            "projects": projects
        }
    )


@login_required
def add_project_view(request):

    if request.method != "POST":
        return redirect("projects")

    title = request.POST.get(
        "title",
        ""
    ).strip()

    description = request.POST.get(
        "description",
        ""
    ).strip()

    technologies = request.POST.get(
        "technologies",
        ""
    ).strip()

    github_url = request.POST.get(
        "github_url",
        ""
    ).strip()

    live_url = request.POST.get(
        "live_url",
        ""
    ).strip()

    if not title or not description or not technologies:

        messages.error(
            request,
            "Please fill in the project title, description and technologies."
        )

        return redirect("projects")

    Project.objects.create(
        user=request.user,
        title=title,
        description=description,
        technologies=technologies,
        github_url=github_url,
        live_url=live_url
    )

    messages.success(
        request,
        f"Project '{title}' added successfully."
    )

    return redirect("projects")


@login_required
def delete_project_view(
    request,
    project_id
):

    if request.method != "POST":
        return redirect("projects")

    try:

        project = Project.objects.get(
            id=project_id,
            user=request.user
        )

    except Project.DoesNotExist:

        messages.error(
            request,
            "Project not found."
        )

        return redirect("projects")

    project_title = project.title

    project.delete()

    messages.success(
        request,
        f"Project '{project_title}' deleted successfully."
    )

    return redirect("projects")


# =========================================================
# CERTIFICATIONS
# =========================================================

@login_required
def certifications_view(request):

    certifications = Certification.objects.filter(
        user=request.user
    ).order_by(
        "-issue_date",
        "-id"
    )

    return render(
        request,
        "certifications.html",
        {
            "certifications": certifications
        }
    )


@login_required
def add_certification_view(request):

    if request.method != "POST":
        return redirect("certifications")

    name = request.POST.get(
        "name",
        ""
    ).strip()

    organization = request.POST.get(
        "organization",
        ""
    ).strip()

    issue_date = request.POST.get(
        "issue_date",
        ""
    ).strip()

    certificate_url = request.POST.get(
        "certificate_url",
        ""
    ).strip()

    if not name or not organization:

        messages.error(
            request,
            "Please enter the certification name and organization."
        )

        return redirect("certifications")

    Certification.objects.create(
        user=request.user,
        name=name,
        organization=organization,
        issue_date=issue_date if issue_date else None,
        certificate_url=certificate_url
    )

    messages.success(
        request,
        f"Certification '{name}' added successfully."
    )

    return redirect("certifications")


@login_required
def delete_certification_view(
    request,
    certification_id
):

    if request.method != "POST":
        return redirect("certifications")

    try:

        certification = Certification.objects.get(
            id=certification_id,
            user=request.user
        )

    except Certification.DoesNotExist:

        messages.error(
            request,
            "Certification not found."
        )

        return redirect("certifications")

    certification_name = certification.name

    certification.delete()

    messages.success(
        request,
        f"Certification '{certification_name}' deleted successfully."
    )

    return redirect("certifications")