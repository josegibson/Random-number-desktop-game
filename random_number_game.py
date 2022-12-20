from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QStringListModel
import random
import sys


class Bet:
    def __init__(self, predicion, amount):
        self.prediction = predicion
        self.amount = amount
        self.balance = 0
        self.comment = ""

    def check_prize(self, number):
        if self.prediction == str(number):
            # correct prediction: add 10x bet_amount to balance
            self.balance = 10 * self.amount
            self.comment = (f"You got a jackpot on {self.prediction}")

        elif (self.prediction == "Odd" and number in [1, 3, 7, 9]) or (self.prediction == "Even" and number in [2, 4, 6, 8]):
            # both numbers are odd: add 2x bet_amount to balance
            self.balance = 2 * self.amount
            self.comment = (f"You got a double-return on {self.prediction}")

        elif self.prediction == "Lucky" and number in [0, 5]:
            # both numbers are 0 or 5: add 4x bet_amount to balance
            self.balance = 4 * self.amount
            self.comment = f"Bet just quadrupled for {self.prediction}"
        return self.balance, self.comment

class BetPage(QtWidgets.QWidget):
    def __init__(self, parent = None, core = None):
        super().__init__(parent)
        self.parent = parent
        self.denomination = 10
        self.initUI()
        self.bet_amount = 0
        self.prediction = None
        self.core = core

    def initUI(self):
        self.bet_amount_label = QtWidgets.QLabel("Enter the bet amount:")
        self.prediction_head_label = QtWidgets.QLabel()
        self.prediction_head_label.setStyleSheet("color: #FF0000;")
        self.back_button = QtWidgets.QPushButton("Back")
        self.confirm_button = QtWidgets.QPushButton("Confirm")

        self.denomination_buttons = []
        for i in range(3):
            button = QtWidgets.QPushButton(str(10**(i+1)))
            button.setProperty("denominationButton", True)
            button.setCheckable(True)  # make the button checkable
            self.denomination_buttons.append(button)

        self.denomination_buttons[0].setChecked(True)

        self.multiplier_decrement = QtWidgets.QPushButton("-")
        self.multiplier_increment = QtWidgets.QPushButton("+")
        self.multiplier_input = QtWidgets.QLineEdit("10")
        self.multiplier_input.setAlignment(Qt.AlignHCenter)

        denominations_layout = QtWidgets.QGridLayout()
        for i, button in enumerate(self.denomination_buttons):
            denominations_layout.addWidget(button, 0, i)

        multiplier_layout = QtWidgets.QGridLayout()
        multiplier_layout.addWidget(self.bet_amount_label, 0, 0)
        multiplier_layout.addWidget(self.multiplier_decrement, 0, 1)
        multiplier_layout.addWidget(self.multiplier_input, 0, 2)
        multiplier_layout.addWidget(self.multiplier_increment, 0, 3)

        buttons_layout = QtWidgets.QGridLayout()
        buttons_layout.addWidget(self.back_button, 0, 0)
        buttons_layout.addWidget(self.confirm_button, 0, 1)

        self.bet_amount_page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.prediction_head_label)
        layout.addLayout(multiplier_layout)
        layout.addLayout(denominations_layout)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.back_button.clicked.connect(self.back)
        self.confirm_button.clicked.connect(self.place_bet)
        self.multiplier_increment.clicked.connect(self.increase_multiplier)
        self.multiplier_decrement.clicked.connect(self.decrease_multiplier)
        for button in self.denomination_buttons:
            button.clicked.connect(self.set_denomination)

    def set_denomination(self):
        button = self.sender()
        self.denomination = int(button.text())
        self.multiplier_input.setText(button.text())
        for button in self.denomination_buttons:
            button.setChecked(False)

    def increase_multiplier(self):
        current_multiplier = int(self.multiplier_input.text())
        new_multiplier = current_multiplier + self.denomination
        self.multiplier_input.setText(str(new_multiplier))

    def decrease_multiplier(self):
        current_multiplier = int(self.multiplier_input.text())
        new_multiplier = current_multiplier - self.denomination
        if new_multiplier < 0:
            new_multiplier = 0
        self.multiplier_input.setText(str(new_multiplier))

    def place_bet(self):
        self.bet_amount = int(self.multiplier_input.text())

        if self.bet_amount > self.core.balance:  # check if the user has enough balance
            self.core.log_screen.addItem("Insufficient balance!")
            return

        self.core.bets.append(Bet(self.prediction, self.bet_amount))
        self.core.log_screen.addItem('Bet: {:5s}\tAmount: {}'.format(
            str(self.prediction), self.bet_amount))
        self.core.balance -= self.bet_amount
        self.core.balance_label.setText(f"Balance : {self.core.balance}")
        self.back()

    def back(self):
        # set the current index to the index of the prediction page
        self.parent.setCurrentIndex(0)

