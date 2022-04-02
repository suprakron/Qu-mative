from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from .models import Quiz,Student
from quiz.utils.createQuiz import createQuiz
from quiz.utils.updateQuiz import _updateQuiz
from quiz.utils.duplicateQuiz import duplicateQuiz

import datetime
import csv
import xlwt
from django.template.loader import get_template
from xhtml2pdf import pisa
from taker.models import Taker
 


class QuizDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Quiz

    def test_func(self):
        return self.request.user == self.get_object().maker


class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz

    def get_queryset(self):
        return Quiz.objects.filter(maker=self.request.user).order_by('-id')
    # paginate_by = 100


class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quiz
    success_url = reverse_lazy('quiz-list')

    def test_func(self):
        return self.request.user == self.get_object().maker


@login_required
def newQuiz(request):
    if request.method == 'POST':
        data = request.POST.dict()
        print(data)

        createQuiz(data, request.user)

        return redirect('quiz-list')

    defaultNumberOfChoices = range(1, 5)
    return render(request, 'quiz/new_quiz.html', {'defaultNumberOfChoices': defaultNumberOfChoices})


@login_required
def updateQuiz(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)

    if request.user != quiz.maker:
        raise PermissionDenied

    if request.method == 'POST':
        data = request.POST.dict()
        print(data)
        _updateQuiz(data, quiz)

        return redirect('quiz-list')

    startDate = quiz.getStartDate()
    startTime = quiz.getStartTime()

    return render(request, 'quiz/quiz_update.html', {'quiz': quiz, 'startDate': startDate, 'startTime': startTime})


@require_POST
def quizDuplicate(request, pk):
    parentQuiz = get_object_or_404(Quiz, id=pk)

    if request.user != parentQuiz.maker:
        raise PermissionDenied

    data = request.POST.dict()

    quiz = duplicateQuiz(request.user, parentQuiz, data['quiz'])

    return redirect('quiz-update', pk=quiz.id)


@login_required
def quizResult(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)

    if request.user != quiz.maker:
        raise PermissionDenied

    takers = quiz.taker_set.all()
    return render(request, 'quiz/result.html', {'quiz': quiz, 'takers': takers})


# def Export_quiz(request):
#     response=HttpResponse(content_type="text/csv")
#     response["content-Disposition"]='attachment ; filename=takers'+str(datetime.datetime.now())+'.csv'
#     writer=csv.writer(response)
#     writer.writerow(['name' , 'email' , 'score' , 'quiz'])
#     takers = quiz.taker_set.all()
#     for quiz in takers :
#         writer.writerow([quiz.name , quiz.email , quiz.quiz ])
#     return response



def student_list(request):
    students=Student.objects.all()
    
    return render(request , 'quiz/studentlist.html' , {'students':students})



def student_details( request , pk) :
    student=Student.objects.get(id = pk)
    return render(request , 'quiz/studentdetails.html' , {'student':student})



def Export_students(request):
    response=HttpResponse(content_type="text/csv")
    response["content-Disposition"]='attachment ; filename=students'+str(datetime.datetime.now())+'.csv'
    writer=csv.writer(response) 
    writer.writerow(['id' , 'Name' , 'Last Name' , 'Student Code'])
    students=Student.objects.all()
    for student in students :
        writer.writerow([student.id , student.Name , student.Family , student.Code])
    return response



def export_excel(response):
    response=HttpResponse(content_type="apllication/ms-excel")
    response["content-Disposition"]='attachment ; filename=Takers'+str(datetime.datetime.now())+'.xls'
    
    workbook=xlwt.Workbook(encoding='utf-8')
    worksheet=workbook.add_sheet("Takers")
    columns=['name' , 'email' , 'score'  ]
    rownumber=0
    
    for col in range(len(columns)):
        worksheet.write(rownumber , col , columns[col])
        
    Takers=taker.objects.all().values_list('name' , 'email' , 'score')
    
    for std in Takers:
        rownumber+=1
        
        for col in range(len(std)):
            worksheet.write(rownumber , col , std[col])
    
    workbook.save(response)
    return response


def export_pdf(request):
    response=HttpResponse(content_type="apllication/pdf")
    response["content-Disposition"]='attachment ; filename=students'+str(datetime.datetime.now())+'.pdf'
    
    template_path="quiz/studentspdf.html"
    template=get_template(template_path)
    students=Student.objects.all()
    context={"students": students}
    html=template.render(context)
    pisa.CreatePDF( html , dest=response  )
    return response

 



 



 