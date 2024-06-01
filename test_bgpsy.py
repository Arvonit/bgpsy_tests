from playwright.sync_api import Page, expect
import pytest

def test_has_title(page: Page):
    """ 
    A basic test to ensure Playwright is working as expected. 
    """
    page.goto("https://bgpy.engr.uconn.edu/")
    expect(page).to_have_title("BGPy")

def test_add_negative_as(page: Page):
    """
    Ensures BGPsy will not an AS to be added to graph that has a negative ASN.
    """
    page.goto("https://bgpy.engr.uconn.edu/")

    # Attempt to add a node with a negative ASN
    page.get_by_role("button", name="Add AS").click()
    page.locator('input[type="number"]').fill("-1")
    page.get_by_role("button", name="Add", exact=True).click()
    
    try:
        # Wait for the toast to appear within a second
        toast_section = page.get_by_role("status")
        toast_section.wait_for(state='visible', timeout=1000)

        # Check if the error message is that an ASN cannot be negative
        assert "AS Number cannot be negative" in toast_section.inner_text()
    except TimeoutError:
        # Toast did not show up
        pytest.fail("Timeout waiting for toast")
    except AssertionError:
        # Different error message
        pytest.fail("The expected toast message 'AS Number cannot be negative' "
                    "was not found")
