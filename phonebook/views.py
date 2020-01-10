from itertools import zip_longest

from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmailForm, OsobaForm, TelefonForm
from .models import Email, Osoba, Telefon


def index_view(request):
    if request.method == "POST":
        handle_search_and_index_post(request)
        return redirect('index')
    else:
        osoby = [(o,
                  zip_longest(
                      Telefon.objects.filter(osoba_id=o.pk),
                      Email.objects.filter(osoba_id=o.pk))
                  )
                 for o in Osoba.objects.all()]

        context = {'osoby': osoby,
                   'telefon_form': TelefonForm(),
                   'email_form': EmailForm()}
    return render(request, 'phonebook/index.html', context)


def search_view(request):
    if request.method == 'GET':
        if request.GET['searchfield'] == 'osoba':
            osoby = (Osoba.objects.filter(
                         imie__icontains=request.GET['query']) |
                     Osoba.objects.filter(
                         nazwisko__icontains=request.GET['query'])
                    )

            osoby = [(o,
                      zip_longest(
                          Telefon.objects.filter(osoba_id=o.pk),
                          Email.objects.filter(osoba_id=o.pk))
                      )
                     for o in osoby]
        elif request.GET['searchfield'] == 'telefon':
            telefony = Telefon.objects.filter(
                           telefon__icontains=request.GET['query']
                       )
            osoby = [(Osoba.objects.get(pk=t.osoba_id),
                      zip_longest(
                          Telefon.objects.filter(osoba_id=t.osoba_id),
                          Email.objects.filter(osoba_id=t.osoba_id))
                      )
                     for t in telefony]
        elif request.GET['searchfield'] == 'email':
            emaile = Email.objects.filter(
                         email__icontains=request.GET['query']
                     )
            osoby = [(Osoba.objects.get(pk=e.osoba_id),
                      zip_longest(
                          Telefon.objects.filter(osoba_id=e.osoba_id),
                          Email.objects.filter(osoba_id=e.osoba_id))
                     )
                     for e in emaile]

        context = {'osoby': osoby,
                   'telefon_form': TelefonForm(),
                   'email_form': EmailForm()
                  }
        return render(request, 'phonebook/search.html', context)
    elif request.method == "POST":
        handle_search_and_index_post(request)
        return redirect('index')
    else:
        return redirect('index')


def add_view(request):
    if request.method == "POST":
        form = OsobaForm(request.POST)
        if form.is_valid():
            osoba = form.save()
            return redirect('index')
    else:
        form = OsobaForm()
    return render(request, 'phonebook/add.html', {'form': form})


def edit_view(request, osoba_id):
    if request.method == "POST":
        o = Osoba.objects.get(pk=osoba_id)
        form = OsobaForm(request.POST, instance=o)
        if form.is_valid():
            osoba = form.save()
            return redirect('index')
    else:
        osoba = Osoba.objects.get(pk=osoba_id)
        form = OsobaForm(instance=osoba)
    return render(request, 'phonebook/edit.html', {'form': form})


def delete_view(request, osoba_id):
    try:
        osoba = get_object_or_404(Osoba, pk=osoba_id)
        osoba.delete()
    except ProtectedError:
        return HttpResponse('Nie mozna usunac, poniewaz osoba'
                            'posiada telefony lub emaile')
    return redirect('index')


def handle_search_and_index_post(request):
    if 'telefon' in request.POST:
        form = TelefonForm(request.POST)

        if form.is_valid():
            telefon = Telefon.objects.create(
                osoba_id=request.POST['osoba'],
                telefon=request.POST['telefon']
            )
            telefon.save()
    elif 'email' in request.POST:
        form = EmailForm(request.POST)

        if form.is_valid():
            email = Email.objects.create(
                osoba_id=request.POST['osoba'],
                email=request.POST['email']
            )
            email.save()
    elif 'del_fon' in request.POST:
        Telefon.objects.get(pk=request.POST['del_fon']).delete()
    elif 'del_mail' in request.POST:
        Email.objects.get(pk=request.POST['del_mail']).delete()
