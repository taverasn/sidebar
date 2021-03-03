from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard_index, name="dashboard_index"),
    path("dashboard/accounts/", views.account_dashboard, name="account_dashboard"),
    path(
        "dashboard/accounts/create/",
        views.AccountCreate.as_view(),
        name="account_create",
    ),
    path(
        "dashboard/accounts/<int:pk>/update/",
        views.AccountUpdate.as_view(),
        name="account_update",
    ),
    path(
        "dashboard/accounts/<int:pk>/delete/",
        views.AccountDelete.as_view(),
        name="account_delete",
    ),
    # path('dashboard/accounts/<int:user_id>/account_photo/', views.account_photo, name='account_photo'),
    path("topics/<int:topic_id>/", views.topics_detail, name="topics_detail"),
    path("topics/", views.TopicList.as_view(), name="topics_index"),
    path("topics/create/", views.TopicCreate.as_view(), name="topic_create"),
    path("topics/<int:pk>/update/", views.TopicUpdate.as_view(), name="topic_update"),
    path("topics/<int:pk>/delete/", views.TopicDelete.as_view(), name="topic_delete"),
    # path('topics/<int:topic_id>/topic_photo/', views.topic_photo, name='topic_photo'),
    # path('topics/<int:topic_id>/bookmark_topic/<int:user_id>/', views.bookmark_topic, name='bookmark_topic'),
    # path('topics/<int:topic_id>/unbookmark_topic/<int:user_id>/', views.unbookmark_topic, name='unbookmark_topic'),
    path("topics/<int:topic_id>/add_post/", views.add_post, name="add_post"),
    path(
        "topics/<int:topic_id>/posts/<int:post_id>/",
        views.post_detail,
        name="post_detail",
    ),
    path(
        "topics/<int:topic_id>/posts/<int:pk>/update/",
        views.PostUpdate.as_view(),
        name="post_update",
    ),
    path(
        "topics/<int:topic_id>/posts/<int:pk>/delete/",
        views.PostDelete.as_view(),
        name="post_delete",
    ),
    # path('topics/<int:topic_id>/posts/<int:post_id>/post_photo/', views.post_photo, name='post_photo'),
    # path('topics/<int:topic_id>/posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    # path('topics/<int:topic_id>/posts/<int:post_id>/comments/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    # path('topics/<int:topic_id>/posts/<int:post_id>/comments/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
]
