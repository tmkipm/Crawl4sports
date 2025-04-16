from .base_scraper import BaseScraper
from typing import Dict, List, Any, Optional
import logging
from src.app.models.formula1 import Formula1Driver
from datetime import datetime

class Formula1Scraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.formula1.com")
        self.logger = logging.getLogger(__name__)
        
    def get_required_fields(self) -> List[str]:
        return [
            "driver_name", "team", "position", "points", "wins",
            "podiums", "fastest_laps", "nationality", "car_number"
        ]
        
    async def scrape(self) -> List[Dict[str, Any]]:
        """Scrape Formula 1 driver data from the official website."""
        drivers = []
        current_year = datetime.now().year
        source_url = f"https://www.formula1.com/en/results.html/{current_year}/drivers.html"
        
        try:
            # Navigate to the Formula 1 drivers standings page
            result = await self.crawler.arun(source_url)
            if not result.success:
                self.logger.error("Failed to load Formula 1 drivers standings page")
                return drivers

            page = result.page
            
            # Get all driver rows
            driver_rows = await page.query_selector_all(".resultsarchive-table tr")
            for row in driver_rows:
                try:
                    driver_data = await self._extract_driver_data(row)
                    if not self.validate_data(driver_data):
                        self.logger.warning(f"Skipping driver due to missing required fields: {driver_data}")
                        continue
                        
                    # Create and validate driver using Pydantic model
                    driver = Formula1Driver(
                        source_url=source_url,
                        name=driver_data["driver_name"],
                        team=driver_data["team"],
                        position=driver_data["position"],
                        points=driver_data["points"],
                        wins=driver_data["wins"],
                        podiums=driver_data["podiums"],
                        fastest_laps=driver_data["fastest_laps"],
                        nationality=driver_data["nationality"],
                        car_number=driver_data["car_number"]
                    )
                    drivers.append(driver.dict())
                except Exception as e:
                    self.logger.error(f"Error processing driver data: {str(e)}")
                    continue
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
        
        return drivers
            
    async def _extract_driver_data(self, row) -> Dict[str, Any]:
        """Extract data for a single driver from their row element."""
        try:
            position_elem = await row.query_selector(".position")
            name_elem = await row.query_selector(".driver-name")
            team_elem = await row.query_selector(".team-name")
            points_elem = await row.query_selector(".points")
            wins_elem = await row.query_selector(".wins")
            podiums_elem = await row.query_selector(".podiums")
            fastest_laps_elem = await row.query_selector(".fastest-laps")
            nationality_elem = await row.query_selector(".nationality")
            car_number_elem = await row.query_selector(".car-number")
            
            # Extract and convert data with error handling
            def safe_int(text: Optional[str]) -> int:
                try:
                    return int(text) if text else 0
                except ValueError:
                    return 0
                    
            def safe_float(text: Optional[str]) -> float:
                try:
                    return float(text) if text else 0.0
                except ValueError:
                    return 0.0
                    
            def safe_str(text: Optional[str]) -> str:
                return text.strip() if text else ""
            
            return {
                "driver_name": safe_str(await name_elem.text_content() if name_elem else ""),
                "team": safe_str(await team_elem.text_content() if team_elem else ""),
                "position": safe_int(await position_elem.text_content() if position_elem else ""),
                "points": safe_float(await points_elem.text_content() if points_elem else ""),
                "wins": safe_int(await wins_elem.text_content() if wins_elem else ""),
                "podiums": safe_int(await podiums_elem.text_content() if podiums_elem else ""),
                "fastest_laps": safe_int(await fastest_laps_elem.text_content() if fastest_laps_elem else ""),
                "nationality": safe_str(await nationality_elem.text_content() if nationality_elem else ""),
                "car_number": safe_int(await car_number_elem.text_content() if car_number_elem else "")
            }
        except Exception as e:
            self.logger.error(f"Error extracting driver data: {str(e)}")
            return {} 