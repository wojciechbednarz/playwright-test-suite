from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from playwright._impl._errors import Error as PlaywrightError
import re
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CareersPage:
    """Class representing the careers page of the website.
    Provides methods to interact with the job search functionality,
    including searching for jobs, filtering by location and job type,
    and retrieving job listings."""

    async def _take_error_screenshot(self, error_type: str) -> None:
        """Takes a screenshot of the current page state for debugging purposes.
        
        Args:
            error_type (str): Type of error for the screenshot filename
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"error_screenshots/{error_type}_{timestamp}.png"
            os.makedirs("error_screenshots", exist_ok=True)
            await self.page.screenshot(path=screenshot_path)
            logger.info("Saved %s screenshot to %s", error_type, screenshot_path)
        except PlaywrightError as screenshot_error:
            logger.error("Failed to take %s screenshot: %s", error_type, screenshot_error)

    def __init__(self, page: Page):
        """Initializes the CareersPage with a Playwright Page object.
        Args:
            page (Page): The Playwright Page object to interact with the careers page.
        """
        self.page = page
        self.url = "https://www.epam.com/careers"
        self.search_input = page.locator("#new_form_job_search-keyword")
        self.find_button = page.get_by_role("button", name="Find")
        self.location_filter = page.locator(
            ".select2-selection__rendered[role='textbox']"
        )
        self.all_jobs_on_page = page.locator("//ul/li//div//h5//a")
        self.no_results_message = page.locator("div[role='alert']")
        self.hamburger_menu = page.locator(".hamburger-menu-ui.hamburger-menu-ui-23")
        self.skills_filter = page.locator(".default-label")

    async def navigate(self):
        """Navigates to the careers page and waits for it to load."""
        try:
            logger.info("Navigating to careers page...")
            # Navigate with a longer timeout and wait for load
            await self.page.goto(self.url, wait_until="load", timeout=30000)
            logger.info("Navigated to careers page successfully")

            # Check for human verification iframe
            try:
                # Common selectors for verification iframes
                verification_selectors = [
                    "iframe[title*='challenge']",
                    "iframe[title*='verify']",
                    "iframe[src*='captcha']",
                    "iframe[src*='recaptcha']",
                    "#challenge-stage",
                    "#challenge-running",
                ]

                for selector in verification_selectors:
                    try:
                        frame = await self.page.wait_for_selector(
                            selector, timeout=5000
                        )
                        if frame:
                            logger.info(
                                "Human verification detected, waiting for completion..."
                            )
                            # Wait for verification to complete (timeout after 2 minutes)
                            await self.page.wait_for_selector(
                                selector, state="hidden", timeout=120000
                            )
                            logger.info("Human verification completed")
                            break
                    except PlaywrightTimeoutError:
                        continue

            except PlaywrightTimeoutError:
                logger.debug("No verification frame found, proceeding...")

            # Accept cookies if present
            try:
                # Try multiple cookie accept button selectors
                cookie_selectors = [
                    "button[id*='onetrust-accept']",
                    "button[id*='cookie-accept']",
                    "[aria-label*='Accept']",
                    "button[contains(text(), 'Accept')]",
                    ".cookie-consent button",
                    "#onetrust-accept-btn-handler",
                ]

                for cookie_selector in cookie_selectors:
                    try:
                        button = self.page.locator(cookie_selector)
                        if await button.is_visible(timeout=2000):
                            await button.click()
                            logger.info(
                                "Accepted cookies using selector: %s", cookie_selector
                            )
                            await self.page.wait_for_timeout(1000)
                            break
                    except PlaywrightTimeoutError:
                        continue

            except PlaywrightError as e:
                logger.debug("Error handling cookie banner: %s", e)

            # Wait for initial page content and log the page state
            await self.page.wait_for_selector("body", timeout=5000)

            # Debug: Log current URL to verify redirection
            current_url = self.page.url
            logger.info("Current page URL: %s", current_url)

            # Try multiple selectors that might indicate the page is ready
            selectors = [
                # Generic search-related selectors
                "input[type='search']",
                "input[placeholder*='search']",
                "input[placeholder*='Search']",
                "input[placeholder*='keyword']",
                "input[placeholder*='Keyword']",
                # EPAM specific selectors
                "#jobSearchFilterForm",
                ".recruitment-search",
                ".job-search",
                "form[action*='job-search']",
                ".top-navigation--epam-sticky",  # EPAM header
                "[class*='job-search']",
                "[class*='search-form']",
                ".search-form",
                ".job-search__wrapper",
            ]

            # Try to find any of the selectors
            found_element = False
            page_content = await self.page.content()
            logger.debug("Page content length: %d", len(page_content))

            for selector in selectors:
                try:
                    # First check if element exists without timeout
                    is_visible = await self.page.locator(selector).is_visible()
                    if is_visible:
                        logger.info("Found visible element with selector: %s", selector)
                        found_element = True
                        break
                    else:
                        element = await self.page.query_selector(selector)
                        if element:
                            logger.info(
                                "Found hidden element with selector: %s", selector
                            )
                            found_element = True
                            break
                except PlaywrightError as e:
                    logger.debug("Error checking selector %s: %s", selector, str(e))
                    continue

            if not found_element:
                # Log the actual page content for debugging
                logger.error(
                    "Could not find any known elements. Current URL: %s", self.page.url
                )
                logger.error("Page title: %s", await self.page.title())
                await self._take_error_screenshot("page_state")
                raise PlaywrightError(
                    "Could not verify page load - no known elements found"
                )

        except PlaywrightError as e:
            logger.error("Failed to navigate to careers page: %s", e)
            await self._take_error_screenshot("navigation_error")
            raise  # Re-raise the original navigation error

    async def search_jobs(self, keyword: str):
        """Searches for jobs using the provided keyword."""
        await self.search_input.fill(keyword)
        await self.find_button.click()
        await self.page.wait_for_load_state("networkidle")

    async def filter_by_location(self, location: str):
        """Filters job listings by the specified location.

        Args:
            location (str): The cities selection (e.g., "All Cities in Poland")
        """
        logger.info("filter_by_location called with location: %s", location)
        await self.page.get_by_role("textbox", name=location).click()
        await self.page.get_by_role("combobox").filter(
            has_text=re.compile(r"^$")
        ).click()
        await self.page.get_by_role("combobox").filter(has_text=re.compile(r"^$")).fill(
            f"{location}"
        )
        await self.find_button.click()
        await self.page.wait_for_load_state("networkidle")

    async def filter_by_job_type(self, filter_type: str):
        """Filters job listings by the specified job type."""
        await self.page.get_by_text(filter_type, exact=True).click()
        await self.find_button.click()
        await self.page.wait_for_load_state("networkidle")

    async def get_job_titles(self):
        """Retrieves the titles of all job cards displayed on the page."""
        # return await self.job_cards.evaluate_all(
        #     "elements => elements.map(el => el.querySelector('.job-title').textContent)"
        # )
        return await self.all_jobs_on_page.all_text_contents()

    async def is_no_results_displayed(self):
        """Checks if the no results message is displayed."""
        return await self.no_results_message.is_visible()

    async def verify_mobile_menu(self):
        """Verifies the mobile menu functionality."""
        await self.hamburger_menu.click()
        await self.page.wait_for_load_state("networkidle")
        return await self.hamburger_menu.is_visible()

    async def check_if_search_input_visible(self):
        """Checks if the search input is visible."""
        await self.page.get_by_role("button", name="Search").click()
        return await self.search_input.is_visible()

    async def check_if_filters_visible(self):
        """Checks if the filters are visible in mobile view."""
        return await self.location_filter.is_visible()

    async def get_job_title(self, job_list: list, keyword: list):
        """Retrieves the job title from the job list."""
        for job in job_list:
            for kw in keyword:
                if kw.lower() in job.lower():
                    yield job
