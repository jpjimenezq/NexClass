from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm, QuizFormClass, AnswerFormSet
from classCreation_Schedules.models import Class


# Vista para crear un quiz
def create_quiz(request, class_id=None):
    if class_id:
        if request.method == 'POST':
            form = QuizFormClass(request.POST)
            if form.is_valid():
                quiz = form.save(commit=False)
                quiz.class_obj = Class.objects.get(id=class_id)
                quiz.save()
                return redirect('add_question', quiz_id=quiz.id)
        else:
            form = QuizFormClass()

    else:
        if request.method == 'POST':
            form = QuizForm(request.POST, class_id=class_id)
            if form.is_valid():
                quiz = form.save()
                return redirect('add_question', quiz_id=quiz.id)
        else:
            form = QuizForm(class_id=class_id)
            form.fields['class_obj'].queryset = Class.objects.all()

    return render(request, 'create_quiz.html', {
        'form': form,
        'class_id': class_id
    })


def quiz_list(request, class_id=None):
    titulo = ''
    if class_id:
        class_obj = get_object_or_404(Class, id=class_id)
        quizzes = Quiz.objects.filter(class_obj=class_obj)
        titulo = f'Mostrando quices para la clase: {class_obj.className}'
        # return render(request, 'quiz_list.html', {'quizzes': quizzes, 'class_obj': class_obj, 'titulo': titulo})
    else:
        quizzes = Quiz.objects.all()
        titulo = f'Mostrando Todos los quices: '
        # return render(request, 'quiz_list.html', {'quizzes': quizzes, 'class_obj': class_id, 'titulo': titulo})
    return render(request, 'quiz_list.html', {'quizzes': quizzes, 'class_id': class_id, 'titulo': titulo})


def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        question_text = request.POST.get('question_text')  # Recupera el texto de la pregunta
        question_form = QuestionForm(request.POST)  # El formulario de preguntas es innecesario aquí

        total_answers = int(request.POST.get('total_answers', 0))

        if question_text:  # Asegúrate de que el texto de la pregunta no esté vacío
            question = Question.objects.create(text=question_text, quiz=quiz)  # Crea la pregunta

            # Guardar las respuestas
            for i in range(total_answers):
                answer_text = request.POST.get(f'answer_text_{i}')
                is_correct = request.POST.get(f'is_correct_{i}', 'off') == 'on'
                if answer_text:
                    Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)

            return redirect('add_question', quiz_id=quiz.id)

    else:
        question_form = QuestionForm()  # Este formulario no es necesario en este caso

    return render(request, 'add_question.html', {
        'quiz': quiz,
    })



def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})


