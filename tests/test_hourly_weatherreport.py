from unittest.mock import patch

import requests

import hourly_weatherreport


class DummyResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


def test_generate_hourly_weather_report_returns_false_when_hourly_key_missing():
    response = DummyResponse({"error": True, "reason": "bad request"})

    with patch("hourly_weatherreport.requests.get", return_value=response):
        assert hourly_weatherreport.generate_hourly_weather_report(12.34, 56.78) is False
