from app import process_query


def test_knows_about_dinosaurs():
    assert (
        process_query("dinosaurs")
        == "Dinosaurs ruled the Earth 200 million years ago"
    )


def test_knows_about_asteroids():
    assert (
        process_query("asteroids")
        == "Asteroids are rocky bodies orbiting the Sun"
    )


def test_returns_unknown_for_invalid_query():
    assert process_query("unknown") == "Unknown"
