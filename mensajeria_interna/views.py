from .models import ClassChat, PrivateChat, Message
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from users.models import Teacher, Student, User, UserType
from .forms import MessageForm
from classCreation_Schedules.models import Class
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import os


# detalle de la clase y enviar mensaje, no se distingue profesor o estudiante
@login_required
def class_chat_detail(request, chat_id):
    class_chat = ClassChat.objects.get(id=chat_id)
    messages = Message.objects.filter(class_chat=class_chat)
    user = request.user
    unread_messages = class_chat.messages.filter(is_read=False).exclude(sender=request.user)
    quick_suggestions = ''
    chat_type = f'Chat grupal de la clase sobre: {class_chat.teacher.specialities}'
    if unread_messages:
        unr = 'unread_messages'
        quick_suggestions = get_message_suggestions(unread_messages, user.name, unr, chat_type)
    else:
        last_message = class_chat.messages.order_by('-timestamp')

        if last_message.exists() and last_message[0].sender == request.user:
            unr = '0_messages_role'
            msj = ''
            if str(request.user.user_type) == 'Student':
                msj += f"Mi Rol: Estudiante\n Rol de la otras personas: \n1. profesor de: {class_chat.teacher.specialities}\n2. Estudiantes de la misma clase"

            else:
                msj += f"Mi Rol: Profesor de {class_chat.teacher.specialities}\n Rol de la otras personas: Estudiantes de mi clase"

            quick_suggestions = get_message_suggestions(msj, user.name, unr, chat_type)

        elif last_message.exists():
            unr = 'last_messages'
            quick_suggestions = get_message_suggestions(last_message[:1], user.name, unr, chat_type)

        else:
            unr = '0_messages_role'
            msj = ''
            if str(request.user.user_type) == 'Student':
                msj = f"Mi Rol: Estudiante\n Rol de la otras personas: \n1. profesor de: {class_chat.teacher.specialities}\n2. Estudiantes de la misma clase"
            else:
                msj += f"Mi Rol: Profesor de {class_chat.teacher.specialities}\n Rol de la otras personas: Estudiantes de mi clase"

            quick_suggestions = get_message_suggestions(msj, user.name, unr, chat_type)


    messages.update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chat = class_chat
            message.save()
            return redirect('class_chat_detail', chat_id=chat_id)
    else:
        form = MessageForm()

    user = request.user
    base = ''
    if user.user_type == UserType.STUDENT:
        base = 'navbar.html'

    if user.user_type == UserType.TEACHER:
        base = 'navbarTeacher.html'

    return render(request, 'class_chat_detail.html',
                {'class_chat': class_chat, 'messages': messages, 'form': form,
                'base': base, 'quick_suggestions': quick_suggestions,})

