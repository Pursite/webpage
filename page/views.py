from django.shortcuts import render, redirect
from django.views import View
from page.forms import AthnticateForm
from django.contrib import messages


class PageView(View):
    template_name = 'page.html'

    def get(self, request, *args, **kwargs):
        form = AthnticateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AthnticateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیامتونو گرفتم! ✅")
            return redirect("page-view")  
        return render(request, self.template_name, {'form': form})
