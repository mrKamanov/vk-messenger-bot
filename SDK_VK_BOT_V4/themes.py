# Copyright <2025> <Сергей Каманов>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

THEMES = {
    "default": {
        "text": "#EDEDED",
        "input_background": "#121212",
        "primary": "#D4AF37",
        "secondary": "#A67C00",
        "hover": "#FFD700",
        "gradient_start": "#0D0D0D",
        "gradient_end": "#1A1A1A",
        "opacity": 0.1
    },
}
current_theme = THEMES["default"]

def get_global_style():
    return f"""
    QMainWindow {{
        background: qlineargradient(
            x1:0, y1:0,
            x2:0, y2:1,
            stop:0 {current_theme['gradient_start']},
            stop:1 {current_theme['gradient_end']}
        );
        color: {current_theme['text']};
    }}
    QLabel {{
        color: {current_theme['text']};
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
    }}
    QLineEdit, QSpinBox {{
        background-color: rgba(255, 255, 255, {current_theme['opacity']});
        border: 1px solid {current_theme['primary']};
        border-radius: 15px;
        padding: 10px;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        color: {current_theme['text']};
    }}
    QLineEdit:focus, QSpinBox:focus {{
        border-color: {current_theme['secondary']};
    }}
    QPushButton {{
        background-color: {current_theme['primary']};
        color: #FFFFFF;
        border: none;
        border-radius: 20px;
        padding: 15px 30px;
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {current_theme['hover']};
    }}
    QComboBox {{
        background-color: rgba(255, 255, 255, {current_theme['opacity']});
        border: 1px solid {current_theme['primary']};
        border-radius: 15px;
        padding: 10px;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        color: {current_theme['text']};
    }}
    QCheckBox {{
        color: {current_theme['text']};
        margin-top: 10px;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
    }}
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 1px solid {current_theme['primary']};
        border-radius: 5px;
        background-color: rgba(255, 255, 255, {current_theme['opacity']});
    }}
    QCheckBox::indicator:checked {{
        background-color: {current_theme['primary']};
    }}
    """

def get_title_style():
    return f"""
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: bold;
    color: {current_theme['primary']};
    margin-bottom: 20px;
    text-align: center;
    """

def get_author_label_style():
    return f"""
    QLabel {{
        font-family: 'Poppins', sans-serif;
        font-size: 12px;
        font-weight: bold;
        color: #121212
        padding: 10px;
        margin-top: 20px;
        text-align: center;
        /* Эффект свечения */
        text-shadow: 
            0 0 30px #4E8DF8,   /* Синее свечение */
            0 0 30px #4E8DF8,  /* Более интенсивное синее свечение */
            0 0 30px #56C6F2;  /* Голубое свечение */
        /* Анимация для плавного изменения цвета */
        animation: shine 3s infinite;
    }}
    @keyframes shine {{
        0% {{ color: #4E8DF8; text-shadow: 0 0 50px #4E8DF8, 0 0 10px #4E8DF8, 0 0 15px #56C6F2; }}
        50% {{ color: #56C6F2; text-shadow: 0 0 60px #56C6F2, 0 0 20px #56C6F2, 0 0 30px #4E8DF8; }}
        100% {{ color: #4E8DF8; text-shadow: 0 0 50px #4E8DF8, 0 0 10px #4E8DF8, 0 0 15px #56C6F2; }}
    }}
    """

def get_checkbox_style():
    return f"""
    QCheckBox {{
        color: {current_theme['text']};
        margin-top: 10px;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
    }}
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 1px solid {current_theme['primary']};
        border-radius: 5px;
        background-color: rgba(255, 255, 255, {current_theme['opacity']});
    }}
    QCheckBox::indicator:checked {{
        background-color: {current_theme['primary']};
    }}
    """

def get_input_style():
    return f"""
    QLineEdit, QSpinBox {{
        background-color: rgba(255, 255, 255, {current_theme['opacity']});
        border: 1px solid {current_theme['primary']};
        border-radius: 15px;
        padding: 10px;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        color: {current_theme['text']};
    }}
    QLineEdit:focus, QSpinBox:focus {{
        border-color: {current_theme['secondary']};
    }}
    """