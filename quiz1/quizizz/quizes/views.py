from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result
from django.shortcuts import render
from .forms import ContactForm
from django.shortcuts import get_object_or_404

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # обрабатываем форму
            ...
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'contact.html', context)

def contact(request):
    return render(request, 'contact.html')
def menu(request):
    return render(request, 'menu.html')

def handle_400(request, exception):
    return render(request, '400.html', status=400)

def handle_403(request, exception):
    return render(request, '403.html', status=403)

def handle_404(request, exception):
    return render(request, '404.html', status=404)

def handle_500(request):
    return render(request, '500.html', status=500)

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_custom_value'] = 'Quiz'
        context['my_other_value'] = 'Django project'
        return context



def quiz_view(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    return render(request, 'quizes/quiz.html', {'obj': quiz})


def quiz_data_view(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, slug):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(slug=slug)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})
