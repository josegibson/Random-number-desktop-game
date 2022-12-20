from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
import random


class RandomNumberGame(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.prediction = None  # store the prediction made by the user
        self.balance = 100  # initial balance
        self.bet_amount = 0
        self.number = 0
        self.denomination = 10
        self.latest_button = None
        self.init_ui()

    def init_ui(self):
        # create widgets
        self.bet_amount_label = QtWidgets.QLabel("Enter the bet amount:")
        self.bet_amount_input = QtWidgets.QLineEdit()
        self.prediction_label = QtWidgets.QLabel("Make a prediction:")
        self.odd_button = QtWidgets.QPushButton("Odd")
        self.even_button = QtWidgets.QPushButton("Even")
        self.lucky_button = QtWidgets.QPushButton("Lucky")
        self.play_button = QtWidgets.QPushButton("Play")
        self.exit_button = QtWidgets.QPushButton("Exit")
        self.result_label = QtWidgets.QLabel()
        self.result_label.setStyleSheet("color: #FF0000;")
        self.balance_label = QtWidgets.QLabel(f"Your current balance is: {self.balance}")
        self.balance_label.setAlignment(Qt.AlignHCenter)

        self.odd_button.setCheckable(True)
        self.odd_button.setProperty("generalButton", True)
        self.even_button.setCheckable(True)
        self.even_button.setProperty("generalButton", True)
        self.lucky_button.setCheckable(True)
        self.lucky_button.setProperty("generalButton", True)

        #bet page widgets
        self.bet_page_back_button = QtWidgets.QPushButton("Back")
        self.bet_page_confirm_button = QtWidgets.QPushButton("Confirm")

        self.bet_page_denomination_10 = QtWidgets.QPushButton("10")
        self.bet_page_denomination_10.setCheckable(True)
        self.bet_page_denomination_10.setChecked(True)
        self.bet_page_denomination_10.setProperty("generalButton", True)
        self.bet_page_denomination_100 = QtWidgets.QPushButton("100")
        self.bet_page_denomination_100.setCheckable(True)
        self.bet_page_denomination_100.setProperty("generalButton", True)
        self.bet_page_denomination_1000 = QtWidgets.QPushButton("1000")
        self.bet_page_denomination_1000.setCheckable(True)
        self.bet_page_denomination_1000.setProperty("generalButton", True)
        self.bet_page_multiplier_decrement = QtWidgets.QPushButton("-")
        self.bet_page_multiplier_increment = QtWidgets.QPushButton("+")
        self.bet_page_multiplier_input = QtWidgets.QLineEdit("10")
        self.bet_page_multiplier_input.setAlignment(Qt.AlignHCenter)

        # create round buttons for each number
        self.buttons = []
        for i in range(10):
            button = QtWidgets.QPushButton(str(i))
            button.setProperty("numberButton", True)
            button.setCheckable(True)  # make the button checkable
            self.buttons.append(button)

        # create stacked widget
        self.stacked_widget = QtWidgets.QStackedWidget()

        # create prediction page
        button_layout = QtWidgets.QGridLayout()
        for i, button in enumerate(self.buttons):
            row = i // 5
            col = i % 5
            button_layout.addWidget(button, row, col)

        general_button_layout = QtWidgets.QGridLayout()
        general_button_layout.addWidget(self.odd_button, 0, 0)
        general_button_layout.addWidget(self.even_button, 0, 1)
        general_button_layout.addWidget(self.lucky_button, 0, 2)

        self.prediction_page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(general_button_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.play_button)
        layout.addWidget(self.exit_button)
        
        self.prediction_page.setLayout(layout)

        # create bet amount page
        bet_denominations_layout = QtWidgets.QGridLayout()
        bet_denominations_layout.addWidget(self.bet_page_denomination_10, 0, 0)
        bet_denominations_layout.addWidget(self.bet_page_denomination_100, 0, 1)
        bet_denominations_layout.addWidget(self.bet_page_denomination_1000, 0, 2)
        
        bet_multiplier_layout = QtWidgets.QGridLayout()
        bet_multiplier_layout.addWidget(self.bet_amount_label, 0, 0)
        bet_multiplier_layout.addWidget(self.bet_page_multiplier_decrement, 0, 1)
        bet_multiplier_layout.addWidget(self.bet_page_multiplier_input, 0, 2)
        bet_multiplier_layout.addWidget(self.bet_page_multiplier_increment, 0, 3)

        bet_buttons_layout = QtWidgets.QGridLayout()
        bet_buttons_layout.addWidget(self.bet_page_back_button, 0, 0)
        bet_buttons_layout.addWidget(self.bet_page_confirm_button, 0, 1)

        self.bet_amount_page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(bet_multiplier_layout)
        layout.addLayout(bet_denominations_layout)
        layout.addWidget(self.result_label)
        layout.addLayout(bet_buttons_layout)

        self.bet_amount_page.setLayout(layout)

        # add pages to stacked widget
        self.stacked_widget.addWidget(self.prediction_page)
        self.stacked_widget.addWidget(self.bet_amount_page)

        # create a QListWidget for the log screen
        self.log_screen = QtWidgets.QListWidget()
        # set the font of the log screen
        font = QtGui.QFont()
        font.setPointSize(10)
        self.log_screen.setFont(font)

        # set the text color of the log screen
        palette = self.log_screen.palette()
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
        self.log_screen.setPalette(palette)

        # set the background color of the log screen
        self.log_screen.setStyleSheet("background-color: #333333;color: #00FF80;border-radius: 10%;padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 20px;")

        self.pre_main_layout = QtWidgets.QHBoxLayout()
        self.pre_main_layout.addWidget(self.stacked_widget)
        self.pre_main_layout.addWidget(self.log_screen)

        # create main layout and add widgets
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.balance_label)
        main_layout.addLayout(self.pre_main_layout)

        self.setLayout(main_layout)

        self.buttons.append(self.odd_button)
        self.buttons.append(self.even_button)
        self.buttons.append(self.lucky_button)

        # connect signals and slots
        self.play_button.clicked.connect(self.play)
        self.exit_button.clicked.connect(self.close)
        for button in self.buttons:
            button.clicked.connect(self.update_prediction)
        self.bet_page_back_button.clicked.connect(self.back)
        self.bet_page_confirm_button.clicked.connect(self.place_bet)
        self.bet_page_multiplier_increment.clicked.connect(self.increase_multiplier)
        self.bet_page_multiplier_decrement.clicked.connect(self.decrease_multiplier)
        self.bet_page_denomination_10.clicked.connect(self.set_denomination)
        self.bet_page_denomination_100.clicked.connect(self.set_denomination)
        self.bet_page_denomination_1000.clicked.connect(self.set_denomination)

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

    def set_denomination(self):
        button = self.sender()
        self.denomination = int(button.text())
        self.bet_page_multiplier_input.setText(button.text())
        self.bet_page_denomination_10.setChecked(False)
        self.bet_page_denomination_100.setChecked(False)
        self.bet_page_denomination_1000.setChecked(False)
        button.setChecked(True)

    def increase_multiplier(self):
        current_multiplier = int(self.bet_page_multiplier_input.text())
        new_multiplier = current_multiplier + self.denomination
        self.bet_page_multiplier_input.setText(str(new_multiplier))

    def decrease_multiplier(self):
        current_multiplier = int(self.bet_page_multiplier_input.text())
        new_multiplier = current_multiplier - self.denomination
        if new_multiplier < 0:
            new_multiplier = 0
        self.bet_page_multiplier_input.setText(str(new_multiplier))

    def update_prediction(self):
        # reset prediction
        self.prediction = None
        self.latest_button = self.sender()
        # check which button is checked and set prediction accordingly
        if self.latest_button.text().isdigit():
            self.prediction = int(self.latest_button.text())
        else:
            self.prediction = self.latest_button.text()
        
        self.bet_page_multiplier_input.setText("10")
        self.stacked_widget.setCurrentIndex(1)

    def generate_number(self):
        self.number = random.randint(0, 9)

    def calculate_score(self):
        prediction = self.prediction
        if isinstance(prediction, int):
            # prediction is a number
            if prediction == self.number:
                # correct prediction: add 10x bet_amount to balance
                self.balance += 10 * self.bet_amount
        elif isinstance(prediction, str):
            # prediction is a string
            if prediction == "Odd" and self.number in [1, 3, 7, 9]:
                # both numbers are odd: add 2x bet_amount to balance
                self.balance += 2 * self.bet_amount
            elif prediction == "Even" and self.number in [2, 4, 6, 8]:
                # both numbers are even and not 0 or 5: add 2x bet_amount to balance
                self.balance += 2 * self.bet_amount
            elif prediction == "Lucky" and self.number in [0, 5]:
                # both numbers are 0 or 5: add 4x bet_amount to balance
                self.balance += 4 * self.bet_amount
        self.balance_label.setText(f"Your current balance is: {self.balance}")

    def place_bet(self):
        self.bet_amount = int(self.bet_page_multiplier_input.text())

        if self.bet_amount > self.balance:  # check if the user has enough balance
            self.result_label.setText(
                "Insufficient balance. Please enter a valid bet amount.")
            return

        self.log_screen.addItem(f"Bet: {self.prediction}\t    Amount: {self.bet_amount}")
        self.balance -= self.bet_amount
        self.balance_label.setText(f"Your current balance is: {self.balance}")
        self.stacked_widget.setCurrentIndex(0)

    def back(self):
        # set the current index to the index of the prediction page
        self.latest_button.setChecked(False)
        self.stacked_widget.setCurrentIndex(0)
        
    def play(self):

        self.generate_number()
        print("number generated!")
        self.calculate_score()
        print("score calculated!")
        self.result_label.setText(
            f"You predicted: {self.prediction}\nThe number was: {self.number}")
        self.balance_label.setText(
            f"Your current balance is: {self.balance}")

        # reset prediction and bet amount
        self.prediction = None
        self.bet_amount = 0

        # reset buttons
        for button in self.buttons:
            button.setChecked(False)
        self.odd_button.setChecked(False)
        self.even_button.setChecked(False)
        self.lucky_button.setChecked(False)

