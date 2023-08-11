import pandas as pd

from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from django.conf import settings

from .forms import EmailForm

# Create your views here.

class EmailtView(View):
    template_name = 'email_form.html'
    
    def get(self, request, *args, **kwargs):
        form = EmailForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data here
            name_column_name = form.cleaned_data['name_column_name']
            email_column_name = form.cleaned_data['email_column_name']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            df = form.cleaned_data['file']

            for index, row in df.iterrows():
                name = row[name_column_name]
                email = row[email_column_name]
                email_content = message.replace('<name>', name)
                send_mail(subject, email_content, settings.EMAIL_HOST_USER, [email])

            # Do something with the form data, such as sending an email or saving to a database
        return render(request, self.template_name, {'form': form})