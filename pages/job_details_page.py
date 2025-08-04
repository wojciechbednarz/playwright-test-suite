from playwright.async_api import Page


class JobDetailsPage:
    """Class representing the job details page of the website."""

    def __init__(self, page: Page):
        """Initializes the JobDetailsPage with a Playwright Page object.
        Args:
            page (Page): The Playwright Page object to interact with the job details page.
        """
        self.page = page
        self.job_title = page.locator("h1[class='vacancy-details-23__job-title']")
        self.job_location = page.locator(".vacancy-details-23__location")
        self.job_description = page.locator("div[class='vacancy-details-23__content-holder']")
        self.apply_button = page.locator("[data-auto='apply-button']")

    async def get_job_title(self):
        """Retrieves the job title from the job details page."""
        return await self.job_title.text_content()

    async def get_job_location(self):
        """Retrieves the job location from the job details page."""
        return await self.job_location.text_content()

    async def get_job_description(self):
        """Retrieves the job description from the job details page."""
        all_descriptions = await self.job_description.locator("li").all_text_contents()
        return " ".join(all_descriptions).strip() if all_descriptions else ""

    async def click_apply(self):
        """Clicks the apply button on the job details page."""
        await self.apply_button.click()
        await self.page.wait_for_load_state("networkidle")
