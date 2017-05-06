from django.shortcuts import render

# Create your views here.
def build_diagram(request):
	return render(request, 'diagen/base.html', context)