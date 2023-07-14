from django.shortcuts import render
from django.http import JsonResponse



# Create your views here.


def calculate_cost(request):
    input_data = request.GET.get('input_data', '').split('\n')
    
    if not input_data:
        response = {
            'error': 'Missing input data or invalid format'
        }
        return JsonResponse(response, status=400)
    
    datasets = []
    for i in range(len(input_data)):
        dataset = list(map(int, input_data[i].split()))
        if dataset == [0, 0, 0]:
            break
        datasets.append(dataset)
    
    total_costs = []
    for dataset in datasets:
        m, c, n = dataset[:3]
        student_requests = dataset[3:]
        
        desks = [[] for _ in range(m)]
        shelf = []
        total_cost = 0

        for student in range(n):
            requests = student_requests.pop(0)
            for _ in range(requests):
                book_id = student_requests.pop(0)
                book_found = False
                cost = 0

                # Check if the requested book is on the desks
                for desk_index, desk in enumerate(desks):
                    if book_id in desk:
                        desk.remove(book_id)
                        desks[0].append(book_id)  # Move the book to desk D1
                        cost = desk_index + 1
                        book_found = True
                        break

                # If the book is not on the desks, check the shelf
                if not book_found and book_id in shelf:
                    shelf.remove(book_id)
                    desks[0].append(book_id)  # Move the book to desk D1
                    cost = m + 1
                    book_found = True

                # If the book is still not found, find the least recently used book on D1 and replace it
                if not book_found:
                    least_recently_used = desks[0].pop(0)
                    cost = m + 1
                    if len(desks[0]) < c:
                        desks[0].append(book_id)
                    else:
                        for desk in desks[1:]:
                            if len(desk) < c:
                                desk.append(book_id)
                                break
                        else:
                            shelf.append(book_id)
                    desks[0].append(least_recently_used)

                total_cost += cost

        total_costs.append(total_cost)

    response = {
        'total_costs': total_costs
    }
    return JsonResponse(response)


def calculate_cost(request):
    input_data = request.GET.get('input_data', '').split('\n')
    
    if not input_data:
        response = {
            'error': 'Missing input data or invalid format'
        }
        return JsonResponse(response, status=400)
    
    datasets = []
    for i in range(len(input_data)):
        dataset = list(map(int, input_data[i].split()))
        if dataset == [0, 0, 0]:
            break
        datasets.append(dataset)
    
    total_costs = []
    for dataset in datasets:
        m, c, n = dataset[:3]
        student_requests = dataset[3:]
        
        desks = [[] for _ in range(m)]
        shelf = []
        total_cost = 0

        for student in range(n):
            requests = student_requests.pop(0)
            for _ in range(requests):
                book_id = student_requests.pop(0)
                book_found = False
                cost = 0

                # Check if the requested book is on the desks
                for desk_index, desk in enumerate(desks):
                    if book_id in desk:
                        desk.remove(book_id)
                        desks[0].append(book_id)  # Move the book to desk D1
                        cost = desk_index + 1
                        book_found = True
                        break

                # If the book is not on the desks, check the shelf
                if not book_found and book_id in shelf:
                    shelf.remove(book_id)
                    desks[0].append(book_id)  # Move the book to desk D1
                    cost = m + 1
                    book_found = True

                # If the book is still not found, find the least recently used book on D1 and replace it
                if not book_found:
                    least_recently_used = desks[0].pop(0)
                    cost = m + 1
                    if len(desks[0]) < c:
                        desks[0].append(book_id)
                    else:
                        for desk in desks[1:]:
                            if len(desk) < c:
                                desk.append(book_id)
                                break
                        else:
                            shelf.append(book_id)
                    desks[0].append(least_recently_used)

                total_cost += cost

        total_costs.append(total_cost)

    response = {
        'total_costs': total_costs
    }
    return JsonResponse(response)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book, Student, Request

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

