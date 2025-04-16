import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.app.scrapers.premier_league_scraper import PremierLeagueScraper
from crawl4ai import AsyncWebCrawler

@pytest.fixture
def premier_league_scraper():
    return PremierLeagueScraper()

@pytest.fixture
def mock_crawler():
    mock = AsyncMock(spec=AsyncWebCrawler)
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = None
    with patch('src.app.scrapers.base_scraper.AsyncWebCrawler', return_value=mock):
        yield mock

@pytest.mark.asyncio
async def test_initialization(premier_league_scraper, mock_crawler):
    """Test that the scraper initializes correctly"""
    await premier_league_scraper.initialize()
    mock_crawler.__aenter__.assert_awaited_once()

@pytest.mark.asyncio
async def test_cleanup(premier_league_scraper, mock_crawler):
    """Test that the scraper cleans up resources correctly"""
    await premier_league_scraper.cleanup()
    mock_crawler.__aexit__.assert_awaited_once_with(None, None, None)

@pytest.mark.asyncio
async def test_get_required_fields(premier_league_scraper):
    """Test that required fields are correctly defined"""
    required_fields = premier_league_scraper.get_required_fields()
    assert isinstance(required_fields, list)
    assert all(isinstance(field, str) for field in required_fields)
    assert "team_name" in required_fields
    assert "position" in required_fields
    assert "points" in required_fields
    assert "played" in required_fields

@pytest.mark.asyncio
async def test_scrape_success(premier_league_scraper, mock_crawler):
    """Test successful scraping of Premier League data"""
    # Mock the crawler's arun method to return a successful result
    mock_page = AsyncMock()
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.page = mock_page
    mock_crawler.arun.return_value = mock_result
    
    # Mock the team data extraction
    mock_row = AsyncMock()
    mock_row.query_selector.return_value = AsyncMock(
        text_content=AsyncMock(return_value="Test Team")
    )
    mock_page.query_selector_all.return_value = [mock_row]
    
    # Initialize before scraping
    await premier_league_scraper.initialize()
    teams = await premier_league_scraper.scrape()
    
    assert isinstance(teams, list)
    mock_crawler.arun.assert_called()

@pytest.mark.asyncio
async def test_scrape_failure(premier_league_scraper, mock_crawler):
    """Test handling of scraping failures"""
    # Mock the crawler's arun method to return a failed result
    mock_result = MagicMock()
    mock_result.success = False
    mock_crawler.arun.return_value = mock_result
    
    # Initialize before scraping
    await premier_league_scraper.initialize()
    teams = await premier_league_scraper.scrape()
    
    assert isinstance(teams, list)
    assert len(teams) == 0
    mock_crawler.arun.assert_called()

@pytest.mark.asyncio
async def test_validate_data(premier_league_scraper):
    """Test data validation"""
    # Valid data
    valid_data = {
        "team_name": "Test Team",
        "position": "1",
        "played": "20",
        "won": "15",
        "drawn": "3",
        "lost": "2",
        "goals_for": "45",
        "goals_against": "15",
        "goal_difference": "30",
        "points": "48",
        "form": "WWWDL"
    }
    assert premier_league_scraper.validate_data(valid_data) is True
    
    # Invalid data (missing required field)
    invalid_data = {
        "team_name": "Test Team",
        "position": "1",
        "played": "20",
        "won": "15",
        "drawn": "3",
        "lost": "2",
        "goals_for": "45",
        "goals_against": "15",
        "goal_difference": "30",
        # Missing points
        "form": "WWWDL"
    }
    assert premier_league_scraper.validate_data(invalid_data) is False 