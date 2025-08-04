from typing import AsyncGenerator
import logging
import pytest_asyncio
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from pages.careers_page import CareersPage
from pages.job_details_page import JobDetailsPage


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def pytest_runtest_makereport(item, call):
    """Set report attribute for each phase of a call (setup, call, teardown).
    Simply set the report attribute - the CallInfo object is the result itself
    """
    setattr(item, f"rep_{call.when}", call)


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line("markers", "asyncio: mark test as async")


@pytest_asyncio.fixture(scope="function")
async def browser() -> AsyncGenerator[Browser, None]:
    """Launch a browser instance for the tests."""
    logger.info("Starting browser fixture")
    try:
        async with async_playwright() as p:
            logger.debug("Launching browser")
            browser_instance = await p.chromium.launch(
                headless=True,  # Set to False if you want to see the browser
                args=[
                    "--start-maximized",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ],
                timeout=60000,  # 60 seconds timeout
            )
            logger.info("Browser launched successfully")
            try:
                yield browser_instance
            finally:
                logger.debug("Closing browser")
                try:
                    await browser_instance.close()
                    logger.info("Browser closed successfully")
                except Exception as e:
                    logger.error(f"Error closing browser: {e}")
    except Exception as e:
        logger.error(f"Error in browser fixture: {e}")
        raise


@pytest_asyncio.fixture(scope="function")
async def context(browser: Browser) -> AsyncGenerator[BrowserContext, None]:
    """Create a new browser context for each test."""
    logger.debug("Creating new browser context")
    try:
        browser_context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
            service_workers="block",  # Disable service workers for better stability
        )
        logger.info("Browser context created successfully")
        try:
            yield browser_context
        finally:
            logger.debug("Closing browser context")
            try:
                await browser_context.close()
                logger.info("Browser context closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser context: {e}")
    except Exception as e:
        logger.error(f"Error creating browser context: {e}")
        raise


@pytest_asyncio.fixture(scope="function")
async def page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """Create a new page for each test."""
    new_page = await context.new_page()
    yield new_page
    await new_page.close()


@pytest_asyncio.fixture(scope="function")
async def careers_page(page: Page) -> AsyncGenerator[CareersPage, None]:
    """Create a CareersPage instance for testing."""
    try:
        careers_page_instance = CareersPage(page)
        await careers_page_instance.navigate()
        yield careers_page_instance
    except Exception as e:
        logger.error(f"Error in careers_page fixture: {e}")
        raise


@pytest_asyncio.fixture(scope="function")
async def job_details_page(page: Page) -> AsyncGenerator[JobDetailsPage, None]:
    """Create a JobDetailsPage instance for testing."""
    yield JobDetailsPage(page)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def trace_on_failure(context, request):
    """Start tracing for each test and stop on failure."""
    logger.debug("Starting trace_on_failure fixture")

    # Create traces directory if it doesn't exist
    Path("traces").mkdir(exist_ok=True)
    await context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    try:
        # Check if test failed - use the CallInfo object directly
        failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
        if failed:
            logger.error(f"Test {request.node.name} failed, saving trace")
            trace_path = Path("traces") / f"{request.node.name}.zip"
            await context.tracing.stop(path=str(trace_path))
        else:
            logger.info(f"Test {request.node.name} passed, not saving trace")
            await context.tracing.stop()
    except Exception as e:
        logger.error(f"Error in trace handling: {e}")
        # Ensure tracing is stopped even if there's an error
        try:
            await context.tracing.stop()
        except Exception as close_error:
            logger.error(f"Error stopping trace: {close_error}")
            pass