class PredictionPage(QtWidgets.QWidget):
    def __init__(self, parent=None, bet_page=None, core = None):
        super().__init__(parent)
        self.parent = parent
        self.bet_page = bet_page
        self.core = core
        self.initUI()

    def initUI(self):

        self.play_button = QtWidgets.QPushButton("Play")

        self.oel_buttons = [QtWidgets.QPushButton("Odd"),
                            QtWidgets.QPushButton("Even"), 
                            QtWidgets.QPushButton("Lucky")]

        for button in self.oel_buttons:
            button.setCheckable(True)
            button.setProperty("generalButton", True)

        # create round buttons for each number
        self.buttons = []
        for i in range(10):
            button = QtWidgets.QPushButton(str(i))
            button.setProperty("numberButton", True)
            button.setCheckable(True)  # make the button checkable
            self.buttons.append(button)


        # create prediction page
        button_layout = QtWidgets.QGridLayout()
        for i, button in enumerate(self.buttons):
            row = i // 5
            col = i % 5
            button_layout.addWidget(button, row, col)

        oel_button_layout = QtWidgets.QGridLayout()
        for i, button in enumerate(self.oel_buttons):
            oel_button_layout.addWidget(button, 0, i)

        layout_gen = QtWidgets.QHBoxLayout()
        layout_gen.addWidget(self.play_button)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(oel_button_layout)
        layout.addLayout(button_layout)
        layout.addLayout(layout_gen)

        self.setLayout(layout)

        for button in self.buttons + self.oel_buttons:
            button.clicked.connect(self.open_bet_page)
        # connect signals and slots
        self.play_button.clicked.connect(self.core.play)

    def open_bet_page(self):
        button = self.sender()
        self.bet_page.prediction = button.text()
        self.bet_page.prediction_head_label.setText(button.text())
        self.parent.setCurrentIndex(1)
        for button in self.buttons + self.oel_buttons:
            button.setChecked(False)

class LogScreen(QtWidgets.QListView):
    def __init__(self, parent=None, core = None):
        super().__init__(parent)
        self.core = core
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)

        # set the text color of the log screen
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
        self.setPalette(palette)
        self.setFixedWidth(350)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # set the background color of the log screen
        self.setStyleSheet(
            "background-color: #333333;color: #00FF80;border-radius: 10%;padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 20px;font-family: Courier New;font-size:16px")

        # Initialize the list model
        self.model =QStringListModel(self)
        # Set the list model for the list view
        self.setModel(self.model)

        # Connect the doubleClicked signal to the remove_item slot
        self.doubleClicked.connect(self.removeItem)

    def addItem(self, message):
        # Add the log message to the list model
        if len(message) > 0:
            self.model.insertRow(0)
            self.model.setData(self.model.index(0), message)

    def removeItem(self, index):
        # Remove the item at the given index from the list model
        self.model.removeRow(index.row())
        self.core.balance += self.core.bets[len(self.core.bets) - 1 - index.row()].amount
        self.core.bets.pop(len(self.core.bets) - 1 - index.row())
        self.core.balance_label.setText(f"Balance : {self.core.balance}")

class RandomNumberGame(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.balance = 100  # initial balance
        self.number = 0
        self.bets = []
        self.initUI()

    def initUI(self):
        # create widgets

        self.balance_label = QtWidgets.QLabel(f"Balance : {self.balance}")
        self.balance_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.balance_label.setStyleSheet("font-size:22px;background-color:#000000;color:#ffffff;border-radius:10%")
        self.balance_label.setFixedWidth(250)

        self.number_label = QtWidgets.QLabel("-")
        self.number_label.setStyleSheet("background-color: orange;border-radius:10%;font-size:24px;font-weight: bold")
        self.number_label.setFixedSize(50, 50)
        self.number_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.stacked_widget = QtWidgets.QStackedWidget()
        # add pages to stacked widget
        self.bet_amount_page = BetPage(self.stacked_widget, self)
        self.prediction_page = PredictionPage(self.stacked_widget, self.bet_amount_page, self)
        self.stacked_widget.addWidget(self.prediction_page)
        self.stacked_widget.addWidget(self.bet_amount_page)

        self.log_screen = LogScreen(core=self)

        self.body = QtWidgets.QHBoxLayout()
        self.body.addWidget(self.stacked_widget)
        self.body.addWidget(self.log_screen)

        self.top_layout = QtWidgets.QHBoxLayout()
        self.top_layout.addWidget(self.balance_label)
        self.top_layout.addWidget(self.number_label)

        # create main layout and add widgets
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(self.top_layout)
        main_layout.addLayout(self.body)

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                    background-color: #ffffff;
                    width:50px
                }
                QLabel {
                    color: #333333;
                    font-size: 16px;
                }
                QLineEdit {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #0088cc;
                    color: #ffffff;
                    font-size: 14px;
                    padding: 10px 20px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #33aadd;
                }
                QPushButton:pressed {
                    background-color: #0077bb;
                }
                QPushButton[generalButton="true"] {
                    background-color: #cc0000;
                }

                QPushButton[generalButton="true"]:checked {
                    background-color: #990000;
                }

                QPushButton[generalButton="true"]:hover {
                    background-color: #ff3333;
                }

                QPushButton[numberButton="true"] {
                    background-color: #00cc00;
                }

                QPushButton[numberButton="true"]:checked {
                    background-color: #009900;
                }

                QPushButton[numberButton="true"]:hover {
                    background-color: #33ff33;
                }

                """)



    def update_prediction(self):
        # reset prediction
        self.prediction = None
        self.latest_button = self.sender()
        # check which button is checked and set prediction accordingly
        if self.latest_button.text().isdigit():
            self.prediction = int(self.latest_button.text())
        else:
            self.prediction = self.latest_button.text()

        self.multiplier_input.setText("10")
        self.prediction_head_label.setText(str(self.prediction))
        self.stacked_widget.setCurrentIndex(1)

    def generate_number(self):
        self.number = random.randint(0, 9)

    def play(self):
        self.log_screen.addItem("------------------------------")
        self.generate_number()
        commentlen = 0
        for bet in self.bets:
            prize, comment = bet.check_prize(self.number)
            commentlen += len(comment)
            self.balance += prize
            self.log_screen.addItem(comment)
        if commentlen == 0:
            self.log_screen.addItem("Better luck next time!")
        self.number_label.setText(f"{self.number}")
        self.balance_label.setText(f"Balance : {self.balance}")

        # reset prediction and bet amount
        self.prediction = None
        self.bet_amount = 0
        self.bets = []

        # reset buttons

        self.log_screen.addItem("------------------------------")
        if self.balance == 0:
            self.log_screen.addItem("Game Over!")

