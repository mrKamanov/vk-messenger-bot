# Copyright <2025> <Сергей Каманов>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


def get_global_style():
    """
    Возвращает глобальный стиль для главного окна приложения.
    """
    return """
    QMainWindow {
        background-color: #f9f9f9;  /* Цвет фона главного окна */
    }
    QLabel {
        margin-bottom: 10px;  /* Отступ снизу для меток */
    }
    QLineEdit, QSpinBox {
        background-color: #ecf0f1;  /* Цвет фона полей ввода */
        border: 1px solid #bdc3c7;  /* Граница полей ввода */
        border-radius: 10px;  /* Скругление углов */
        padding: 10px;  /* Поля внутри полей ввода */
    }
    QPushButton {
        background-color: #9d3b3f;  /* Цвет фона кнопок */
        color: white;  /* Цвет текста на кнопках */
        border: none;  /* Без границы */
        border-radius: 15px;  /* Скругление углов */
        padding: 15px 30px;  /* Поля внутри кнопок */
    }
    QPushButton:hover {
        background-color: #2980b9;  /* Цвет фона кнопок при наведении */
    }
    QCheckBox {
        color: #2c3e50;  /* Цвет текста чекбоксов */
    }
    """

def get_button_style():
    """
    Возвращает стиль для обычных кнопок.
    """
    return """
    background-color: #9d3b3f;  /* Цвет фона кнопок */
    color: white;  /* Цвет текста на кнопках */
    border: none;  /* Без границы */
    border-radius: 15px;  /* Скругление углов */
    padding: 15px 30px;  /* Поля внутри кнопок */
    """

def get_start_script_button_style():
    """
    Возвращает стиль для кнопки "Запустить скрипт".
    """
    return """
    background-color: #2cac4c;  /* Цвет фона кнопки "Запустить скрипт" */
    color: white;  /* Цвет текста на кнопке */
    border: none;  /* Без границы */
    border-radius: 15px;  /* Скругление углов */
    padding: 15px 30px;  /* Поля внутри кнопки */
    """

def get_label_style():
    """
    Возвращает стиль для меток (QLabel).
    """
    return """
    color: #2c3e50;  /* Цвет текста меток */
    """

def get_title_style():
    """
    Возвращает стиль для заголовка приложения.
    """
    return """
    font-family: Roboto;  /* Шрифт */
    font-size: 24px;  /* Размер шрифта */
    font-weight: bold;  /* Жирность шрифта */
    color: #3498db;  /* Цвет текста */
    margin-bottom: 20px;  /* Отступ снизу */
    text-align: center;  /* Выравнивание по центру */
    """

def get_input_style():
    """
    Возвращает стиль для полей ввода (QLineEdit, QSpinBox).
    """
    return """
    font-family: Roboto;  /* Шрифт */
    font-size: 14px;  /* Размер шрифта */
    """

def get_checkbox_style():
    """
    Возвращает стиль для чекбоксов (QCheckBox).
    """
    return """
    color: #2c3e50;  /* Цвет текста чекбоксов */
    margin-top: 10px;  /* Отступ сверху */
    """

def get_author_label_style():
    """
    Возвращает стиль для метки с информацией об авторе приложения.
    """
    return """
    font-family: Roboto;  /* Шрифт */
    font-size: 12px;  /* Размер шрифта */
    color: #7f8c8d;  /* Цвет текста */
    margin-top: 20px;  /* Отступ сверху */
    text-align: center;  /* Выравнивание по центру */
    """ 
