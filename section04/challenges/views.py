import calendar

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

_challenges = [
    "Eat no meat for the entire month!",
    "Walk for at least 20 minutes every day!",
    "Learn Django for at least 20 minutes every day!",
]

monthly_challenges = {
    calendar.month_name[1 + month].lower(): _challenges[month % 3] for month in range(11)
} | {"december": None}


def _list_item(month: str) -> str:
    capitalized_month = month.capitalize()
    month_path = reverse("monthly_challenge", args=[month])
    return f'<li><a href="{month_path}">{capitalized_month}</a></li>'


def index(req: HttpRequest) -> HttpResponse:
    months = list(monthly_challenges.keys())
    return render(req, "challenges/index.html", {"months": months})


# Second argument name must match whatever is used in `urls.py`.
# These act as keyword arguments.
def monthly_challenge_by_number(req: HttpRequest, month: int) -> HttpResponse:
    if 1 <= month <= 12:
        month_name = calendar.month_name[month].lower()
        return monthly_challenge(req, month_name)
    raise Http404()


def monthly_challenge(req: HttpRequest, month: str) -> HttpResponse:
    if month not in monthly_challenges:
        # Looks for a template named 404.html.
        raise Http404()
    return render(
        req,
        "challenges/challenge.html",
        {"month": month, "challenge": monthly_challenges[month]},
    )
