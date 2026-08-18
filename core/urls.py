from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        "signup/",
        views.signup_view,
        name="signup"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    # =====================================================
    # PROFILE
    # =====================================================

    path(
        "profile/",
        views.profile_view,
        name="profile"
    ),


    # =====================================================
    # SKILLS
    # =====================================================

    path(
        "skills/",
        views.skills_view,
        name="skills"
    ),

    path(
        "skills/add/",
        views.add_skill_view,
        name="add_skill"
    ),

    path(
        "skills/delete/<int:skill_id>/",
        views.delete_skill_view,
        name="delete_skill"
    ),


    # =====================================================
    # CAREER
    # =====================================================

    path(
        "career/",
        views.career_view,
        name="career"
    ),

    path(
        "career/set/",
        views.set_career_goal_view,
        name="set_career_goal"
    ),


    # =====================================================
    # SKILL GAP
    # =====================================================

    path(
        "skill-gap/",
        views.skill_gap_view,
        name="skill_gap"
    ),


    # =====================================================
    # LEARNING ROADMAP
    # =====================================================

    path(
        "roadmap/",
        views.roadmap_view,
        name="roadmap"
    ),

    path(
        "roadmap/update/<int:item_id>/",
        views.update_learning_progress_view,
        name="update_learning_progress"
    ),


    # =====================================================
    # PROJECTS
    # =====================================================

    path(
        "projects/",
        views.projects_view,
        name="projects"
    ),

    path(
        "projects/add/",
        views.add_project_view,
        name="add_project"
    ),

    path(
        "projects/delete/<int:project_id>/",
        views.delete_project_view,
        name="delete_project"
    ),


    # =====================================================
    # CERTIFICATIONS
    # =====================================================

    path(
        "certifications/",
        views.certifications_view,
        name="certifications"
    ),

    path(
        "certifications/add/",
        views.add_certification_view,
        name="add_certification"
    ),

    path(
        "certifications/delete/<int:certification_id>/",
        views.delete_certification_view,
        name="delete_certification"
    ),
]