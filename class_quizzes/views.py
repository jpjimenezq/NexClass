from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .models import Quiz, Question, Answer, QuizResult
from .forms import QuizForm, QuestionForm, QuizFormClass, AnswerFormSet
from classCreation_Schedules.models import Class
from users.models import Student, Teacher


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
    teacher_obj = get_object_or_404(Teacher, user=request.user)
    if class_id:
        class_obj = get_object_or_404(Class, id=class_id)
        quizzes = Quiz.objects.filter(class_obj=class_obj)
        titulo = f'Mostrando quices para la clase: {class_obj.className}'
        # return render(request, 'quiz_list.html', {'quizzes': quizzes, 'class_obj': class_obj, 'titulo': titulo})
    else:
        quizzes = Quiz.objects.filter(class_obj__teacher=teacher_obj)
        titulo = f'Mostrando Todos los quices: '

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


def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    total_questions = questions.count()
    student = Student.objects.get(user=request.user)

    current_question_index = int(request.GET.get('question_index', 0))

    if 'correct_answers' not in request.session:
        request.session['correct_answers'] = 0

    if current_question_index >= total_questions:
        # Guardar el resultado en la base de datos
        correct_answers = request.session['correct_answers']
        score = int((correct_answers / total_questions) * 100)

        QuizResult.objects.create(
            student=student,  # Asumiendo que el usuario está autenticado
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers
        )

        del request.session['correct_answers']

        return redirect('quiz_result', quiz_id=quiz.id)

    current_question = questions[current_question_index]
    answers = current_question.answers.all()

    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer')
        selected_answer = Answer.objects.get(id=selected_answer_id)

        # Verificar si la respuesta es correcta y actualizar el conteo
        if selected_answer.is_correct:
            request.session['correct_answers'] += 1

        # Redirigir a la siguiente pregunta
        return redirect(f'{request.path}?question_index={current_question_index + 1}')

    progress = int((current_question_index + 1) / total_questions * 100)  # Progreso en %

    return render(request, 'take_quiz.html', {
        'quiz': quiz,
        'current_question': current_question,
        'answers': answers,
        'progress': progress,
        'current_question_index': current_question_index + 1,
        'total_questions': total_questions
    })


def quiz_result(request, quiz_id):
    student = Student.objects.get(user=request.user)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    result = QuizResult.objects.filter(student=student, quiz=quiz).last()
    return render(request, 'quiz_result.html', {'quiz': quiz, 'result': result})


def quiz_list_student(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    quizzes = Quiz.objects.filter(class_obj=class_obj)

    return render(request, 'quiz_list_student.html', {
        'quizzes': quizzes,
        'class_obj': class_obj
    })


def completed_quizzes(request):
    student = Student.objects.get(user=request.user)
    student_quizzes = QuizResult.objects.filter(student=student)

    return render(request, 'completed_quizzes.html', {
        'student_quizzes_': student_quizzes,
    })
