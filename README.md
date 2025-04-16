# Crawl4Sports

A powerful sports data scraping and analysis platform that collects and processes data from various sports sources including Premier League, Formula 1, and UFC.

## Features

- **Multi-Sport Support**: Scrape data from multiple sports sources
  - Premier League standings and statistics
  - Formula 1 driver rankings and race results
  - UFC fighter rankings and event information
- **Robust Scraping**: Built on `crawl4ai` for reliable and efficient web scraping
- **Data Validation**: Comprehensive data validation using Pydantic models
- **Error Handling**: Robust error handling and logging
- **Extensible Architecture**: Easy to add new sports and data sources

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tmkipm/Crawl4sports.git
cd Crawl4sports
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
cp .env.example .env.local
```
Edit `.env.local` and add your Groq API key:
```plaintext
GROQ_API_KEY=your_api_key_here
```

## Project Structure

```
src/
├── app/
│   ├── config/          # Configuration files
│   ├── models/          # Pydantic data models
│   ├── scrapers/        # Web scraping implementations
│   └── services/        # Business logic and services
tests/
├── integration/         # Integration tests
└── unit/               # Unit tests
```

## Usage

### Running Scrapers

```python
from src.app.scrapers.premier_league_scraper import PremierLeagueScraper
from src.app.scrapers.formula1_scraper import Formula1Scraper
from src.app.scrapers.ufc_scraper import UFCScraper

async def main():
    # Initialize scrapers
    pl_scraper = PremierLeagueScraper()
    f1_scraper = Formula1Scraper()
    ufc_scraper = UFCScraper()
    
    # Initialize resources
    await pl_scraper.initialize()
    await f1_scraper.initialize()
    await ufc_scraper.initialize()
    
    try:
        # Scrape data
        pl_data = await pl_scraper.scrape()
        f1_data = await f1_scraper.scrape()
        ufc_data = await ufc_scraper.scrape()
        
        # Process data...
        
    finally:
        # Cleanup
        await pl_scraper.cleanup()
        await f1_scraper.cleanup()
        await ufc_scraper.cleanup()
```

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test file
python -m pytest tests/unit/test_premier_league_scraper.py

# Run with coverage
python -m pytest --cov=src tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Use type hints
- Handle errors appropriately
- Log important events

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [crawl4ai](https://github.com/crawl4ai/crawl4ai) - Web scraping framework
- [Pydantic](https://pydantic.dev/) - Data validation
- [Playwright](https://playwright.dev/) - Browser automation

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Add more sports sources
- [ ] Implement data analysis features
- [ ] Add visualization capabilities
- [ ] Create API endpoints
- [ ] Add user authentication
- [ ] Implement caching
- [ ] Add rate limiting
- [ ] Improve error handling
- [ ] Add more test coverage 