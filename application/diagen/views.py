from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from diagen.utils.DiagramCreator import build_diagram_from_code
from diagen.utils.TextConverter import convert_text_to_code
from diagen.utils.extraction.ComponentsExtractor import DEFAULT_COMPONENTS
from django.contrib.auth import authenticate, login, logout
from .models import *
import time
import re


def _build_default_components_text():
    text = ''
    for c in DEFAULT_COMPONENTS:
        text += c + '\n'
    return text

DEFAULT_COMPONENTS_TEXT = _build_default_components_text()
SERV_FULL_ADDRESS = 'http://127.0.0.1:8000/'


def autentificate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    data = {'error': False}
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            data['error'] = True
            data['error_message'] = 'Этот аккаутн заблокирован.'
    else:
        data['error'] = True
        data['error_message'] = 'Неправильный логин или пароль.'

    return JsonResponse(data)


def logout_user(request):
	logout(request)
	return render(request, 'index.html', {'components': DEFAULT_COMPONENTS_TEXT})


def registrate_user(request):
	username = request.POST['username']
	password = request.POST['password']
	try:
		new_user = User.objects.create_user(username, password=password)
	except Exception:
		return JsonResponse({'error': True, 'error_message': "Пользователь с таким именем уже существует."})
	else:
		return JsonResponse({'error': False})


def load_user_data(request):
    user = request.user
    data = {'error': False, 'is_autentificated': False}
    if user.is_authenticated():
        diagrams = Diagram.objects.filter(author=user)
        data['html_text'] = render_to_string('account_data.html', {
            "diagrams": diagrams, 'username': user.username
        })
        data['is_autentificated'] = True
    else:
        data['error'] = True
        data['error_message'] = 'Пользователь не выполнил вход в аккаунт.'
    return JsonResponse(data)

def load_user_diagram(request):
	user = request.user
	pk = request.POST['pk']

	data = {'error': False}
	if user.is_authenticated():
		diagram = get_object_or_404(Diagram, id=pk)
		if diagram.author.id == user.id:
			data['code'] = diagram.text
			data['url'] = diagram.image_url
			data['title'] = diagram.title
		else:
			data['error'] = True
			data['error_message'] = 'Недостаточно прав для данного действия.'
	else:
		data['error'] = True
		data['error_message'] = 'Пользователь не вошел в систему.'
	return JsonResponse(data)

def diagen_main(request):
    return render(request, 'index.html', {'components': DEFAULT_COMPONENTS_TEXT})


def save_diagram_for_user(request):
	data = {'error': False}
	if request.user.is_authenticated():
		code = request.POST['code']
		file_name = build_diagram_from_code(code)
		url = SERV_FULL_ADDRESS + 'static/diagrams/' + file_name
		title = request.POST['title']

		diagram = Diagram.objects.filter(author=request.user, title=title)
		if diagram.count() == 1:
			diagram = diagram[0]
			diagram.image_url = url
			diagram.text = code
			diagram.save()
			data['message'] = 'Диаграмма успешно обновлена.'
		else:
			new_diagram = Diagram.objects.create(title=title, author=request.user, text=code, image_url=url)
			if new_diagram != None:
				data['message'] = 'Диаграмма успешно сохранена.'
			else:
				data['error'] = True
				data['error_message'] = 'Не получилось сохранить диаграмму.'
	else:
		data['error'] = True
		data['error_message'] = 'Пользователь не вошел в систему.'

	return JsonResponse(data)


def delete_user_diagram(request):
	user = request.user
	pk = request.POST['pk']

	data = {'error': False}
	if user.is_authenticated():
		diagram = get_object_or_404(Diagram, id=pk)
		if diagram.author.id == user.id:
			diagram.delete()
		else:
			data['error'] = True
			data['error_message'] = 'Недостаточно прав для данного действия.'
	else:
		data['error'] = True
		data['error_message'] = 'Пользователь не вошел в систему.'
	return JsonResponse(data)


def get_diagram(request):
    responce = {}

    try:
        file_name = build_diagram_from_code(request.POST['code'])
        url = SERV_FULL_ADDRESS + 'static/diagrams/' + file_name
        responce = {'image_url': url}
    except Exception as e:
        responce = {'error': 'true', 'message': str(e)}

    return JsonResponse(responce)


def generate_diagram(request):
    responce = {}
    text = request.POST['text']
    component_types = _parse_text_to_lines(request.POST['component_types'])
    component_names = _parse_text_to_lines(request.POST['component_names'])

    try:
        code = convert_text_to_code(text, component_types, component_names)
        file_name = build_diagram_from_code(code)
        url = SERV_FULL_ADDRESS + 'static/diagrams/' + file_name
        responce = {'code': code, 'image_url': url}
    except Exception as e:
        responce = {'error': 'true', 'message': str(e)}

    return JsonResponse(responce)


def _parse_text_to_lines(text):
    lines = []
    for line in text.split('\n'):
        if _words_number(line) == 1:
            lines.append(line)
    return lines


def _words_number(line):
    words = re.findall(r"[\w]+", line)
    return len(words)
