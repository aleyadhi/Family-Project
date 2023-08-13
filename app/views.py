from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from app.models import Family, Details
from datetime import date
from app.forms import FamilyForm, FamilyUpdateForm, FamilyDetialsForm
from django.db.models import Q

# Create your views here.

@login_required
def home_view(request):
    context = {
         'data' : {
             'name': 'Samran',
             'phone': '0507723276',
             'car': 'Camry 2000',
             'job': 'goverment employee',
             'birthdate': '1973-7-30',
              },
         }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

@login_required
def family_view(request):
    if request.GET:
        lookups = Q(name__contains=request.GET['q']) | Q(phone__contains=request.GET['q'])
        all_family = Family.objects.filter(lookups)
    else:
        all_family = Family.objects.all()
    context = {
     'all_family' : all_family,   
    }
    template = loader.get_template('family.html')
    return HttpResponse(template.render(context, request))

@login_required
def create_view(request):
    form = FamilyForm(request.POST or None)
    context = {
        'form' : form,
    }
    if request.method == 'POST':
        if form.is_valid():
            object = form.save(commit=False)
            object.user = request.user
            object.save()
            context['form'] = FamilyForm()
            context['object'] = object
            context['created'] = True
    return render(request, 'create.html', context=context)

@login_required
def details_view(request, slug=None):
    hx_url = reverse('family:hx-details', kwargs={'slug': slug})
    context = {
        'hx_url': hx_url,
    }
    template = loader.get_template('details.html')
    return HttpResponse(template.render(context, request))

@login_required
def details_hx_view(request, slug=None):
    if not request.htmx:
        raise Http404
    try:
        person = Family.objects.get(slug=slug, user=request.user)
    except:
        person = None
    if person is None:
        return HttpResponse("Not Found")
    age = int((date.today() - person.birth_date).days / 365)
    context = {
        'person': person,
        'age': age,
    }
    template = loader.get_template('partials/details.html')
    return HttpResponse(template.render(context, request))

@login_required
def update_view(request, slug=None):
    person =  get_object_or_404(Family, slug=slug)
    person.user = request.user
    form = FamilyUpdateForm(request.POST or None, instance=person)
    new_detail_url = reverse('family:hx-detail-create', kwargs={'slug': slug})
    # for Formset editting details
    # FamilyDetialsFormSet = modelformset_factory(Details, form=FamilyDetialsForm, extra=0)
    # qs = person.details_set.all()
    # formset = FamilyDetialsFormSet(request.POST or None, queryset=qs)
    context = {
        'form': form,
        # 'formset': formset,
        'person': person,
        'new_detail_url': new_detail_url,
    }
    if form.is_valid():
        form.save()
        context['message'] = 'The changes have been made'
    # To save formset Details
    # if all([form.is_valid(), formset.is_valid()]):
    #     parent = form.save(commit=False)
    #     parent.save()
    #     for form in formset:
    #         child = form.save(commit=False)
    #         child.family = parent
    #         if child.car and child.education:
    #             child.save()
    #     context['message'] = 'The changes have been made'
    if request.htmx:
        return render(request, 'forms.html', context=context)
    return render(request, 'update.html', context=context)

@login_required
def details_update_hx_view(request, slug=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_person = Family.objects.get(slug=slug, user=request.user)
    except:
        parent_person = None
    if parent_person is None:
        return HttpResponse("Not Found")
    instance = None
    if id is not None:
        try:
            instance = Details.objects.get(family=parent_person, id=id)
        except:
            instance = None
    form = FamilyDetialsForm(request.POST or None, instance=instance)
    url = reverse('family:hx-detail-create', kwargs={'slug': slug})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        'url': url,
        'form': form,
        'object': instance,
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.family = parent_person
        new_obj.save()
        context['object'] = new_obj
        return render(request, 'detail-inline.html', context)
    
    return render(request, 'partials/detail-form.html', context)
