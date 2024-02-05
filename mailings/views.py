from random import sample

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from mailings.forms import ClientForm, MessageForm, SettingsForm, BlogForm
from mailings.models import Client, Message, Settings, Log, Blog


def homepage(request):
    client_count = Client.objects.count()
    message_count = Message.objects.count()
    log_count = Log.objects.count()

    blog_list = Blog.objects.all()
    random_blog = sample(list(blog_list), min(3, blog_list.count()))

    context = {
        "client_count": client_count,
        "message_count" : message_count,
        "log_count" : log_count,
        "random_blog" : random_blog
    }

    return render(request, "mailings/homepage.html", context)


def index(request):
    logs = Log.objects.all()
    context = {"logs": logs}
    return render(request, "mailings/index.html", context)


def success(request):
    return render(request, "mailings/email_success.html")


def no_success(request):
    return render(request, "mailings/email_no_success.html")


def is_superuser(user):
    """ tyhle permissions fungujou jen na funkce """
    return user.is_superuser


def is_moderator(user):
    """ tyhle permissions fungujou jen na funkce """
    return user.groups.filter(name='moderator').exists()


### Client
class ClientListView(ListView):
    """ show all Clients """
    model = Client
    template_name = 'mailings/client_list_view.html'


@user_passes_test(lambda u: is_superuser(u) or is_moderator(u))  # tohle testuje jestli je user moderator
def send_email_to_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    messages = client.messages.all()
    settings = client.settings.all()

    if request.method == 'POST':
        selected_message_id = request.POST.get('selected_message')
        selected_setting_id = request.POST.get('selected_setting')
        # settings_obj = client.settings.get()  # dostat setting pro clienta
        # start_date = settings_obj.start_date  # datum kdy se to zadalo
        # days_passed = (timezone.now().date() - start_date).days  # dnešní datum - dny kdy se to zadalo
        # periodicity = settings_obj.periodicity  # jestli: daily, weekly nebo monthly
        if selected_message_id and selected_setting_id:
            selected_message = get_object_or_404(Message, id=selected_message_id)
            selected_setting = get_object_or_404(Settings, id=selected_setting_id)
            periodicity = selected_setting.periodicity
            start_date = selected_setting.start_date
            days_passed = (timezone.now().date() - start_date).days
            if periodicity == 'daily':
                send_e_mail(client, selected_message, selected_setting)
                return redirect("success")

            elif periodicity == 'weekly':
                if days_passed % 7 == 0:
                    send_e_mail(client, selected_message, selected_setting)
                    return redirect("success")
                else:
                    return redirect("no success")

            elif periodicity == 'monthly':  # srát na jinak dlouhý měsíce monthly je prostě 30 dní
                if days_passed % 30 == 0:  # bacha 0 / 30 == 0, takže se to pošle i dneska
                    send_e_mail(client, selected_message, selected_setting)
                    return redirect("success")
                else:
                    return redirect("no success")

    context = {'client': client, 'messages': messages, 'settings': settings}
    return render(request, 'mailings/send_email_form.html', context)


def send_e_mail(client, selected_message, selected_settings):
    subject = selected_message.subject
    body = selected_message.body

    send_mail(
        f"{subject}",
        f"{body}",
        settings.EMAIL_HOST_USER,
        [client.email]
    )
    log_entry = Log.objects.create(
        client=client,
        status="finished",
        server_response="Email sent successfully",
        email_subject=subject,
        email_body=body
    )


