import calendar

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.urls import reverse

_challenges = [
    "Eat no meat for the entire month!",
    "Walk for at least 20 minutes every day!",
    "Learn Django for at least 20 minutes every day!",
]

monthly_challenges = {
    calendar.month_name[1 + month].lower(): _challenges[month % 3] for month in range(12)
}


def _list_item(month: str) -> str:
    capitalized_month = month.capitalize()
    month_path = reverse("monthly_challenge", args=[month])
    return f'<li><a href="{month_path}">{capitalized_month}</a></li>'


def index(_: HttpRequest) -> HttpResponse:
    list_items = ""
    for month in monthly_challenges:
        list_items += _list_item(month)
    return HttpResponse(f"<ul>{list_items}</ul>")


# Second argument name must match whatever is used in `urls.py`.
# These act as keyword arguments.
def monthly_challenge_by_number(_: HttpRequest, month: int) -> HttpResponse:
    if 1 <= month <= 12:
        month_name = calendar.month_name[month].lower()
        return HttpResponse(monthly_challenges[month_name])
    return HttpResponseNotFound(f"Month '{month}' is not supported")


def monthly_challenge(_: HttpRequest, month: str) -> HttpResponse:
    if month not in monthly_challenges:
        return HttpResponseNotFound(f"Month '{month}' is not supported")
    return HttpResponse(monthly_challenges[month])
