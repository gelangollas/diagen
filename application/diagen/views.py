from django.shortcuts import render
from django.http import JsonResponse
from diagen.utils.DiagramCreator import build_diagram_from_code
from diagen.utils.TextConverter import convert_text_to_code

SERV_FULL_ADDRESS = 'http://127.0.0.1:8000/'

# Create your views here.
def diagen_main(request):
	return render(request, 'index.html', {})

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

	try:
		code = convert_text_to_code(text)
		file_name = build_diagram_from_code(code)
		url = SERV_FULL_ADDRESS + 'static/diagrams/' + file_name
		responce = {'code': code, 'image_url': url}
	except Exception as e:
		responce = {'error': 'true', 'message': str(e)}

	return JsonResponse(responce)