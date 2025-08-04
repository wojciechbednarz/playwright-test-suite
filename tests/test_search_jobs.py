import allure
import pytest
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@allure.feature("Job Search")
@pytest.mark.asyncio
class TestSearchJobs:
    """Class to test job search functionality on the careers page."""

    @allure.story("Search for QA positions")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_search_qa_positions(self, careers_page):
        """Tests searching for QA positions."""
        logger.info("Starting test_search_qa_positions")
        await careers_page.search_jobs("QA")
        job_titles = await careers_page.get_job_titles()

        assert len(job_titles) > 0, "No QA jobs found"
        logger.info(f"Job titles found: {job_titles}, type: {type(job_titles)}")
        assert careers_page.get_job_title(
            job_titles, ["qa", "quality", "test"]
        ), "No QA jobs found in job titles"

    @allure.story("Search with invalid input")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_search_invalid_input(self, careers_page):
        """Tests searching with invalid input."""
        logger.info("Starting test_search_invalid_input")
        await careers_page.search_jobs("xzy123!@#")
        assert (
            await careers_page.is_no_results_displayed()
        ), "No results message not shown"
        logger.info("No results message displayed as expected")
