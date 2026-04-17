from home_cards import render_card


ROUTE_ID = "submit"


def render_submit_recorded_card():
    render_card(
        "Submit recorded session",
        "Upload a completed session from another workflow.",
        ROUTE_ID,
    )
