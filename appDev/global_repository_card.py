from home_cards import render_card


ROUTE_ID = "repository"


def render_global_repository_card():
    render_card(
        "Global repository",
        "See shared practices, community momentum, and the future home of open meditation data.",
        ROUTE_ID,
    )
