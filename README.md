# Sports Data Scraper

A web scraping project that collects data from major sports websites including UFC, Premier League, and Formula 1.

## Features

- Scrapes data from:
  - UFC.com
  - PremierLeague.com
  - Formula1.com
- Asynchronous data collection
- Data validation and cleaning
- CSV export functionality

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sports-data-scraper.git
cd sports-data-scraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

## Usage

Run the scraper:
```bash
python src/app/main.py
```

## Project Structure

```
src/
├── app/
│   ├── main.py
│   └── scrapers/
│       ├── ufc_scraper.py
│       ├── premier_league_scraper.py
│       └── formula1_scraper.py
├── components/
│   └── data_validator.py
├── lib/
│   └── utils.py
└── styles/
    └── globals.css
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit your changes: `git commit -m 'Add some feature'`
3. Push to the branch: `git push origin feature/your-feature`
4. Open a Pull Request

## License

MIT License 