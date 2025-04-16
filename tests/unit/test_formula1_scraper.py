import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.app.scrapers.formula1_scraper import Formula1Scraper
from crawl4ai import AsyncWebCrawler

@pytest.fixture
def formula1_scraper():
    return Formula1Scraper()

@pytest.fixture
def mock_crawler():
    mock = AsyncMock(spec=AsyncWebCrawler)
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = None
    with patch('src.app.scrapers.base_scraper.AsyncWebCrawler', return_value=mock):
        yield mock

@pytest.mark.asyncio
async def test_initialization(formula1_scraper, mock_crawler):
    """Test that the scraper initializes correctly"""
    await formula1_scraper.initialize()
    mock_crawler.__aenter__.assert_awaited_once()

@pytest.mark.asyncio
async def test_cleanup(formula1_scraper, mock_crawler):
    """Test that the scraper cleans up resources correctly"""
    await formula1_scraper.cleanup()
    mock_crawler.__aexit__.assert_awaited_once_with(None, None, None)

@pytest.mark.asyncio
async def test_get_required_fields(formula1_scraper):
    """Test that required fields are correctly defined"""
    required_fields = formula1_scraper.get_required_fields()
    assert isinstance(required_fields, list)
    assert all(isinstance(field, str) for field in required_fields)
    assert "driver_name" in required_fields
    assert "team" in required_fields
    assert "position" in required_fields
    assert "points" in required_fields

@pytest.mark.asyncio
async def test_scrape_success(formula1_scraper, mock_crawler):
    """Test successful scraping of Formula 1 data"""
    # Mock the crawler's arun method to return a successful result
    mock_page = AsyncMock()
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.page = mock_page
    mock_crawler.arun.return_value = mock_result
    
    # Mock the driver data extraction
    mock_row = AsyncMock()
    mock_row.query_selector.return_value = AsyncMock(
        text_content=AsyncMock(return_value="Test Driver")
    )
    mock_page.query_selector_all.return_value = [mock_row]
    
    # Initialize before scraping
    await formula1_scraper.initialize()
    drivers = await formula1_scraper.scrape()
    
    assert isinstance(drivers, list)
    mock_crawler.arun.assert_called()

@pytest.mark.asyncio
async def test_scrape_failure(formula1_scraper, mock_crawler):
    """Test handling of scraping failures"""
    # Mock the crawler's arun method to return a failed result
    mock_result = MagicMock()
    mock_result.success = False
    mock_crawler.arun.return_value = mock_result
    
    # Initialize before scraping
    await formula1_scraper.initialize()
    drivers = await formula1_scraper.scrape()
    
    assert isinstance(drivers, list)
    assert len(drivers) == 0
    mock_crawler.arun.assert_called()

@pytest.mark.asyncio
async def test_validate_data(formula1_scraper):
    """Test data validation"""
    # Valid data
    valid_data = {
        "driver_name": "Test Driver",
        "team": "Test Team",
        "position": "1",
        "points": "100",
        "wins": "5",
        "podiums": "10",
        "poles": "3",
        "fastest_laps": "2",
        "nationality": "Test Country",
        "car_number": "44"
    }
    assert formula1_scraper.validate_data(valid_data) is True
    
    # Invalid data (missing required field)
    invalid_data = {
        "driver_name": "Test Driver",
        "team": "Test Team",
        "position": "1",
        # Missing points
        "wins": "5",
        "podiums": "10",
        "poles": "3",
        "fastest_laps": "2",
        "nationality": "Test Country",
        "car_number": "44"
    }
    assert formula1_scraper.validate_data(invalid_data) is False 