import pytest
from src.app.scrapers.base_scraper import BaseScraper

class TestBaseScraper(BaseScraper):
    def get_required_fields(self) -> list:
        return ["field1", "field2"]

@pytest.mark.asyncio
async def test_initialization():
    scraper = TestBaseScraper("https://test.com")
    assert scraper.base_url == "https://test.com"
    assert scraper.logger is not None

@pytest.mark.asyncio
async def test_validate_data():
    scraper = TestBaseScraper("https://test.com")
    
    # Test valid data
    valid_data = {"field1": "value1", "field2": "value2"}
    assert scraper.validate_data(valid_data) is True
    
    # Test invalid data
    invalid_data = {"field1": "value1"}
    assert scraper.validate_data(invalid_data) is False

@pytest.mark.asyncio
async def test_save_to_csv(tmp_path):
    scraper = TestBaseScraper("https://test.com")
    test_data = [
        {"field1": "value1", "field2": "value2"},
        {"field1": "value3", "field2": "value4"}
    ]
    
    # Test saving data
    test_file = tmp_path / "test.csv"
    await scraper.save_to_csv(test_data, str(test_file))
    
    # Verify file was created and contains correct data
    assert test_file.exists()
    with open(test_file, 'r') as f:
        content = f.read()
        assert "field1,field2" in content
        assert "value1,value2" in content
        assert "value3,value4" in content

@pytest.mark.asyncio
async def test_save_to_csv_empty_data(tmp_path):
    scraper = TestBaseScraper("https://test.com")
    test_file = tmp_path / "test.csv"
    
    # Test saving empty data
    await scraper.save_to_csv([], str(test_file))
    assert not test_file.exists() 