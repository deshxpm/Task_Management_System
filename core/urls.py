from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingView, name='landing_page'),

    path('register', views.register_view, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # Employee
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.create_employee, name='create_employee'),
    path('employees/<int:id>/view/', views.view_employee, name='view_employee'),
    path('employees/<int:id>/edit/', views.edit_employee, name='edit_employee'),
    path('employees/<int:id>/delete/', views.delete_employee, name='delete_employee'),

    path('employee/upload/', views.upload_employee_excel, name='upload_employee_excel'),
    path('employee/demo/', views.download_demo_file, name='download_demo_file'),

    # Department
    path('departments/', views.list_departments, name='list_departments'),
    path('departments/create/', views.create_department, name='create_department'),
    path('departments/<int:id>/edit/', views.edit_department, name='edit_department'),
    path('departments/<int:id>/delete/', views.delete_department, name='delete_department'),

    # Designation
    path('designations/', views.list_designations, name='list_designations'),
    path('designations/create/', views.create_designation, name='create_designation'),
    path('designations/<int:id>/edit/', views.edit_designation, name='edit_designation'),
    path('designations/<int:id>/delete/', views.delete_designation, name='delete_designation'),
    
    #Auth
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard_view, name='dashboard'),

    path('task/list/', views.task_list, name='task_list'),
    path('create-task/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/chat/', views.task_chat_view, name='task_chat'),
    path('save-message/', views.save_message, name='save_message'),
    path('get_chat_messages/<int:task_id>/', views.get_chat_messages, name='get_chat_messages'),
    path('tasks/update/status/<int:task_id>/', views.update_task_status, name='update_task_status'),

    path('chat/delete_message/<int:message_id>/', views.delete_message_view, name='delete_message'),

    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),

    # Fetch unread message count
    path('get_unread_message_count/', views.get_unread_message_count, name='get_unread_message_count'),

    # Mark messages as read
    path('mark_messages_as_read/<int:task_id>/', views.mark_messages_as_read, name='mark_messages_as_read'),

    # Role & Permissions
    path('roles/', views.role_list, name='role_list'),
    path('roles/add/', views.add_role, name='add_role'),
    path('roles/<int:id>/edit/', views.edit_role, name='edit_role'),
    path('roles/<int:id>/delete/', views.delete_role, name='delete_role'),

    path('protected-page/', views.some_protected_view, {'permission': 'view_reports'}, name='protected_page'),

]


