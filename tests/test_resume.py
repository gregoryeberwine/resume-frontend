import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://gregoryeberwine.com/")

    # expects title to contain this string
    expect(page).to_have_title(re.compile("Resume"))

def test_email_link(page: Page):
    page.goto("https://gregoryeberwine.com/")

    # expects email link to point to my email
    email_link = page.get_by_role("link", name="geberwine@gmail.com")
    expect(email_link).to_have_attribute("href", "mailto:geberwine@gmail.com")

def test_counter_number(page: Page):
    page.goto("https://gregoryeberwine.com/")

    # expects visitor counter to be a number
    counter = page.locator("#visitorCounter")
    expect(counter).not_to_have_text("")
    expect(counter).to_have_text(re.compile(r"\d+"))

def test_counter_increments(page: Page):
    page.goto("https://gregoryeberwine.com/")
    
    # expects visitor counter value to change after each reload
    counter = page.locator("#visitorCounter")
    expect(counter).to_have_text(re.compile(r"\d+"))
    first_count = int(counter.text_content())
    page.reload()
    expect(counter).to_have_text(re.compile(r"\d+"))
    second_count = int(counter.text_content())
    assert second_count > first_count