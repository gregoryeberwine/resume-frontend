import re
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"


def test_has_title(page: Page):
    page.goto(BASE_URL)

    # expects title to contain this string
    expect(page).to_have_title(re.compile("Resume"))


def test_email_link(page: Page):
    page.goto(BASE_URL)

    # expects email link to point to my email
    email_link = page.get_by_role("link", name="geberwine@gmail.com")
    expect(email_link).to_have_attribute("href", "mailto:geberwine@gmail.com")


def test_name_heading(page: Page):
    page.goto(BASE_URL)

    # expects full name to appear as the top-level heading
    heading = page.get_by_role("heading", name="Gregory Eberwine", level=1)
    expect(heading).to_be_visible()


def test_github_link(page: Page):
    page.goto(BASE_URL)

    # expects GitHub link to point to the correct profile
    github_link = page.get_by_role("link", name="GitHub")
    expect(github_link).to_have_attribute("href", "https://github.com/gregoryeberwine")


def test_linkedin_link(page: Page):
    page.goto(BASE_URL)

    # expects LinkedIn link to point to the correct profile
    linkedin_link = page.get_by_role("link", name="LinkedIn")
    expect(linkedin_link).to_have_attribute("href", re.compile(r"linkedin\.com/in/gregory-eberwine"))


def test_contact_has_phone_number(page: Page):
    page.goto(BASE_URL)

    # expects phone number to appear in the contact section
    contact = page.locator("#contact")
    expect(contact).to_have_text(re.compile(r"\(\d{3}\)\s*\d{3}-\d{4}"))


def test_has_summary_section(page: Page):
    page.goto(BASE_URL)

    expect(page.get_by_role("heading", name="SUMMARY")).to_be_visible()


def test_has_experience_section(page: Page):
    page.goto(BASE_URL)

    expect(page.get_by_role("heading", name="EXPERIENCE")).to_be_visible()


def test_has_certifications_section(page: Page):
    page.goto(BASE_URL)

    expect(page.get_by_role("heading", name="CERTIFICATIONS")).to_be_visible()


def test_has_skills_section(page: Page):
    page.goto(BASE_URL)

    expect(page.get_by_role("heading", name="TECHNICAL SKILLS")).to_be_visible()


def test_has_education_section(page: Page):
    page.goto(BASE_URL)

    expect(page.get_by_role("heading", name="EDUCATION")).to_be_visible()


def test_visitor_counter_element_exists(page: Page):
    page.goto(BASE_URL)

    # expects the counter element to be present in the footer
    counter = page.locator("#visitorCounter")
    expect(counter).to_be_attached()
