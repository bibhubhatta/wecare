from django.http import Http404
from django.shortcuts import render, redirect

from .models import AutoAddRequestForm, AutoAddRequest, ManualAddRequestForm


def add_item(request):
    form = AutoAddRequestForm()

    if request.method == "POST":
        form = AutoAddRequestForm(request.POST)
        if form.is_valid():
            add_request = form.save()
            return redirect("add_item_result", add_request_id=add_request.id)

    return render(request, "ui/add_item.html", {"auto_add_request_form": form})


def add_item_result(request, add_request_id):

    try:
        add_request = AutoAddRequest.objects.get(pk=add_request_id)
    except AutoAddRequest.DoesNotExist:
        raise Http404("Add request does not exist")

    return render(
        request,
        "ui/add_result.html",
        {
            "add_request": add_request,
            "auto_add_request_form": AutoAddRequestForm(),
            "manual_add_request_form": ManualAddRequestForm(),
        },
    )
