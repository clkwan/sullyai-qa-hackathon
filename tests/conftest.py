import pytest
import requests
import logging
import pytest_html

BASE_URL = "http://localhost:3000/api"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Hook into the test report
    outcome = yield
    report = outcome.get_result()

    # Attach captured logs to the report
    if call.when == "call":
        caplog = item.funcargs.get("caplog", None)
        if caplog:
            report.extra = getattr(report, 'extra', [])
            report.extra.append(pytest_html.extras.text(caplog.text, name="Captured Logs"))