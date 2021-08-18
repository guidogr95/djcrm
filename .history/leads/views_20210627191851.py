from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm

class LandingPageView(TemplateView):
  template_name = 'landing.html'

def landing_page(request):
  return render(request, "landing.html")

class LeadListView(ListView):
  template_name = 'leads/lead_list.html'
  queryset = Lead.objects.all()

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
  form = LeadModelForm(instance=lead)
  if request.method == 'POST':
    print('Retrieving a post request')
    # reassigning
    form = LeadModelForm(request.POST, instance=lead)
    if form.is_valid():
      form.save()
      return redirect(f'/leads/{pk}')
  context = {
    'form': form,
    'lead': lead
  }
  return render(request, "leads/lead_update.html", context)

def lead_delete(request, pk):
  lead = Lead.objects.get(id=pk)
  lead.delete()
  return redirect ('/leads')

# def lead_update(request, pk):
#   lead = Lead.objects.get(id=pk)
#   form = LeadForm()
#   if request.method == 'POST':
#     form = LeadForm(request.POST)
#     if form.is_valid():
#       first_name = form.cleaned_data['first_name']
#       last_name = form.cleaned_data['last_name']
#       age = form.cleaned_data['age']
#       lead.first_name = first_name
#       lead.last_name = last_name
#       lead.age = age
#       # commit changes to db
#       lead.save()
#       return redirect(f'/leads/{pk}')
#   context = {
#     'lead': lead,
#     'form': form
#   }
#   return render(request, "leads/lead_update.html", context)
  

# def lead_create(request):
  # form = LeadModelForm()
  # if request.method == 'POST':
  #   print('Retrieving a post request')
  #   # reassigning
  #   form = LeadModelForm(request.POST)
  #   if form.is_valid():
  #     print("Form is valid")
  #     print(form.cleaned_data)
  #     first_name = form.cleaned_data['first_name']
  #     last_name = form.cleaned_data['last_name']
  #     age = form.cleaned_data['age']
  #     agent = Agent.objects.first()
  #     Lead.objects.create(
  #       first_name=first_name,
  #       last_name=last_name,
  #       age=age,
  #       agent=agent
  #     )
  #     print("created")
  #     return redirect('/leads')
#   context = {
#     'form': form
#   }
#   return render(request, "leads/lead_create.html", context)