import re
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class ViewTests(TestCase):
    def test_index_links_format(self) -> None:
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        content = response.content.decode()

        # Regex to match <a href="...">link_text</a>
        pattern = r'<a href="(?P<href>[^"]+)">(?P<name>[^<]+)</a>'
        links = re.findall(pattern, content)

        self.assertTrue(len(links), 12)

        for href, name in links:
            with self.subTest(link=name):
                month = name.lower()
                # Verify that href matches /challenges/{month}
                expected_href = f"/challenges/{month}"
                self.assertEqual(href, expected_href)

    def test_monthly_challenge_by_numbers(self) -> None:
        test_cases = [
            (1, HTTPStatus.OK, "Eat no meat for the entire month!"),
            (2, HTTPStatus.OK, "Walk for at least 20 minutes every day!"),
            (3, HTTPStatus.OK, "Learn Django for at least 20 minutes every day!"),
            (13, HTTPStatus.NOT_FOUND, "unused"),
        ]

        for month, status, body in test_cases:
            with self.subTest(month=month):
                response = self.client.get(reverse("monthly_challenge_by_number", args=[month]))
                self.assertEqual(response.status_code, status)
                actual = response.content.decode()
                if status.value < 400:
                    self.assertEqual(actual, body)

    def test_monthly_challenges(self) -> None:
        test_cases = [
            ("january", HTTPStatus.OK, "Eat no meat for the entire month!"),
            ("february", HTTPStatus.OK, "Walk for at least 20 minutes every day!"),
            ("march", HTTPStatus.OK, "Learn Django for at least 20 minutes every day!"),
            ("thirteenth_month", HTTPStatus.NOT_FOUND, "unused"),
        ]

        for month, status, body in test_cases:
            with self.subTest(month=month):
                response = self.client.get(reverse("monthly_challenge", args=[month]))
                self.assertEqual(response.status_code, status)
                actual = response.content.decode()
                if status.value < 400:
                    self.assertEqual(actual, body)
