from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm

def lead_list(request):
  leads = Lead.objects.all()
  context = {
    'leads': leads
  }
  return render(request, "leads/lead_list.html", context)

def lead_detail(request, pk):
  lead = Lead.objects.get(id=pk)
  context = {
    'lead': lead
  }
  return render(request, "leads/lead_detail.html", context)

def lead_create(request):
  form = LeadModelForm()
  if request.method == 'POST':
    print('Retrieving a post request')
    # reassigning
    form = LeadModelForm(request.POST)
    if form.is_valid():
      # first_name = form.cleaned_data['first_name']
      # last_name = form.cleaned_data['last_name']
      # age = form.cleaned_data['age']
      # agent = form.cleaned_data['agent']
      # Lead.objects.create(
      #   first_name=first_name,
      #   last_name=last_name,
      #   age=age,
      #   agent=agent
      # ) since we specify the model for the form this is equal to:
      form.save()
      return redirect('/leads')
  context = {
    'form': form
  }
  return render(request, "leads/lead_create.html", context)

def lead_update(request, pk):
  lead = Lead.objects.get(id=pk)
  context = {
    'lead': lead
  }
  return render(request, "leads/lead_update.html", context)
  

# def lead_create(request):
#   form = LeadModelForm()
#   if request.method == 'POST':
#     print('Retrieving a post request')
#     # reassigning
#     form = LeadModelForm(request.POST)
#     if form.is_valid():
#       print("Form is valid")
#       print(form.cleaned_data)
#       first_name = form.cleaned_data['first_name']
#       last_name = form.cleaned_data['last_name']
#       age = form.cleaned_data['age']
#       agent = Agent.objects.first()
#       Lead.objects.create(
#         first_name=first_name,
#         last_name=last_name,
#         age=age,
#         agent=agent
#       )
#       print("created")
#       return redirect('/leads')
#   context = {
#     'form': form
#   }
#   return render(request, "leads/lead_create.html", context)