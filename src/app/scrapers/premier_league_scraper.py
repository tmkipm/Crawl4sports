from .base_scraper import BaseScraper
from typing import Dict, List, Any, Optional
import logging
from src.app.models.premier_league import PremierLeagueTeam

class PremierLeagueScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.premierleague.com")
        self.logger = logging.getLogger(__name__)
        
    def get_required_fields(self) -> List[str]:
        return [
            "team_name", "position", "played", "won", "drawn", "lost",
            "goals_for", "goals_against", "goal_difference", "points", "form"
        ]
        
    async def scrape(self) -> List[Dict[str, Any]]:
        """Scrape Premier League team data from the official website."""
        teams = []
        source_url = "https://www.premierleague.com/tables"
        
        try:
            # Navigate to the Premier League table page
            result = await self.crawler.arun(source_url)
            if not result.success:
                self.logger.error("Failed to load Premier League table page")
                return teams

            page = result.page
            
            # Get all team rows
            team_rows = await page.query_selector_all(".table-row")
            for row in team_rows:
                try:
                    team_data = await self._extract_team_data(row)
                    if not self.validate_data(team_data):
                        self.logger.warning(f"Skipping team due to missing required fields: {team_data}")
                        continue
                        
                    # Create and validate team using Pydantic model
                    team = PremierLeagueTeam(
                        source_url=source_url,
                        name=team_data["team_name"],
                        position=team_data["position"],
                        played=team_data["played"],
                        won=team_data["won"],
                        drawn=team_data["drawn"],
                        lost=team_data["lost"],
                        goals_for=team_data["goals_for"],
                        goals_against=team_data["goals_against"],
                        goal_difference=team_data["goal_difference"],
                        points=team_data["points"],
                        form=team_data["form"]
                    )
                    teams.append(team.dict())
                except Exception as e:
                    self.logger.error(f"Error processing team data: {str(e)}")
                    continue
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
        
        return teams
            
    async def _extract_team_data(self, row) -> Dict[str, Any]:
        """Extract data for a single team from their row element."""
        try:
            position_elem = await row.query_selector(".position")
            name_elem = await row.query_selector(".team-name")
            played_elem = await row.query_selector(".played")
            won_elem = await row.query_selector(".won")
            drawn_elem = await row.query_selector(".drawn")
            lost_elem = await row.query_selector(".lost")
            goals_for_elem = await row.query_selector(".for")
            goals_against_elem = await row.query_selector(".against")
            goal_difference_elem = await row.query_selector(".goal-difference")
            points_elem = await row.query_selector(".points")
            form_elem = await row.query_selector(".form")
            
            # Extract and convert data with error handling
            def safe_int(text: Optional[str]) -> int:
                try:
                    return int(text) if text else 0
                except ValueError:
                    return 0
                    
            def safe_str(text: Optional[str]) -> str:
                return text.strip() if text else ""
            
            return {
                "team_name": safe_str(await name_elem.text_content() if name_elem else ""),
                "position": safe_int(await position_elem.text_content() if position_elem else ""),
                "played": safe_int(await played_elem.text_content() if played_elem else ""),
                "won": safe_int(await won_elem.text_content() if won_elem else ""),
                "drawn": safe_int(await drawn_elem.text_content() if drawn_elem else ""),
                "lost": safe_int(await lost_elem.text_content() if lost_elem else ""),
                "goals_for": safe_int(await goals_for_elem.text_content() if goals_for_elem else ""),
                "goals_against": safe_int(await goals_against_elem.text_content() if goals_against_elem else ""),
                "goal_difference": safe_int(await goal_difference_elem.text_content() if goal_difference_elem else ""),
                "points": safe_int(await points_elem.text_content() if points_elem else ""),
                "form": safe_str(await form_elem.text_content() if form_elem else "")
            }
        except Exception as e:
            self.logger.error(f"Error extracting team data: {str(e)}")
            return {} 