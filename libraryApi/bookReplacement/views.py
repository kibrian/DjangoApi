from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Book, Student, Request
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['POST'])
def calculate_total_cost(request):
    data = request.data

    m = int(data['m'])
    c = int(data['c'])
    n = int(data['n'])
    students = data['students']

    total_cost = calculate_total_cost_helper(m, c, n, students)

    response = {'total_cost': total_cost}
    return JsonResponse(response)

def calculate_total_cost_helper(m, c, n, students):
    desks = [[] for _ in range(m)]  # Initialize empty desks
    shelf = []  # Initialize empty shelf
    cost = 0  # Total cost

    for student in students:
        for book_id in student:
            # Check if the requested book is already on a desk
            for desk_idx, desk in enumerate(desks):
                if book_id in desk:
                    desk.remove(book_id)
                    desk.append(book_id)  # Move the book to the top of the desk
                    cost += desk_idx + 1  # Accessing the desk costs its index + 1
                    break
            # else:  # If the book is not on any desk
            #     # Check if there is space on the first desk (D1)
            #     if len(desks[0]) < c:
            #         desks[0].append(book_id)
            #         cost += 1  # Accessing D1 costs 1
            #     else:
            #         # Find the least recently used book on D1
            #         lru_book = desks[0].pop(0)
            #         desks[0].append(book_id)
            #         shelf.append(lru_book)
                    cost += m + 1  # Accessing the shelf costs m + 1

    return cost





@csrf_exempt
def create_book(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            book = Book.objects.create(id=data['id'], title=data['title'])
            response = {
                'message': 'Book created successfully.',
                'book_id': book.id
            }
            return JsonResponse(response)
        except KeyError:
            response = {
                'error': 'Invalid data. Please provide the ID and title of the book.'
            }
            return JsonResponse(response, status=400)
    else:
        response = {
            'error': 'Invalid request method. Only POST requests are allowed.'
        }
        return JsonResponse(response, status=405)


@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            student = Student.objects.create(id=data['id'], name=data['name'])
            response = {
                'message': 'Student created successfully.',
                'student_id': student.id
            }
            return JsonResponse(response)
        except KeyError:
            response = {
                'error': 'Invalid data. Please provide the ID and name of the student.'
            }
            return JsonResponse(response, status=400)
    else:
        response = {
            'error': 'Invalid request method. Only POST requests are allowed.'
        }
        return JsonResponse(response, status=405)


@csrf_exempt
def create_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            student_id = data['student']
            book_id = data['book']
            student = Student.objects.get(id=student_id)
            book = Book.objects.get(id=book_id)
            request = Request.objects.create(student=student, book=book)
            response = {
                'message': 'Request created successfully.',
                'request_id': request.id
            }
            return JsonResponse(response)
        except (KeyError, Student.DoesNotExist, Book.DoesNotExist):
            response = {
                'error': 'Invalid data. Please provide valid student and book IDs.'
            }
            return JsonResponse(response, status=400)
    else:
        response = {
            'error': 'Invalid request method. Only POST requests are allowed.'
        }
        return JsonResponse(response, status=405)

def get_books(request):
    books = Book.objects.all()
    book_list = [{'id': book.id, 'title': book.title} for book in books]
    response = {'books': book_list}
    return JsonResponse(response)

def get_students(request):
    students = Student.objects.all()
    student_list = [{'id': student.id, 'name': student.name} for student in students]
    response = {'students': student_list}
    return JsonResponse(response)

def get_requests(request):
    requests = Request.objects.all()
    request_list = [{'student': req.student.name, 'book': req.book.title, 'timestamp': req.timestamp} for req in requests]
    response = {'requests': request_list}
    return JsonResponse(response)

