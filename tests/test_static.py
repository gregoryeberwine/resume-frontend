import re
from playwright.sync_api import Page, expect


def test_has_title(site_visit: Page):
    expect(site_visit).to_have_title(re.compile("Resume"))


def test_email_link(site_visit: Page):
    # expects email link to point to my email
    email_link = site_visit.get_by_role("link", name="geberwine@gmail.com")
    expect(email_link).to_have_attribute("href", "mailto:geberwine@gmail.com")


def test_name_heading(site_visit: Page):
    # expects full name to appear as the top-level heading
    heading = site_visit.get_by_role("heading", name="Gregory Eberwine", level=1)
    expect(heading).to_be_visible()


def test_github_link(site_visit: Page):
    # expects GitHub link to point to the correct profile
    github_link = site_visit.get_by_role("link", name="GitHub")
    expect(github_link).to_have_attribute("href", "https://github.com/gregoryeberwine")


def test_linkedin_link(site_visit: Page):
    # expects LinkedIn link to point to the correct profile
    linkedin_link = site_visit.get_by_role("link", name="LinkedIn")
    expect(linkedin_link).to_have_attribute("href", re.compile(r"linkedin\.com/in/gregory-eberwine"))

def test_has_summary_section(site_visit: Page):
    expect(site_visit.get_by_role("heading", name="SUMMARY")).to_be_visible()


def test_has_experience_section(site_visit: Page):
    expect(site_visit.get_by_role("heading", name="EXPERIENCE")).to_be_visible()


def test_has_certifications_section(site_visit: Page):
    expect(site_visit.get_by_role("heading", name="CERTIFICATIONS")).to_be_visible()


def test_has_skills_section(site_visit: Page):
    expect(site_visit.get_by_role("heading", name="TECHNICAL SKILLS")).to_be_visible()


def test_has_education_section(site_visit: Page):
    expect(site_visit.get_by_role("heading", name="EDUCATION")).to_be_visible()


def test_visitor_counter_element_exists(site_visit: Page):
    # expects the counter element to be present in the footer
    counter = site_visit.locator("#visitorCounter")
    expect(counter).to_be_attached()
