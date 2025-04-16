from crawl4ai import AsyncWebCrawler
import asyncio
from typing import Dict, List, Any, Optional
import logging
import os
from pathlib import Path

class BaseScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.crawler = AsyncWebCrawler()
        self.logger = logging.getLogger(__name__)
        
    async def initialize(self) -> None:
        """Initialize resources needed for scraping"""
        await self.crawler.__aenter__()
        
    async def cleanup(self) -> None:
        """Clean up resources after scraping"""
        await self.crawler.__aexit__(None, None, None)
        
    async def scrape(self) -> List[Dict[str, Any]]:
        """Base scrape method to be implemented by child classes"""
        raise NotImplementedError("Subclasses must implement scrape()")
        
    async def save_to_csv(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """Save scraped data to CSV
        
        Args:
            data: List of dictionaries containing the data to save
            filename: Path to the output CSV file
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        if not data:
            self.logger.warning("No data to save")
            return False
            
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                
            self.logger.info(f"Saved {len(data)} records to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save data to {filename}: {str(e)}")
            return False
        
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate scraped data
        
        Args:
            data: Dictionary containing the data to validate
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        required_fields = self.get_required_fields()
        return all(field in data for field in required_fields)
        
    def get_required_fields(self) -> List[str]:
        """Get list of required fields for validation
        
        Returns:
            List[str]: List of required field names
        """
        raise NotImplementedError("Subclasses must implement get_required_fields()") 