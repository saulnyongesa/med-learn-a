from django.urls import path
from student.forms import PWDChangeView
from django.contrib.auth import views as auth_views
from student import views

urlpatterns = [
    path('Dashboard/', views.dashboard_index_student, name='student-dashboard-url'),
    path('Tutorial/View/<pk>/', views.tutorial, name='student-tutorial-url'),
    path('Tutorial/Remove-From-Recently/<pk>/', views.tutorial_remove_from_recently_viewed, name='student-tutorial-rm-rv-url'),
]

urlpatterns += [
    path('Profile/', views.profile, name='student-profile-url'),
    path('Profile/Edit/', views.profile_edit, name='student-profile-edit-url'),
    path('Signout/', views.sign_out, name='student-sign-out-url'),
]
# Exams Url==================================================================
urlpatterns += [
    path('Cat/Home/', views.cat_home, name='student-cat-home-url'),
    path('Cat/View/<pk>/', views.cat_view, name='student-cat-view-url'),
    path('Search/Cat/', views.cat_search, name='student-cat-search-url'),
    path('Cat/Response/Save/<pk>', views.cat_response_save, name='student-cat-response-save-url'),
    path('Cat/Submit/<pk>', views.cat_submission, name='student-cat-submit-url'),

]

# Password and account related urls===========================================
urlpatterns += [
    path('PasswordChange/',
         PWDChangeView.as_view(template_name='pwd/student-pwd-change.html'), name='student-change-pwd-url'),
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
