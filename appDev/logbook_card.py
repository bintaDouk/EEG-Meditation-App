from home_cards import render_card


ROUTE_ID = "logbook"


def render_logbook_card():
    render_card(
        "Logbook",
        "Open a dedicated page for your saved reflections, newest first.",
        ROUTE_ID,
    )
