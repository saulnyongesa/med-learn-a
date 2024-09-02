from django.urls import path

from author import views
from student.forms import PWDChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('Dashboard/', views.dashboard_index_author, name='author-dashboard-url'),
    path('Tutorial/View/<pk>/', views.tutorial_view, name='author-tutorial-url'),
]

urlpatterns += [
    path('Profile/', views.profile, name='author-profile-url'),
    path('Profile/Edit/', views.profile_edit, name='author-profile-edit-url'),
]
urlpatterns += [
    path('Tutorial/Edit/<pk>/', views.tutorial_edit, name='author-tutorial-url'),
    path('Tutorial/Create/', views.create_tutorial, name='tutorial-create-url'),
    path('Tutorial/Save/<pk>/', views.save_tutorial, name='save-tutorial-url'),
    path('Tutorial/Topic/Save/', views.save_topic, name='save-topic-url'),
    path('Tutorial/Topic/Create/', views.create_topic, name='create-topic-url'),

    path('Tutorial/Search/', views.search, name='author-search-url'),
    path('Tutorial/Concel-Publish/<pk>/', views.tutorial_conceal_publish, name='conceal-publish-tutorial-url'),
    path('Tutorial/Delete/<pk>/', views.tutorial_delete, name='delete-tutorial-url'),

]
# Exams Url==================================================================
urlpatterns += [
    path('Cat/Home/', views.cat_home, name='cat-home-url'),
    path('Cat/Create/', views.cat_create, name='cat-create-url'),
    path('Cat/View/<pk>', views.cat_view, name='cat-view-url'),
    path('Cat/Edit/<pk>', views.cat_edit, name='cat-edit-url'),
    path('Cat/Publish-Conceal/<pk>', views.cat_publish_conceal, name='cat-conceal-publish-url'),
    path('Cat/Delete/<pk>', views.cat_delete, name='delete-cat-url'),
    path('Cat/Response/Save/<pk>', views.cat_response_save, name='cat-response-save-url'),
]
# Password and account related urls===========================================
urlpatterns += [
    path('PasswordChange/',
         PWDChangeView.as_view(template_name='pwd/author-pwd-change.html'), name='author-change-pwd-url'),
    path('reset_pwd/', auth_views.PasswordResetView.as_view(template_name='pwd/pwd-reset.html'),
         name='reset_password'),
    path('reset_pwd_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='pwd/done.html'),
         name='password_reset_done'),
    path('reset_pwd/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='pwd/confirm.html'),
         name='password_reset_confirm'),
    path('reset_pwd_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='pwd/complete.html'),
         name='password_reset_complete'),
]
