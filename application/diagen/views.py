from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import string
import os
import random

SERV_FULL_ADDRESS = 'http://127.0.0.1:8000/'

# Create your views here.
def diagen_main(request):
	return render(request, 'index.html', {})

def get_diagram(request):
	diagram_url = build_diagram_from_code(request.POST['code'])
	return JsonResponse({'image_url': diagram_url})

def generate_diagram(request):
	result = generate_diagram_from_text(request.POST['text'])
	return JsonResponse(result)


def generate_diagram_from_text(text):
	code = convert_text_to_code(text)
	url = build_diagram_from_code(code)
	result = {'code': code, 'image_url': url}
	return result

def convert_text_to_code(text):
	code = '''@startuml

abstract class AbstractList
abstract AbstractCollection
interface List
interface Collection

List <|-- AbstractList
Collection <|-- AbstractCollection

Collection <|- List
AbstractCollection <|- AbstractList
AbstractList <|-- ArrayList

class ArrayList {
  Object[] elementData
  size()
}

enum TimeUnit {
  DAYS
  HOURS
  MINUTES
}

annotation SuppressWarnings

@enduml
	'''
	return code

PATH_TO_DIAGRAMS_FOLDER = 'diagen/static/diagrams/'
def build_diagram_from_code(code):
	file_name = get_random_name()
	f = open('./'+PATH_TO_DIAGRAMS_FOLDER + file_name + '.txt', 'w')
	f.write(code)
	f.close()
	subprocess.call(['java', '-jar', 'diagen/tools/plantuml/plantuml.jar', PATH_TO_DIAGRAMS_FOLDER+file_name+'.txt'])
	os.remove('./'+PATH_TO_DIAGRAMS_FOLDER + file_name + '.txt')
	return SERV_FULL_ADDRESS+'static/diagrams/'+file_name+'.png'


RANDOM_CHARS = string.ascii_letters + string.digits
def get_random_name(n=17):
	return ''.join([random.choice(RANDOM_CHARS) for i in range(n)])