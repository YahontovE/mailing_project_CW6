from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.models import Blog
from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Client, Mailing, MessageMailing


def home(request):
    blog = Blog.objects.all()
    mailing_is_active = Mailing.objects.filter(status='started')
    client_mailing = Client.objects.all()
    unique_clients = client_mailing.values_list('email', flat=True).distinct()
    random_articles = sample(list(blog), k=min(len(blog), 3))

    context = {
        'random_articles': random_articles,
        'total_mailings': len(client_mailing),
        'active_mailings': len(mailing_is_active),
        'unique_clients': len(unique_clients)
    }

    return render(request, 'mailing/home.html', context)


#####################################################CLIENTS############################################################

class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client')


#####################################################Mailing############################################################

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mail_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        for mailing in context['object_list']:
            message_mail = mailing.messagemailing_set.first()
            if message_mail:
                mailing.active_version_title = message_mail.title
                mailing.active_version_body = message_mail.body
            else:
                mailing.active_version_title = 'отсутсвует'
                mailing.active_version_title = None

        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['client'].queryset = Client.objects.filter(user=self.request.user)

        return form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        message_formset = inlineformset_factory(Mailing, MessageMailing, form=MessageForm, extra=1)

        if self.request.method == 'POST':
            formset = message_formset(self.request.POST, instance=self.object)
        else:
            formset = message_formset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        form.instance.user = self.request.user
        self.object = form.save()

        if formset.is_valid():
            #form.instance.user = self.request.user
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        message_formset = inlineformset_factory(Mailing, MessageMailing, form=MessageForm, extra=0)

        if self.request.method == 'POST':
            formset = message_formset(self.request.POST, instance=self.object)
        else:
            formset = message_formset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing')
