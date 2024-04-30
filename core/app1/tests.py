# #unittest start ------

# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import Task, Priority
# from django.utils import timezone

# class TaskListViewTestCase(TestCase):
#     def setUp(self):
#         # Create a test user
#         self.user = User.objects.create_user(username='testuser', password='password123')
#         print("Test user created")

#         # Create a test priority
#         priority = Priority.objects.create(name='High')
#         print("Test priority created")

#         # Create a test task with the priority
#         self.task1 = Task.objects.create(
#             description='Task 1',
#             assigned_user=self.user,
#             deadline=timezone.now(),
#             priority=priority  # Pass the created priority object
#         )
#         print("Test task 1 created")

#         # Log in the test user
#         self.client = Client()
#         self.client.login(username='testuser', password='password123')
#         print("Test user logged in")

#         # Create another task for user
#         self.task2 = Task.objects.create(description='Task 2', assigned_user=self.user, deadline=timezone.now(), priority=priority)
#         print("Test task 2 created")

#     def test_task_list_view(self):
#         print("Testing task list view")

#         # Get the task list view URL
#         url = reverse('task_list')
#         print("URL:", url)

#         # Make a GET request to the task list view
#         response = self.client.get(url)
#         print("GET request made to task list view")

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)
#         print("Response status code:", response.status_code)

#         # Check that the tasks are present in the response context
#         self.assertIn('tasks', response.context)
#         print("Tasks found in response context")

#         # Check that the tasks returned in the response context match the tasks created in the setUp method
#         tasks = response.context['tasks']
#         self.assertEqual(len(tasks), 2)
#         self.assertEqual(tasks[0].description, 'Task 1')
#         self.assertEqual(tasks[1].description, 'Task 2')
#         print("Tasks in response context match created tasks")
#         print()

# #unittest end ------

# #integration start ------

# from django.urls import reverse
# from rest_framework.test import APITestCase
# from datetime import datetime
# from django.contrib.auth import get_user_model
# from .models import Task, Priority

# User = get_user_model()

# class TaskIntegrationTest(APITestCase):
#     def setUp(self):
#         # Create a test user
#         self.user = User.objects.create_user(username="testuser", password="password")  # Create user with password

#         # Create a test priority
#         self.priority = Priority.objects.create(name="High")

#     def test_task_flow(self):
#         # Authenticate the user
#         self.client.force_authenticate(user=self.user)

#         # Create a task with primary key values for assigned_user and priority
#         task_data = {
#             'description': 'Test task',
#             'assigned_user': self.user.id,  # Primary key value for assigned_user
#             'deadline': datetime.now(),
#             'priority': self.priority.id  # Primary key value for priority
#         }

#         # Make a POST request to create the task
#         response = self.client.post(reverse('task_list_create'), task_data, format='json')

#         # Print the response content
#         print("POST Response Content:", response.content)
    
#         # Check if the task was created successfully
#         self.assertEqual(response.status_code, 201)  # HTTP 201 Created
#         self.assertEqual(Task.objects.count(), 1)
#         print("Task count:", Task.objects.count())

#         # Retrieve the created task from the database
#         task = Task.objects.first()

#         # Check if the retrieved task matches the created task
#         self.assertEqual(task.description, "Test task")
#         self.assertEqual(task.assigned_user, self.user)
#         self.assertIsNotNone(task.deadline)
#         self.assertEqual(task.priority, self.priority)

#         # Retrieve the task using its detail endpoint
#         detail_response = self.client.get(reverse('task_detail_view', kwargs={'pk': task.id}))

#         # Print the detail response content
#         print("Detail Response Content:", detail_response.content)

#         # Check if the task detail endpoint returns the expected data
#         self.assertEqual(detail_response.status_code, 200)  # HTTP 200 OK
#         self.assertEqual(detail_response.data['description'], "Test task")

#integration end ------

#end to end start -------

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TaskCreationNotificationTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  
        self.driver.get("http://localhost:8000/tasks/")  # Update the URL to match the new pattern

    def test_task_creation_notification(self):
        driver = self.driver

        # Simulate logging in
        username = driver.find_element(By.ID, "username")
        username.send_keys("testuser")
        password = driver.find_element(By.ID, "password")
        password.send_keys("password")
        password.send_keys(Keys.RETURN)

        # Simulate navigating to the task creation page
        create_task_button = driver.find_element(By.ID, "create_task_button")
        create_task_button.click()

        # Fill in task details
        task_description = driver.find_element(By.ID, "task_description")
        task_description.send_keys("Sample task description")

        # Submit the task creation form
        submit_button = driver.find_element(By.ID, "submit_button")
        submit_button.click()

        # Wait for the notification to appear
        time.sleep(2)

        # Verify that the notification is displayed
        notification = driver.find_element(By.ID, "notification")
        self.assertEqual(notification.text, "You have a new task assigned.")

    def tearDown(self):
        self.driver.close()

#end to end / end -------