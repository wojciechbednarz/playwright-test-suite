import logging
import allure
import pytest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@allure.feature("Job Filters")
@pytest.mark.asyncio
class TestFilters:
    """Class to test job filtering functionality on the careers page."""

    @allure.story("Filter by location")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    async def test_filter_by_location(self, careers_page):
        """Tests filtering job listings by location."""
        try:
            logger.info("Starting test_filter_by_location")
            await careers_page.filter_by_location("All Cities in Poland")
            job_titles = await careers_page.get_job_titles()
            assert len(job_titles) > 0, "No jobs found for All Cities in Poland"
            logger.info(f"Job titles found for All Cities in Poland: {job_titles}")
        except TypeError as e:
            logger.error(f"TypeError occurred: {e}")
            logger.error(f"careers_page type: {type(careers_page)}")
            logger.error(
                f"filter_by_location method: {getattr(careers_page, 'filter_by_location', None)}"
            )
            raise

    @allure.story("Filter by job type")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_filter_by_job_type(self, careers_page):
        """Tests filtering job listings by job type."""
        logger.info("Starting test_filter_by_job_type")
        await careers_page.filter_by_job_type("Remote")
        job_titles = await careers_page.get_job_titles()

        assert len(job_titles) > 0, "No remote jobs found"
        logger.info(f"Job titles found for Remote: {job_titles}")

    @allure.story("Validate job card content")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_job_card_content(self, careers_page, job_details_page):
        """Tests that job cards contain expected content and navigates to job details."""
        logger.info("Starting test_job_card_content")
        await careers_page.search_jobs("Python Developer")
        job_titles = await careers_page.get_job_titles()

        assert len(job_titles) > 0, "No Python Developer jobs found"

        # Click first job card and verify details
        await careers_page.all_jobs_on_page.first.click()
        job_title = await job_details_page.get_job_title()
        job_location = await job_details_page.get_job_location()
        job_description = await job_details_page.get_job_description()

        assert job_title, "Job title is empty"
        assert job_location, "Job location is empty"
        assert job_description, "Job description is empty"
        logger.info(
            f"Job title: {job_title}, Location: {job_location}, Description: {job_description}"
        )