@login_required
def send_class_message(request, chat_id):
    class_chat = get_object_or_404(ClassChat, id=chat_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(class_chat=class_chat, sender=request.user, content=content)
        return redirect('class_chat_detail', chat_id=class_chat.id)


# Todos los chats
@login_required
def chat_list(request):
    # Identificar si el usuario es un profesor o un estudiante
    user = request.user
    base = ''
    context = {}

    if user.user_type == UserType.STUDENT:
        base = 'navbar.html'
        student = Student.objects.get(user=request.user)

        class_chats = student.class_chats_students.all()
        private_chats = PrivateChat.objects.filter(student=student)

        class_chats_data = []
        for class_chat in class_chats:
            unread_count = class_chat.messages.filter(is_read=False).exclude(sender=request.user).count()
            class_chats_data.append((class_chat, unread_count))

        private_chats_data = []
        for private_chat in private_chats:
            unread_count = private_chat.messages.filter(is_read=False).exclude(sender=request.user).count()
            private_chats_data.append((private_chat, unread_count))

        context = {
            'class_chats_data': class_chats_data,
            'private_chats_data': private_chats_data,
            'base': base
        }

    elif user.user_type == UserType.TEACHER:
        base = 'navbarTeacher.html'
        teacher = Teacher.objects.get(user=request.user)
        class_chats = ClassChat.objects.filter(teacher=teacher)
        private_chats = PrivateChat.objects.filter(teacher=teacher)

        class_chats_data = []
        for class_chat in class_chats:
            unread_count = class_chat.messages.filter(is_read=False).exclude(sender=request.user).count()
            class_chats_data.append((class_chat, unread_count))

        private_chats_data = []
        for private_chat in private_chats:
            unread_count = private_chat.messages.filter(is_read=False).exclude(sender=request.user).count()
            private_chats_data.append((private_chat, unread_count))


        context = {
            'class_chats_data': class_chats_data,
            'private_chats_data': private_chats_data,
            'base': base,
        }


    return render(request, 'chat_list.html', context)


# Mensaje privado
@login_required
def get_or_create_private_chat(request, other_user_id):
    user = request.user
    other_user = get_object_or_404(User, id=other_user_id)
    private_chat, created = None, False
    base = ''

    if user.user_type == UserType.TEACHER and other_user.user_type == UserType.STUDENT:
        private_chat, created = PrivateChat.objects.get_or_create(teacher=Teacher.objects.get(user=user), student=Student.objects.get(user=other_user))

    elif user.user_type == UserType.STUDENT and other_user.user_type == UserType.TEACHER:
        private_chat, created = PrivateChat.objects.get_or_create(teacher=Teacher.objects.get(user=other_user), student=Student.objects.get(user=user))

    else:
        return redirect('home')

    return redirect('private_chat_detail', chat_id=private_chat.id)


@login_required
def private_chat_detail(request, chat_id):
    private_chat = get_object_or_404(PrivateChat, id=chat_id)
    messages_list = private_chat.messages.order_by('timestamp')
    user = request.user
    base = ''
    quick_suggestions = ''
    chat_type = f'Chat privado'


    unread_messages = private_chat.messages.filter(is_read=False).exclude(sender=request.user)
    if unread_messages:
        unr = 'unread_messages'
        quick_suggestions = get_message_suggestions(unread_messages, user.name, unr, chat_type)
    else:
        last_message = private_chat.messages.order_by('-timestamp')
        if last_message.exists() and last_message[0].sender == request.user:
            unr = '0_messages_role'
            msj = ''
            if str(request.user.user_type) == 'Student':
                msj += f"Mi Rol: Estudiante\n Rol de la otra persona: profesor de: {private_chat.teacher.specialities}"

            else:
                msj += f"Mi Rol: Profesor de {private_chat.teacher.specialities}\n Rol de la otra persona: Estudiante"

            quick_suggestions = get_message_suggestions(msj, user.name, unr, chat_type)

        elif last_message.exists():
            unr = 'last_messages'
            quick_suggestions = get_message_suggestions(last_message[:1], user.name, unr, chat_type)

        else:
            unr = '0_messages_role'
            msj = ''
            if str(request.user.user_type) == 'Student':
                msj += f"Mi Rol: Estudiante\n Rol de la otra persona: profesor de: {private_chat.teacher.specialities}"
            else:
                msj += f"Mi Rol: Profesor de {private_chat.teacher.specialities}\n Rol de la otra persona: Estudiante"

            quick_suggestions = get_message_suggestions(msj, user.name, unr, chat_type)



    unread_messages.update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.private_chat = private_chat
            new_message.sender = user
            new_message.save()
            return redirect('private_chat_detail', chat_id=chat_id)
    else:
        form = MessageForm()

    base = 'navbarTeacher.html' if user.user_type == UserType.TEACHER else 'navbar.html'

    return render(request, 'private_chat_detail.html', {
        'private_chat': private_chat,
        'messages': messages_list,
        'form': form,
        'base': base,
        'quick_suggestions': quick_suggestions,
    })

def get_message_suggestions(messages, username, type, chat_type):
    _ = load_dotenv('api_keys.env')
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get('openai_apikey'),
    )
    user_message = ''
    if type == 'unread_messages':
        num_message = 1
        user_message = f"Tipo de chat: {chat_type}\n**Caso de mensajes no leídos**\n Estos son mis mensajes:\n"
        for message in messages:
            user_message += f"({num_message}). Autor del mensaje:{message.sender}\nContenido: {message.content}\n"
            num_message += 1

    if type == '0_messages_role':
        user_message = f"Tipo de chat: {chat_type}\n**Caso de mensaje vacio**\n yo tengo el rol de: {messages}"

    if type == 'last_messages':
        user_message = f"Tipo de chat: {chat_type}\n**Caso del último mensaje**\n Este es mi ultimo mensaje:\n"
        for message in messages:
            user_message += f"(1). Autor del mensaje:{message.sender}\nContenido: {message.content}\n"

    system_instruction = f'''
    Eres un asistente virtual para un sistema de mensajes. Tu tarea es responder a los mensajes según su contenido. Recibirás mensajes y, dependiendo del contexto y del Tipo de chat, debes dar una respuesta adecuada. Hay tres casos que debes manejar:
    
    1. **Caso de mensajes no leídos**:
       - Si hay varios mensajes no leídos, responde a cada uno de ellos por separado, teniendo en cuenta que podrían estar relacionados. No repitas la misma respuesta si se mencionan temas similares. Si en algún mensaje se menciona el nombre del usuario {username} en el Contenido del mensaje, dirígete directamente a él o ella con el Autor del mensaje. Si no se menciona el nombre, responde según el contenido del mensaje de manera adecuada.
    
    2. **Caso del último mensaje**:
       - Si solo se proporciona el último mensaje del chat, responde a ese mensaje. Si se menciona el nombre del usuario {username} en el Contenido del mensaje, responde de manera personalizada con el Autor del mensaje. Si no se menciona el nombre, responde en función del contenido del mensaje.
    
    3. **Caso de mensaje vacio**
        - No hay mensaje asociado, pero la persona te dira el rol que posee, y te mencionara el rol que posee la otra persona a quien desea enviar un mensaje, responde de manera clara y profesional. Si el rol que posee es Student, puedes responder cosas como: preguntas de la clase, tutorias, fechas de examenes, etc... . Si el que posee es Teacher, puedes responder cosas como: preguntar sobre dudas de clase, si ha realizado los trabajos asignados, preguntar si requiere asesoria, etc.... Por ultimo DEBES responder en primera persona, no des contexto, responde directamente y ve al grano.
        
    Mantén siempre un tono educado, claro y útil en tus respuestas, adaptándote al contexto de cada conversación.
    '''

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  # Ensure you're using the appropriate GPT model
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ],
            max_tokens=100,
            n=3,
            temperature=0.7,
        )

        responses_list = [response.message.content for response in completion.choices]


        return responses_list


    except Exception as e:
        print("Error al obtener sugerencias de la IA:", e)
        return ["No se pudieron generar sugerencias en este momento."]