class ClientDetailView(DetailView):
    """ show one Client """
    model = Client
    template_name = "mailings/client_detail.html"


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ update Client """  # |
    # Permission - dát toto sem----------------------
    # v /admin/ vybrat který Permission má která grupa nebo user
    # potom na serveru pokud bude chtít, někdo udělat něco na co nebude mít pravomoce tak bude 403 error
    # do každé classy nasrat <permission_required> = jsou 4 předělaný metody a musí to vypadat takto:
    # <jméno aplikace>.<metoda>_<jméno modelu> ; metody: <add>    <change>   <delete>   <view>
    #                                                 CreateView;UpdateView;DeleteView;DetailView
    model = Client
    form_class = ClientForm
    permission_required = "mailings.change_client"
    template_name = "mailings/client_form.html"

    def get_success_url(self):
        """ come back to client list view """
        return reverse('client_list_view')


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ delete Client """
    model = Client
    permission_required = "mailings.delete_client"
    template_name = "mailings/client_confirm_delete.html"

    def get_success_url(self):
        """ come back to client list view """
        return reverse('client_list_view')


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ create Client """
    model = Client
    form_class = ClientForm
    permission_required = "mailings.add_client"
    template_name = "mailings/client_form.html"

    def get_success_url(self):
        """ come back to client list view """
        return reverse('client_list_view')


### Message
class MessageListView(ListView):
    """ show all Messages """
    model = Message
    template_name = 'mailings/message_list_view.html'


class MessageDetailView(DetailView):
    """ show one Message """
    model = Message
    template_name = "mailings/message_detail.html"


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ update Message """
    model = Message
    form_class = MessageForm
    permission_required = "mailings.change_message"
    template_name = "mailings/message_form.html"

    def get_success_url(self):
        """ come back to message list view """
        return reverse('message_list_view')


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ delete Message """
    model = Message
    permission_required = "mailings.delete_message"
    template_name = "mailings/message_confirm_delete.html"

    def get_success_url(self):
        """ come back to message list view """
        return reverse('message_list_view')


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ create Message """
    model = Message
    form_class = MessageForm
    permission_required = "mailings.add_message"
    template_name = "mailings/message_form.html"

    def get_success_url(self):
        """ come back to message list view """
        return reverse('message_list_view')


### Setings

class SettingsDetailView(DetailView):
    """ show one Settings """
    model = Settings
    template_name = "mailings/settings_detail.html"


class SettingsListView(ListView):
    """ shows all settings"""
    model = Settings
    template_name = 'mailings/settings_list_view.html'


class SettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ update Settings """
    model = Settings
    form_class = SettingsForm
    permission_required = "mailings.change_settings"
    template_name = "mailings/settings_form.html"

    def get_success_url(self):
        """ come back to Settings list view """
        return reverse('settings_list_view')


class SettingsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ delete Settings """
    model = Settings
    permission_required = "mailings.delete_settings"
    template_name = "mailings/settings_confirm_delete.html"

    def get_success_url(self):
        """ come back to settings list view """
        return reverse('settings_list_view')


class SettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Settings
    form_class = SettingsForm
    permission_required = "mailings.add_settings"
    template_name = 'mailings/settings_form.html'

    def get_success_url(self):
        return reverse("settings_list_view")


def client_detail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST' and 'send_email' in request.POST:

        searched_client = Client.objects.filter(name=client.name, surname=client.surname).first()

        if searched_client:
            send_email_to_client(searched_client)
            return render(request, 'mailings/email_sent.html')

    context = {'client': client}
    return render(request, 'mailings/client_detail.html', context)


### Blog
class BlogListView(ListView):
    model = Blog
    template_name = "mailings/blog/blog.html"


class BlogDetailView(DetailView):
    model = Blog
    template_name = "mailings/blog/blog_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_view += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    # permission_required = "blog.change_blog"
    template_name = "mailings/blog/blog_form.html"

    def get_success_url(self):
        return reverse("blog")


class BlogDeleteView(DetailView):
    model = Blog
    # permission_required = "mailings.delete_blog"
    template_name = "mailings/blog/blog_confirm_delete.html"

    def get_success_url(self):
        return reverse("blog")


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    # permission_required = mailings.add_blog
    template_name = "mailings/blog/blog_form.html"

    def get_success_url(self):
        return reverse("blog")
