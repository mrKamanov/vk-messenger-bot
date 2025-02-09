# Copyright <2025> <Сергей Каманов>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

THEMES = {
    "default": {
        "text": "#2c3e50",
        "input_background": "#ffffff",
        "primary": "#EDC7B7",
        "secondary": "#EE2DC",
        "hover": "#BAB2B5",
        "gradient_start": "#123C69",
        "gradient_end": "#AC3B61",
        "opacity": 0.8  # Начальная прозрачность
    },
}

current_theme = THEMES["default"]


def get_global_style():
    return f"""
    QMainWindow {{
        background: qlineargradient(
            spread:pad,
            x1:0, y1:0,
            x2:1, y2:1,
            stop:0 {current_theme['gradient_start']},
            stop:1 {current_theme['gradient_end']}
        );
        color: {current_theme['text']};
        border-radius: 10px;
    }}
    QLabel {{
        color: {current_theme['text']};
        font-family: Roboto;
        font-size: 14px;
    }}
    QLineEdit, QSpinBox {{
        background-color: {current_theme['input_background']};
        color: {current_theme['text']};
        border: 1px solid #bdc3c7;
        border-radius: 10px;
        padding: 10px;
        font-family: Roboto;
        font-size: 14px;
    }}
    QPushButton {{
        background-color: {current_theme['primary']};  /* Используем однотонный цвет для кнопок */
        color: white;
        border: none;
        border-radius: 40px;
        padding: 15px 30px;
        font-family: Roboto;
        font-size: 16px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {current_theme['hover']};
    }}
    QComboBox {{
        background-color: {current_theme['input_background']};
        color: {current_theme['text']};
        border: 1px solid #bdc3c7;
        border-radius: 10px;
        padding: 10px;
        font-family: Roboto;
        font-size: 14px;
    }}
    QCheckBox {{
        color: {current_theme['text']};
        margin-top: 10px;
        font-family: Roboto;
        font-size: 14px;
    }}
    """


def get_title_style():
    return f"""
    font-family: Roboto;
    font-size: 24px;
    font-weight: bold;
    color: {current_theme['primary']};
    margin-bottom: 20px;
    text-align: center;
    """


def get_label_style():
    return f"""
    QLabel {{
        color: {current_theme['text']};
        font-family: Roboto;
        font-size: 14px;
    }}
    """


def get_author_label_style():
    return f"""
    font-family: Roboto;
    font-size: 12px;
    color: {current_theme['text']};
    margin-top: 20px;
    text-align: center;
    """


def get_checkbox_style():
    return f"""
    QCheckBox {{
        color: {current_theme['text']};
        margin-top: 10px;
        font-family: Roboto;
        font-size: 14px;
    }}
    """


def get_input_style():
    return f"""
    QLineEdit, QSpinBox {{
        background-color: {current_theme['input_background']};
        color: {current_theme['text']};
        border: 1px solid #bdc3c7;
        border-radius: 10px;
        padding: 10px;
        font-family: Roboto;
        font-size: 14px;
    }}
    """