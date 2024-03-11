from django.urls import path

from . import views

urlpatterns = [
    path("", views.add_item, name="add_item"),
    path(
        "add_item_result/<int:add_request_id>",
        views.add_item_result,
        name="add_item_result",
    ),
    path("manual_add_item", views.manual_add_item, name="manual_add_item"),
]
