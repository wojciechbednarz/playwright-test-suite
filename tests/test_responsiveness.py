import pytest
import allure
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@allure.feature("Responsive Design")
@pytest.mark.asyncio
class TestResponsiveness:
    """Class to test the responsiveness of the careers page on different devices."""

    @pytest.mark.parametrize(
        "device",
        [
            {"name": "iPhone 12", "width": 390, "height": 844},
            {"name": "iPad Air", "width": 820, "height": 1180},
        ],
    )
    @allure.story("Mobile responsiveness")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_mobile_responsiveness(self, careers_page, device):
        """Tests the mobile responsiveness of the careers page."""
        logger.info(f"Testing mobile responsiveness on {device['name']}")
        await careers_page.page.set_viewport_size(
            {"width": device["width"], "height": device["height"]}
        )
        # Verify mobile menu functionality
        assert (
            await careers_page.verify_mobile_menu()
        ), f"Mobile menu not functional on {device['name']}"
        # Check if search functionality is accessible in mobile view
        assert (
            await careers_page.check_if_search_input_visible()
        ), f"Search input not visible on {device['name']}"
        # Check if filters are accessible in mobile view
        assert (
            await careers_page.check_if_filters_visible()
        ), f"Filter toggle not visible on {device['name']}"
        # Verify that filter options become visible after clicking
        assert (
            await careers_page.skills_filter.is_visible()
        ), f"Filter options not visible after clicking on {device['name']}"
        logger.info(
            f"Mobile responsiveness test passed for {device['name']}"
        )
