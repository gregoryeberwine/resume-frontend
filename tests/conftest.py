import os
import pytest
from playwright.sync_api import Page

BASE_URL = os.environ.get("PLAYWRIGHT_BASE_URL", "http://localhost:8000")

@pytest.fixture
def site_visit(page: Page):
    page.goto(BASE_URL)
    return page
