import re
from playwright.sync_api import Page, expect

def test_counter_number(page: Page):
    page.goto("https://gregoryeberwine.com")

    # expects visitor counter to be a number
    counter = page.locator("#visitorCounter")
    expect(counter).not_to_have_text("")
    expect(counter).to_have_text(re.compile(r"\d+"))

def test_counter_increments(page: Page):
    page.goto("https://gregoryeberwine.com")
    
    # expects visitor counter value to change after each reload
    counter = page.locator("#visitorCounter")
    expect(counter).to_have_text(re.compile(r"\d+"))
    first_count = int(counter.text_content())
    page.reload()
    expect(counter).to_have_text(re.compile(r"\d+"))
    second_count = int(counter.text_content())
    assert second_count > first_count