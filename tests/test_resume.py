import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://gregoryeberwine.com/")

    # expects title to contain this string
    expect(page).to_have_title(re.compile("Resume"))