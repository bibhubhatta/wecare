from django.http import Http404
from django.shortcuts import render, redirect

from .models import (
    AutoAddRequestForm,
    AutoAddRequest,
    ManualAddRequestForm,
)


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

    if add_request.success is False:
        form = ManualAddRequestForm()
        form.fields["upc"].initial = add_request.upc
        form.fields["item_name"].widget.attrs["autofocus"] = "autofocus"
        post_url = "manual_add_item"
    else:
        form = AutoAddRequestForm()
        post_url = "add_item"

    return render(
        request,
        "ui/add_result.html",
        {
            "add_request": add_request,
            "add_request_form": form,
            "post_url": post_url,
        },
    )


def manual_add_item(request):
    if request.method == "POST":
        form = ManualAddRequestForm(request.POST)
        if form.is_valid():
            add_request = form.save()
            return redirect("add_item_result", add_request_id=add_request.id)
