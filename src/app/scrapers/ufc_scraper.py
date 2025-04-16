from .base_scraper import BaseScraper
from typing import Dict, List, Any, Optional
import logging
from src.app.models.ufc import UFCFighter

class UFCScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.ufc.com")
        self.logger = logging.getLogger(__name__)
        
    def get_required_fields(self) -> List[str]:
        return ["name", "record", "weight_class", "rank"]
        
    async def scrape(self) -> List[Dict[str, Any]]:
        """Scrape UFC fighter data from the official UFC rankings page."""
        fighters = []
        source_url = "https://www.ufc.com/rankings"
        
        try:
            # Navigate to the UFC rankings page
            result = await self.crawler.arun(source_url)
            if not result.success:
                self.logger.error("Failed to load UFC rankings page")
                return fighters

            page = result.page
            
            # Get all weight classes
            weight_class_elements = await page.query_selector_all(".view-grouping-header")
            for weight_class_elem in weight_class_elements:
                try:
                    weight_class = await weight_class_elem.text_content()
                    if not weight_class:
                        continue
                        
                    # Get all fighters in this weight class
                    fighter_rows = await page.query_selector_all(f".view-grouping-content:has(+ .view-grouping-header:contains('{weight_class}')) .views-row")
                    for row in fighter_rows:
                        try:
                            fighter_data = await self._extract_fighter_data(row, weight_class)
                            if not self.validate_data(fighter_data):
                                self.logger.warning(f"Skipping fighter due to missing required fields: {fighter_data}")
                                continue
                                
                            # Create and validate fighter using Pydantic model
                            fighter = UFCFighter(
                                source_url=source_url,
                                name=fighter_data["name"],
                                rank=fighter_data["rank"],
                                record=fighter_data["record"],
                                weight_class=fighter_data["weight_class"]
                            )
                            fighters.append(fighter.dict())
                        except Exception as e:
                            self.logger.error(f"Error processing fighter data: {str(e)}")
                            continue
                except Exception as e:
                    self.logger.error(f"Error processing weight class {weight_class}: {str(e)}")
                    continue
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
        
        return fighters
            
    async def _extract_fighter_data(self, row, weight_class: str) -> Dict[str, Any]:
        """Extract data for a single fighter from their row element."""
        try:
            name_elem = await row.query_selector(".views-field-title")
            rank_elem = await row.query_selector(".views-field-weight-class-rank")
            record_elem = await row.query_selector(".views-field-record")
            
            # Extract and convert data with error handling
            def safe_str(text: Optional[str]) -> str:
                return text.strip() if text else ""
            
            def safe_rank(text: Optional[str]) -> str:
                try:
                    # Remove any non-numeric characters and convert to int
                    rank = ''.join(filter(str.isdigit, text)) if text else "0"
                    return str(int(rank))
                except ValueError:
                    return "0"
            
            name = safe_str(await name_elem.text_content() if name_elem else "")
            rank = safe_rank(await rank_elem.text_content() if rank_elem else "")
            record = safe_str(await record_elem.text_content() if record_elem else "")
            
            return {
                "name": name,
                "rank": rank,
                "record": record,
                "weight_class": safe_str(weight_class)
            }
        except Exception as e:
            self.logger.error(f"Error extracting fighter data: {str(e)}")
            return {} 