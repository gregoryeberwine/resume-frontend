import re
import os
from playwright.sync_api import Page, expect

BASE_URL = os.environ.get("PLAYWRIGHT_BASE_URL", "https://gregoryeberwine.com")

def test_counter_number(page: Page):
    page.goto("BASE_URL")

    # expects visitor counter to be a number
    counter = page.locator("#visitorCounter")
    expect(counter).not_to_have_text("")
    expect(counter).to_have_text(re.compile(r"\d+"))

def test_counter_increments(page: Page):
    page.goto("BASE_URL")
    
    # expects visitor counter value to change after each reload
    counter = page.locator("#visitorCounter")
    expect(counter).to_have_text(re.compile(r"\d+"))
    first_count = int(counter.text_content())
    page.reload()
    expect(counter).to_have_text(re.compile(r"\d+"))
    second_count = int(counter.text_content())
    assert second_count > first_count