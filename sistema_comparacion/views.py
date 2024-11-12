from django.shortcuts import render, redirect
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import os
from users.models import Teacher
from classCreation_Schedules.models import Class
from django.urls import reverse
from embeddings_simmilarities.utils import calcular_similitud
import re


def seleccionar_comparacion(request):
    if request.method == "POST":
        tipo_comparacion = request.POST.get("tipo_comparacion")
        if tipo_comparacion == "profesores":
            return redirect(reverse("comparar_elementos", kwargs={"tipo": "profesores"}))
        elif tipo_comparacion == "clases":
            return redirect(reverse("comparar_elementos", kwargs={"tipo": "clases"}))
    return render(request, "seleccionar_comparacion.html")


def seleccionar_elementos(request, tipo):
    if tipo == "profesores":
        elementos = Teacher.objects.all()
        tipo_elemento = "profesor"
    else:
        elementos = Class.objects.all()
        tipo_elemento = "clase"

    if request.method == "POST":
        seleccionados = request.POST.getlist("elementos")
        if 2 <= len(seleccionados) <= 4:
            return redirect('mostrar_comparacion', tipo=tipo, seleccionados=",".join(seleccionados))
        else:
            error = "Selecciona entre 2 y 4 elementos para comparar."
            return render(request, "seleccionar_elementos.html",
                          {"elementos": elementos, "error": error, "tipo_elemento": tipo_elemento})

    return render(request, "seleccionar_elementos.html", {"elementos": elementos, "tipo_elemento": tipo_elemento})


def mostrar_comparacion(request, tipo, seleccionados):
    ids = seleccionados.split(",")
    elementos = Teacher.objects.filter(id__in=ids) if tipo == "profesores" else Class.objects.filter(id__in=ids)
    user_message = f"Tipo de comparaciones: {tipo}:\n"

    print(elementos)
    i = 1
    if tipo == "profesores":
        for teacher in elementos:
            user_message += f"({i}). Nombre Profesor: {teacher.user.name}\nEspecialidades: {teacher.specialities}\nBiography: {teacher.biography}\nDescription: {teacher.description}\nCalificacion del profesor: {teacher.average_rating}\nModo de clase: {teacher.mode}\nCiudad: {teacher.ciudad}\n**Comparaciones:\n"

    else:
        for class_obj in elementos:
            user_message += f"({i}). Nombre Clase: {class_obj.className}\nDescription: {class_obj.description}\Rating del profesor de clase: {class_obj.teacher.average_rating}\nModo de clase: {class_obj.teacher.mode}\nCiudad: {class_obj.teacher.ciudad}\n**Comparaciones:\n"

    comparaciones = []
    for i, elemento1 in enumerate(elementos):
        for elemento2 in elementos[i + 1:]:
            similitud = calcular_similitud(elemento1.get_embedding(), elemento2.get_embedding())
            if tipo == "profesores":
                comparaciones.append({
                    "elemento1": elemento1.user.name,
                    "elemento2": elemento2.user.name,
                    "similitud": similitud
                })
            else:  # Suponemos que el tipo es "clases"
                comparaciones.append({
                    "elemento1": elemento1.className,
                    "elemento2": elemento2.className,
                    "similitud": similitud
                })

    # Prompt para OpenAI describiendo las similitudes y diferencias
    user_message += f'{comparaciones}'

    respuesta_openai = generar_recomendacion_openai(user_message)

    return render(request, "mostrar_comparacion.html", {
        'tipo': tipo,
        'elementos': elementos,
        "comparaciones": comparaciones,
        "recomendacion": respuesta_openai,
    })


def generar_recomendacion_openai(prompt):
    _ = load_dotenv('api_keys.env')
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get('openai_apikey'),
    )
    system_instruction = """
        Eres un sistema de comparaciones de profesores o clases, recibiras in TIPO de comparaciones (profesores, clase).
        Ademas recibiras la descripcion de los profesores o clases y su respectivo embedding generado entre los diferentes profesores y clases.
        Debes analizar cada profesor o clase, y mostrar los pros y contras de cada uno teniendo en cuenta todos los aspectos.
        Desarrollar el siguiente formato, las etiquetas dejalas asi como esta en el formato
    
        <br><br><h2>Nombre profesor o clase</h2><br>
        <h5>1)  Analisis: </h5> analisis de cada profesor o clase.<br><h5>2) Pros y contras: pros </h5>y contras de cada profesor o clase.<br><h5>3)  Embedding:</h5> Analizar los embebeddings y relaciones entre los profesores o clase.<br><h5>4)  Conclusion:</h5> Conlclusiones de cual deberia elegir.<br>
        
        y asi por cada clase o profesor que te den
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Ensure you're using the appropriate GPT model
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        max_tokens=750,
        temperature=0.7,
    )
    msj = completion.choices[0].message.content

    return msj

