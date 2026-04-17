from home_cards import render_card


ROUTE_ID = "repository"


def render_global_repository_card():
    render_card(
        "Global repository",
        "Shared knowledge and community resources can live here later.",
        ROUTE_ID,
    )
