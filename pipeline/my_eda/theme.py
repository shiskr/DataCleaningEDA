import plotly.io as pio

THEMES = {
    "light": {
        "bg": "#ffffff",
        "text": "#222",
        "header": "#2c3e50"
    },
    "dark": {
        "bg": "#0f172a",
        "text": "#e5e7eb",
        "header": "#38bdf8"
    }
}


def css(theme):
    return f"""
    body {{
        background-color: {theme['bg']};
        color: {theme['text']};
        font-family: Arial;
        margin: 40px;
    }}
    h1, h2 {{ color: {theme['header']}; }}
    """

EDA_THEME = "plotly_white"

def apply_eda_theme():
    pio.templates.default = EDA_THEME