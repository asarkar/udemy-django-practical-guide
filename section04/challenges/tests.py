import calendar
import re
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    """Tests for the index view, ensuring links are generated correctly."""

    def test_index_link_format(self) -> None:
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        content = response.content.decode()

        # Match <a href="...">Text</a>
        pattern = r'<a href="(?P<href>[^"]+)">(?P<name>[^<]+)</a>'
        links = re.findall(pattern, content)

        # 12 months + "All Challenges"
        self.assertEqual(len(links), 13)

        for href, name in links:
            with self.subTest(link=name):
                if name == "All Challenges":
                    self.assertEqual(href, "/challenges/")
                else:
                    month = name.lower()
                    expected_href = f"/challenges/{month}"
                    self.assertEqual(href, expected_href)


class MonthlyChallengeNumberHappyPathTests(TestCase):
    """Happy-path tests for numeric monthly challenge URLs returning 200 OK."""

    def test_numeric_months_valid(self) -> None:
        valid_cases = [
            (1, "Eat no meat for the entire month!"),
            (2, "Walk for at least 20 minutes every day!"),
            (3, "Learn Django for at least 20 minutes every day!"),
            (12, "There is no challenge for this month yet!"),
        ]

        for month, expected_text in valid_cases:
            with self.subTest(month=month):
                url = reverse("monthly_challenge_by_number", args=[month])
                response = self.client.get(url)

                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertContains(response, calendar.month_name[month])
                self.assertContains(response, expected_text)


class MonthlyChallengeNumberErrorTests(TestCase):
    """Error-path tests for numeric monthly challenge URLs returning 404."""

    def test_numeric_months_invalid(self) -> None:
        invalid_months = [0, 13, 999]

        for month in invalid_months:
            with self.subTest(month=month):
                url = reverse("monthly_challenge_by_number", args=[month])
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        # `reverse` doesn't accept negative values, test as raw URLs.
        response = self.client.get("/challenges/-1")
        self.assertEqual(response.status_code, 404)


class MonthlyChallengeTextHappyPathTests(TestCase):
    """Happy-path tests for text-based monthly challenge URLs returning 200 OK."""

    def test_valid_months(self) -> None:
        test_cases = [
            ("january", "Eat no meat for the entire month!"),
            ("february", "Walk for at least 20 minutes every day!"),
            ("march", "Learn Django for at least 20 minutes every day!"),
            ("december", "There is no challenge for this month yet!"),
        ]

        for month, expected_text in test_cases:
            with self.subTest(month=month):
                url = reverse("monthly_challenge", args=[month])
                response = self.client.get(url)

                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertContains(response, month.capitalize())
                self.assertContains(response, expected_text)


class MonthlyChallengeTextErrorTests(TestCase):
    """Error-path tests for invalid text-based monthly challenge URLs."""

    def test_invalid_months(self) -> None:
        invalid_months = [
            "thirteenth_month",
            "notamonth",
            "foobar",
            "JAnuAry",
        ]

        for month in invalid_months:
            with self.subTest(month=month):
                url = reverse("monthly_challenge", args=[month])
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
