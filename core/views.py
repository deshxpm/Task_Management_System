from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Task, ChatMessage, User, Notification, Department, Designation,Company
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .utils import *


# Create your views here.
def landingView(request):
    return render(request, 'landing_page.html')

# Registration View
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        except:
            messages.error(request, "Registration failed! Username or email may already exist.")
            return redirect('register')

    return render(request, 'register.html')


def create_employee(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        try:
            user = User.objects.create(username=phone, 
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email, 
                                    phone_number=phone,
                                    company=request.user.company)
            
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
                user.save()

            send_user_credentials(request, user, first_name, last_name)  # Email the credentials
            return redirect('employee_list')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'employee/create_employee.html')  
          
    return render(request, 'employee/create_employee.html')



def employee_list(request):
    employees = User.objects.filter(is_staff=False)  # Assuming employees are non-staff users
    return render(request, 'employee/employee_list.html', {'employees': employees})


# View Employee
def view_employee(request, id):
    employee = get_object_or_404(User, id=id, is_staff=False)  # Assuming employees are non-staff users
    return render(request, 'employee/view_employee.html', {'employee': employee})

# Edit Employee
def edit_employee(request, id):
    employee = get_object_or_404(User, id=id, is_staff=False)  # Assuming employees are non-staff users

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Update fields
        employee.username = username
        employee.email = email
        employee.phone_number = phone_number

        if 'profile_picture' in request.FILES:
            employee.profile_picture = request.FILES['profile_picture']

        employee.save()
        messages.success(request, 'Employee details updated successfully.')
        return redirect('employee_list')

    return render(request, 'employee/edit_employee.html', {'employee': employee})

# Delete Employee
def delete_employee(request, id):
    employee = get_object_or_404(User, id=id, is_staff=False)  # Assuming employees are non-staff users

    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('employee_list')

    return render(request, 'employee/delete_employee.html', {'employee': employee})



# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html')


# Logout View
@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# Dashboard View (example protected view)
@login_required(login_url='/login/')
def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})



# Dashboard (Task List)
@login_required(login_url='/login/')
def task_list(request):
    tasks = Task.objects.filter().order_by('-created_at')
    tasks_message = ChatMessage.objects.filter().order_by('-id')
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'tasks_message':tasks_message})

# Task Creation
@login_required(login_url='/login/')
def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        eta = request.POST['eta']
        assigned_to_id = request.POST['assigned_to']
        assigned_to = User.objects.get(id=assigned_to_id)

        task = Task.objects.create(
            title=title,
            description=description,
            eta=eta,
            created_by=request.user,
            assigned_to=assigned_to
        )
        return redirect('task_list')

    users = User.objects.exclude(id=request.user.id,company=request.user.company,)
    return render(request, 'tasks/create_task.html', {'users': users})

# Task Detail and Chat
@login_required(login_url='/login/')
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    messages = ChatMessage.objects.filter(task=task).order_by('timestamp')
    return render(request, 'tasks/task_detail.html', {'task': task, 'messages': messages})


def get_chat_messages(request, task_id):
    # Fetch messages for the given task from the database
    messages = ChatMessage.objects.filter(task_id=task_id).order_by('timestamp')

    # Prepare the data to send back as JSON
    message_data = []
    for message in messages:
        message_data.append({
            'sender': message.sender.username,  # Assuming sender is a User object
            'message': message.message,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({'messages': message_data})



# Task Chat View (to render chat and notifications page)
@login_required(login_url='/login/')
def task_chat_view(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        # Handle task not found
        return render(request, '404.html')  # Or redirect to some error page

    return render(request, 'chat_and_notifications.html', {'task': task})


# Save Chat Messages
from django.core.files.storage import default_storage
@login_required(login_url='/login/')
def save_message(request):
    if request.method == 'POST':
        task_id = request.POST['task_id']
        message = request.POST.get('message', '')
        file = request.FILES.get('file', None)

        task = Task.objects.get(id=task_id)
        chat_message = ChatMessage.objects.create(
            task=task,
            sender=request.user,
            message=message,
            file=file
        )

        response_data = {
            'status': 'Message saved',
            'sender': chat_message.sender.username,
            'message_id': chat_message.id,
            'timestamp': chat_message.timestamp,
            'file_url': chat_message.file.url if chat_message.file else None,
        }
        return JsonResponse(response_data)
    return JsonResponse({'status': 'Invalid request'}, status=400)



from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/login/')
@csrf_exempt
def delete_message_view(request, message_id):
    try:
        message = ChatMessage.objects.get(id=message_id, sender=request.user)
        message.is_deleted = True  # Soft delete
        message.message = "[Message deleted]"
        message.save()
        return JsonResponse({'status': 'success'})
    except ChatMessage.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)



from django.views.decorators.http import require_GET

@require_GET
def get_unread_message_count(request):
    task_id = request.GET.get('task_id')
    if task_id:
        count = ChatMessage.objects.filter(task_id=task_id, is_read=False).count()
        return JsonResponse({'unread_count': count})
    return JsonResponse({'error': 'Task ID is required'}, status=400)


@csrf_exempt
def mark_messages_as_read(request, task_id):
    if request.method == "POST":
        ChatMessage.objects.filter(task_id=task_id, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)










# List Departments
def list_departments(request):
    departments = Department.objects.filter(company=request.user.company)
    return render(request, 'department/list_departments.html', {'departments': departments})

# Create Department
def create_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        company = request.user.company

        Department.objects.create(name=name, company=company)
        messages.success(request, 'Department created successfully.')
        return redirect('list_departments')

    return render(request, 'department/create_department.html')

# Edit Department
def edit_department(request, id):
    department = get_object_or_404(Department, id=id, company=request.user.company)

    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.save()
        messages.success(request, 'Department updated successfully.')
        return redirect('list_departments')

    return render(request, 'department/edit_department.html', {'department': department})

# Delete Department
def delete_department(request, id):
    department = get_object_or_404(Department, id=id, company=request.user.company)

    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully.')
        return redirect('list_departments')

    return render(request, 'department/delete_department.html', {'department': department})

# List Designations
def list_designations(request):
    designations = Designation.objects.filter(company=request.user.company)
    return render(request, 'designation/list_designations.html', {'designations': designations})

# Create Designation
def create_designation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        company = request.user.company

        Designation.objects.create(name=name, company=company)
        messages.success(request, 'Designation created successfully.')
        return redirect('list_designations')

    return render(request, 'designation/create_designation.html')

# Edit Designation
def edit_designation(request, id):
    designation = get_object_or_404(Designation, id=id, company=request.user.company)

    if request.method == 'POST':
        designation.name = request.POST.get('name')
        designation.save()
        messages.success(request, 'Designation updated successfully.')
        return redirect('list_designations')

    return render(request, 'designation/edit_designation.html', {'designation': designation})

# Delete Designation
def delete_designation(request, id):
    designation = get_object_or_404(Designation, id=id, company=request.user.company)

    if request.method == 'POST':
        designation.delete()
        messages.success(request, 'Designation deleted successfully.')
        return redirect('list_designations')

    return render(request, 'designation/delete_designation.html', {'designation': designation})




