from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
from django.core.mail import send_mail
from django.views import generic
from .models import Lead, Category
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from .decorators import get_role_based_leads, get_categories

class SignupView(generic.CreateView):
  template_name = 'registration/signup.html'
  form_class = CustomUserCreationForm  
  
  def get_success_url(self):
    return reverse('login')

class LandingPageView(generic.TemplateView):
  template_name = 'landing.html'

class LeadListView(LoginRequiredMixin, generic.ListView):
  template_name = 'leads/lead_list.html'
  context_object_name = 'leads'
  
  @get_role_based_leads
  def get_queryset(self):
    return self.queryset.filter(agent__isnull=False)
  
  def get_context_data(self, **kwargs):
    context = super(LeadListView, self).get_context_data(**kwargs)
    user = self.request.user
    if user.is_organisor:
      queryset = Lead.objects.filter(
        organisation=user.userprofile,
        agent__isnull=True
      )
      context.update({
        'unassigned_leads': queryset
      })
    return context

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = 'leads/lead_detail.html'
  queryset = Lead.objects.all()
  context_object_name = 'lead'
  
  # This view fetches only one lead because we're passing generic.DetailView
  @get_role_based_leads
  def get_queryset(self):
    return self.queryset 

class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
  template_name = 'leads/lead_create.html'
  form_class = LeadModelForm
  
  def get_success_url(self):
      return reverse('leads:lead_list')
    
  def form_valid(self, form):
    lead = form.save(commit=False)
    lead.organisation = self.request.user.userprofile
    lead.save()
    send_mail(
      subject='A lead has been created',
      message='Go to the site to see the new lead',
      from_email='test@test.com',
      recipient_list=['test2@test.com']
    )
    # This is what is done on form_valid at CreateView. We are just adding an extra step before above
    return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
  template_name = 'leads/lead_update.html'
  form_class = LeadModelForm
  
  @get_role_based_leads
  def get_queryset(self):
    return self.queryset
  
  def get_success_url(self):
    return reverse('leads:lead_detail', args=[self.object.pk])

class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
  template_name = 'leads/lead_delete.html'
  
  @get_role_based_leads
  def get_queryset(self):
    return self.queryset
  
  def get_success_url(self):
      return reverse('leads:lead_list')
  
class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
  template_name = 'leads/lead_category_update.html'
  form_class = LeadCategoryUpdateForm
  
  @get_role_based_leads
  def get_queryset(self):
    return self.queryset
  
  def get_success_url(self):
    return reverse('leads:lead_detail', args=[self.object.pk])

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
  template_name = 'leads/assign_agent.html'
  form_class = AssignAgentForm
  
  # Pass extra args into the form
  def get_form_kwargs(self, **kwargs):
    kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
    kwargs.update({
      'request': self.request
    })
    return kwargs
  
  def get_success_url(self):
    return reverse('leads:lead_list')
  
  # Because this is not a model form we can't use form.save(), a save method would have to be defined on the form
  def form_valid(self, form):
    agent = form.cleaned_data['agent']
    lead = Lead.objects.get(id=self.kwargs['pk'])
    lead.agent = agent
    lead.save()
    return super(AssignAgentView, self).form_valid(form)
  
class CategoryListView(LoginRequiredMixin, generic.ListView):
  template_name = 'leads/category_list.html'
  context_object_name = 'category_list'
  
  def get_context_data(self, **kwargs):
    context = super(CategoryListView, self).get_context_data(**kwargs)
    user = self.request.user
    
    if user.is_organisor:
      queryset = Lead.objects.filter(
        organisation = user.userprofile
      )
    else:
      queryset = Lead.objects.filter(
        organisation = Lead.objects.filter(
          organisation = user.agent.organisation
        )
      )
    context.update({
      'unassigned_lead_count': queryset.filter(category__isnull=True).count()
    })
    return context
  
  @get_categories
  def get_queryset(self):
    return self.queryset
  
class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = 'leads/category_detail.html'
  context_object_name = 'category'
  
  # Everything that is done below can be achieved by just calling the context object + leads.all on the template due to the FK relation
  
  # def get_context_data(self, **kwargs):
  #   context = super(CategoryDetailView, self).get_context_data(**kwargs)
  #   # get_objects() is a method for the DetailView which fetches the object for the view, thus we can use it like so
  #   # leads = Lead.objects.filter(category=self.get_objects())
  #   # **reverse lookup** leads=.lead_set can be used on the object because the category was set as a FK for the lead model
  #   # lead_set can be replaced by leads because that is the related_name assigned to the relationship between the two models
  #   leads = self.get_object().leads  .all()
  #   context.update({
  #     'leads': leads
  #   })
  #   return context
  
  @get_categories
  def get_queryset(self):
    # This is assigned to the context object
    return self.queryset
  
# Landing page handled as function
# def landing_page(request):
#   return render(request, "landing.html")
# Lead list page handled as function
# def lead_list(request):
#   leads = Lead.objects.all()
#   context = {
#     'leads': leads
#   }
#   return render(request, 'leads/lead_list.html', context)
# Lead detail page handled as function
# def lead_detail(request, pk):
#   lead = Lead.objects.get(id=pk)
#   context = {
#     'lead': lead
#   }
#   return render(request, 'leads/lead_detail.html', context)
# Lead create page handled as function
# def lead_create(request):
#   form = LeadModelForm()
#   if request.method == 'POST':
#     print('Retrieving a post request')
#     # reassigning
#     form = LeadModelForm(request.POST)
#     if form.is_valid():
#       # first_name = form.cleaned_data['first_name']
#       # last_name = form.cleaned_data['last_name']
#       # age = form.cleaned_data['age']
#       # agent = form.cleaned_data['agent']
#       # Lead.objects.create(
#       #   first_name=first_name,
#       #   last_name=last_name,
#       #   age=age,
#       #   agent=agent
#       # ) since we specify the model for the form this is equal to:
#       form.save()
#       return redirect('/leads')
#   context = {
#     'form': form
#   }
#   return render(request, "leads/lead_create.html", context)
# Lead update page handled as function
# def lead_update(request, pk):
#   lead = Lead.objects.get(id=pk)
#   form = LeadModelForm(instance=lead)
#   if request.method == 'POST':
#     # reassigning
#     form = LeadModelForm(request.POST, instance=lead)
#     if form.is_valid():
#       form.save()
#       return redirect(f'/leads/{pk}')
#   context = {
#     'form': form,
#     'lead': lead
#   }
#   return render(request, "leads/lead_update.html", context)

# Lead delete page handled as function
# def lead_delete(_, pk):
#   lead = Lead.objects.get(id=pk)
#   lead.delete()
#   return redirect ('/leads')