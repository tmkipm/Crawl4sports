import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.app.scrapers.ufc_scraper import UFCScraper
from crawl4ai import AsyncWebCrawler

@pytest.fixture
def ufc_scraper():
    return UFCScraper()

@pytest.fixture
def mock_crawler():
    mock = AsyncMock(spec=AsyncWebCrawler)
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = None
    with patch('src.app.scrapers.base_scraper.AsyncWebCrawler', return_value=mock):
        yield mock

@pytest.mark.asyncio
async def test_initialization(ufc_scraper, mock_crawler):
    """Test that the scraper initializes correctly"""
    await ufc_scraper.initialize()
    mock_crawler.__aenter__.assert_awaited_once()

@pytest.mark.asyncio
async def test_cleanup(ufc_scraper, mock_crawler):
    """Test that the scraper cleans up resources correctly"""
    await ufc_scraper.cleanup()
    mock_crawler.__aexit__.assert_awaited_once_with(None, None, None)

@pytest.mark.asyncio
async def test_get_required_fields(ufc_scraper):
    """Test that required fields are correctly defined"""
    required_fields = ufc_scraper.get_required_fields()
    assert isinstance(required_fields, list)
    assert all(isinstance(field, str) for field in required_fields)
    assert "name" in required_fields
    assert "record" in required_fields
    assert "weight_class" in required_fields
    assert "rank" in required_fields

@pytest.mark.asyncio
async def test_scrape_success(ufc_scraper, mock_crawler):
    """Test successful scraping of UFC data"""
    # Mock the crawler's arun method to return a successful result
    mock_page = AsyncMock()
    mock_page.query_selector_all.return_value = [
        AsyncMock(get_attribute=AsyncMock(return_value="Heavyweight")),
        AsyncMock(get_attribute=AsyncMock(return_value="Lightweight"))
    ]
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.page = mock_page
    mock_crawler.arun.return_value = mock_result
    
    # Mock the fighter data extraction
    mock_row = AsyncMock()
    mock_row.query_selector.return_value = AsyncMock(
        text_content=AsyncMock(return_value="Test Fighter")
    )
    mock_page.query_selector_all.return_value = [mock_row]
    
    # Initialize before scraping
    await ufc_scraper.initialize()
    fighters = await ufc_scraper.scrape()
    
    assert isinstance(fighters, list)
    mock_crawler.arun.assert_called()

@pytest.mark.asyncio
async def test_scrape_failure(ufc_scraper, mock_crawler):
    """Test handling of scraping failures"""
    # Mock the crawler's arun method to return a failed result
    mock_result = MagicMock()
    mock_result.success = False
    mock_crawler.arun.return_value = mock_result
    
    # Initialize before scraping
    await ufc_scraper.initialize()
    fighters = await ufc_scraper.scrape()
    
    assert isinstance(fighters, list)
    assert len(fighters) == 0
    mock_crawler.arun.assert_called()

@pytest.mark.asyncio
async def test_validate_data(ufc_scraper):
    """Test data validation"""
    # Valid data
    valid_data = {
        "name": "Test Fighter",
        "record": "10-0-0",
        "weight_class": "Heavyweight",
        "rank": "1",
        "country": "USA",
        "age": "30",
        "height": "6'2\"",
        "reach": "76\"",
        "last_fight": "2024-01-01"
    }
    assert ufc_scraper.validate_data(valid_data) is True
    
    # Invalid data (missing required field)
    invalid_data = {
        "name": "Test Fighter",
        "record": "10-0-0",
        "weight_class": "Heavyweight",
        # Missing rank
        "country": "USA",
        "age": "30",
        "height": "6'2\"",
        "reach": "76\"",
        "last_fight": "2024-01-01"
    }
    assert ufc_scraper.validate_data(invalid_data) is False 