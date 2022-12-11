from django.shortcuts import render
from .forms import PlayerInputForm

# Create your views here.

# This home function just redirects to home.html template, the main template 
def home(request):
    """View function for home page of site."""

    # Create an empty context and render the template with it
    context = {}
    return render(request, 'home.html', context=context)


def input(request):

    description=""

    # Request with the form created to insert the query
    if request.method == 'POST':
        form = PlayerInputForm(request.POST)

    else:
        form = PlayerInputForm()


    # Create the context with the information and render the template with it
    context = {
        'form': form,
        # 'description': description,
    }

    return render(request, 'input.html', context)



def output(request):

    error_case = ""

    # No error case situation 
    if request.method == 'POST':
        form = PlayerInputForm(request.POST)
        if form.is_valid():
            # form.save(commit=True)
            # print(form.cleaned_data())
            return render(request, 'output.html', {'result': form.cleaned_data})
    else:
        form = PlayerInputForm()

    # Create the context with the information and render the template with it
    context = {
        'error_case': error_case
    }

    return render(request, 'output.html', context)
