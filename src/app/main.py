import asyncio
import logging
from datetime import datetime
from scrapers.ufc_scraper import UFCScraper
from scrapers.premier_league_scraper import PremierLeagueScraper
from scrapers.formula1_scraper import Formula1Scraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Initialize scrapers
        ufc_scraper = UFCScraper()
        premier_league_scraper = PremierLeagueScraper()
        formula1_scraper = Formula1Scraper()
        
        # Create timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Run scrapers concurrently
        ufc_data, premier_league_data, formula1_data = await asyncio.gather(
            ufc_scraper.scrape(),
            premier_league_scraper.scrape(),
            formula1_scraper.scrape()
        )
        
        # Save data to CSV files
        await asyncio.gather(
            ufc_scraper.save_to_csv(ufc_data, f"data/ufc_standings_{timestamp}.csv"),
            premier_league_scraper.save_to_csv(premier_league_data, f"data/premier_league_standings_{timestamp}.csv"),
            formula1_scraper.save_to_csv(formula1_data, f"data/formula1_standings_{timestamp}.csv")
        )
        
        logger.info("Scraping completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        
if __name__ == "__main__":
    asyncio.run(main()) 