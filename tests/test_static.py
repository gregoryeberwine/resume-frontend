import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("http://localhost:8000")

    # expects title to contain this string
    expect(page).to_have_title(re.compile("Resume"))

def test_email_link(page: Page):
    page.goto("http://localhost:8000")

    # expects email link to point to my email
    email_link = page.get_by_role("link", name="geberwine@gmail.com")
    expect(email_link).to_have_attribute("href", "mailto:geberwine@gmail.com")
