import pytest
import asyncio
from src.app.scrapers.base_scraper import BaseScraper
from src.app.scrapers.ufc_scraper import UFCScraper
from src.app.scrapers.premier_league_scraper import PremierLeagueScraper
from src.app.scrapers.formula1_scraper import Formula1Scraper

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_test():
    """Setup any state specific to the execution of the given test case."""
    yield  # this is where the testing happens

@pytest.fixture
async def ufc_scraper():
    scraper = UFCScraper()
    await scraper.initialize()
    yield scraper
    await scraper.cleanup()

@pytest.fixture
async def premier_league_scraper():
    scraper = PremierLeagueScraper()
    await scraper.initialize()
    yield scraper
    await scraper.cleanup()

@pytest.fixture
async def formula1_scraper():
    scraper = Formula1Scraper()
    await scraper.initialize()
    yield scraper
    await scraper.cleanup()

@pytest.fixture
def sample_ufc_data():
    return {
        "name": "Test Fighter",
        "record": "20-5-0",
        "weight_class": "Lightweight",
        "rank": "1",
        "country": "USA",
        "age": "30",
        "height": "5'9\"",
        "reach": "72\"",
        "last_fight": "2024-03-15"
    }

@pytest.fixture
def sample_premier_league_data():
    return {
        "team_name": "Test FC",
        "position": "1",
        "played": "30",
        "won": "20",
        "drawn": "5",
        "lost": "5",
        "goals_for": "60",
        "goals_against": "20",
        "goal_difference": "40",
        "points": "65",
        "form": "WWWDL"
    }

@pytest.fixture
def sample_formula1_data():
    return {
        "driver_name": "Test Driver",
        "team": "Test Racing",
        "position": "1",
        "points": "100",
        "wins": "5",
        "podiums": "8",
        "poles": "3",
        "fastest_laps": "2",
        "nationality": "GBR",
        "car_number": "44"
    } 