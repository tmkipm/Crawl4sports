import pytest
from datetime import datetime
from src.app.models.ufc import UFCFighter
from src.app.models.premier_league import PremierLeagueTeam
from src.app.models.formula1 import Formula1Driver

def test_ufc_fighter_validation():
    """Test that UFC fighter model validates data correctly."""
    # Valid fighter data
    valid_fighter = UFCFighter(
        source_url="https://www.ufc.com/rankings",
        name="Jon Jones",
        rank="1",
        record="27-1-0",
        weight_class="Heavyweight"
    )
    assert valid_fighter.name == "Jon Jones"
    assert valid_fighter.rank == "1"
    assert valid_fighter.record == "27-1-0"
    assert valid_fighter.weight_class == "Heavyweight"
    assert isinstance(valid_fighter.scraped_at, datetime)

def test_ufc_fighter_invalid_record():
    """Test that invalid record format raises validation error."""
    with pytest.raises(ValueError, match="Record must be in format W-L-D"):
        UFCFighter(
            source_url="https://www.ufc.com/rankings",
            name="Jon Jones",
            rank="1",
            record="27-1",  # Missing draws
            weight_class="Heavyweight"
        )

def test_ufc_fighter_invalid_rank():
    """Test that invalid rank raises validation error."""
    with pytest.raises(ValueError, match="Rank must be a number or \"C\" for champion"):
        UFCFighter(
            source_url="https://www.ufc.com/rankings",
            name="Jon Jones",
            rank="invalid",
            record="27-1-0",
            weight_class="Heavyweight"
        )

def test_ufc_fighter_invalid_weight_class():
    """Test that invalid weight class raises validation error."""
    with pytest.raises(ValueError, match="Invalid weight class"):
        UFCFighter(
            source_url="https://www.ufc.com/rankings",
            name="Jon Jones",
            rank="1",
            record="27-1-0",
            weight_class="Invalid Class"
        )

def test_ufc_fighter_champion_rank():
    """Test that champion rank ('C') is accepted."""
    champion = UFCFighter(
        source_url="https://www.ufc.com/rankings",
        name="Jon Jones",
        rank="C",
        record="27-1-0",
        weight_class="Heavyweight"
    )
    assert champion.rank == "C"

def test_ufc_fighter_optional_fields():
    """Test that optional fields can be omitted."""
    fighter = UFCFighter(
        source_url="https://www.ufc.com/rankings",
        name="Jon Jones",
        rank="1",
        record="27-1-0",
        weight_class="Heavyweight",
        country="USA",
        age=35,
        height="6'4\"",
        reach="84.5\"",
        last_fight="2023-03-04"
    )
    assert fighter.country == "USA"
    assert fighter.age == 35
    assert fighter.height == "6'4\""
    assert fighter.reach == "84.5\""
    assert fighter.last_fight == "2023-03-04"

def test_premier_league_team_validation():
    """Test that Premier League team model validates data correctly."""
    valid_team = PremierLeagueTeam(
        source_url="https://www.premierleague.com/tables",
        name="Arsenal",
        position=1,
        played=30,
        won=20,
        drawn=5,
        lost=5,
        goals_for=60,
        goals_against=25,
        goal_difference=35,
        points=65,
        form="WWDLW"
    )
    assert valid_team.name == "Arsenal"
    assert valid_team.position == 1
    assert valid_team.points == 65
    assert valid_team.form == "WWDLW"
    assert isinstance(valid_team.scraped_at, datetime)

def test_premier_league_team_invalid_form():
    """Test that invalid form string raises validation error."""
    with pytest.raises(ValueError, match="Form must contain only W \\(win\\), D \\(draw\\), or L \\(loss\\)"):
        PremierLeagueTeam(
            source_url="https://www.premierleague.com/tables",
            name="Arsenal",
            position=1,
            played=30,
            won=20,
            drawn=5,
            lost=5,
            goals_for=60,
            goals_against=25,
            goal_difference=35,
            points=65,
            form="WWDLX"  # Invalid character
        )

def test_premier_league_team_invalid_points():
    """Test that incorrect points calculation raises validation error."""
    with pytest.raises(ValueError, match="Points must be 65 \\(3 \\* won \\+ drawn\\)"):
        PremierLeagueTeam(
            source_url="https://www.premierleague.com/tables",
            name="Arsenal",
            position=1,
            played=30,
            won=20,
            drawn=5,
            lost=5,
            goals_for=60,
            goals_against=25,
            goal_difference=35,
            points=70,  # Incorrect points
            form="WWDLW"
        )

def test_premier_league_team_invalid_goal_difference():
    """Test that incorrect goal difference raises validation error."""
    with pytest.raises(ValueError, match="Goal difference must be 35 \\(goals_for - goals_against\\)"):
        PremierLeagueTeam(
            source_url="https://www.premierleague.com/tables",
            name="Arsenal",
            position=1,
            played=30,
            won=20,
            drawn=5,
            lost=5,
            goals_for=60,
            goals_against=25,
            goal_difference=30,  # Incorrect goal difference
            points=65,
            form="WWDLW"
        )

def test_formula1_driver_validation():
    """Test that Formula 1 driver model validates data correctly."""
    valid_driver = Formula1Driver(
        source_url="https://www.formula1.com/en/results.html/2024/drivers.html",
        name="Max Verstappen",
        team="Red Bull Racing",
        position=1,
        points=250.5,
        wins=10,
        podiums=15,
        fastest_laps=5,
        nationality="Dutch",
        car_number=1
    )
    assert valid_driver.name == "Max Verstappen"
    assert valid_driver.team == "Red Bull Racing"
    assert valid_driver.points == 250.5
    assert valid_driver.car_number == 1
    assert isinstance(valid_driver.scraped_at, datetime)

def test_formula1_driver_invalid_podiums():
    """Test that podiums less than wins raises validation error."""
    with pytest.raises(ValueError, match="Podiums count cannot be less than wins count"):
        Formula1Driver(
            source_url="https://www.formula1.com/en/results.html/2024/drivers.html",
            name="Max Verstappen",
            team="Red Bull Racing",
            position=1,
            points=250.5,
            wins=10,
            podiums=8,  # Less than wins
            fastest_laps=5,
            nationality="Dutch",
            car_number=1
        )

def test_formula1_driver_invalid_points():
    """Test that invalid points format raises validation error."""
    with pytest.raises(ValueError, match="Points must be a multiple of 0.5"):
        Formula1Driver(
            source_url="https://www.formula1.com/en/results.html/2024/drivers.html",
            name="Max Verstappen",
            team="Red Bull Racing",
            position=1,
            points=250.25,  # Not a multiple of 0.5
            wins=10,
            podiums=15,
            fastest_laps=5,
            nationality="Dutch",
            car_number=1
        )

def test_formula1_driver_invalid_car_number():
    """Test that retired car number raises validation error."""
    with pytest.raises(ValueError, match="Car number 17 is retired or reserved"):
        Formula1Driver(
            source_url="https://www.formula1.com/en/results.html/2024/drivers.html",
            name="Max Verstappen",
            team="Red Bull Racing",
            position=1,
            points=250.5,
            wins=10,
            podiums=15,
            fastest_laps=5,
            nationality="Dutch",
            car_number=17  # Retired number
        ) 