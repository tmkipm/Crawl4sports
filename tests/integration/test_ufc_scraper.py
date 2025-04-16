import pytest
from src.app.scrapers.ufc_scraper import UFCScraper

@pytest.mark.asyncio
async def test_ufc_scraper_initialization(ufc_scraper):
    assert ufc_scraper.base_url == "https://www.ufc.com"
    assert ufc_scraper.logger is not None

@pytest.mark.asyncio
async def test_ufc_required_fields(ufc_scraper):
    required_fields = ufc_scraper.get_required_fields()
    assert isinstance(required_fields, list)
    assert len(required_fields) > 0
    assert "name" in required_fields
    assert "record" in required_fields
    assert "weight_class" in required_fields

@pytest.mark.asyncio
async def test_ufc_data_validation(ufc_scraper, sample_ufc_data):
    assert ufc_scraper.validate_data(sample_ufc_data) is True
    
    # Test with missing required field
    invalid_data = sample_ufc_data.copy()
    del invalid_data["name"]
    assert ufc_scraper.validate_data(invalid_data) is False

@pytest.mark.asyncio
async def test_ufc_scrape_integration(ufc_scraper):
    # This is an integration test that actually scrapes the UFC website
    # Note: This test might fail if the website structure changes
    try:
        data = await ufc_scraper.scrape()
        assert isinstance(data, list)
        
        if data:  # If we got any data
            first_item = data[0]
            assert ufc_scraper.validate_data(first_item)
            
            # Check that all required fields are present and not empty
            for field in ufc_scraper.get_required_fields():
                assert field in first_item
                assert first_item[field] is not None
                assert first_item[field] != ""
                
    except Exception as e:
        pytest.fail(f"Scraping failed with error: {str(e)}")

@pytest.mark.asyncio
async def test_ufc_save_to_csv(ufc_scraper, sample_ufc_data, tmp_path):
    test_file = tmp_path / "ufc_test.csv"
    await ufc_scraper.save_to_csv([sample_ufc_data], str(test_file))
    
    assert test_file.exists()
    with open(test_file, 'r') as f:
        content = f.read()
        assert "name" in content
        assert "Test Fighter" in content 