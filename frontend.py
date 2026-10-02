import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QSpinBox, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from backend import load_data, service_by_category, service_status, save_data

class CarMaintenance(QWidget):

    def __init__(self): # This line means "Define a function that runs automatically when this object (window) is created"
        super().__init__() # This line means "Run the original setup from QWidget before adding my custom stuff"
        self.setWindowTitle("Car Maintenance Tracker")
        self.resize(800,400)

        self.data = load_data()
        self.main_layout = QVBoxLayout() #This is making the main layout in vertical
        #self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout) #Means use this layout to organize everything in this window        

        self.build_main_menu()
        

        
    def show_fluids(self):
        self.clear_screen()

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.append("Fluids")
        fluid_services = service_by_category(self.data, "Fluids")
        for service in fluid_services:
            self.output_box.append(f"{service['name']} - every {service['interval']} miles")
        
        
        self.oil_button = QPushButton("Oil")
        self.wiperfluid_button = QPushButton("Wiper Fluid")
        self.back_button = QPushButton("Back")
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.oil_button)
        self.button_layout.addWidget(self.wiperfluid_button)
        
        self.main_layout.addWidget(self.output_box)
        self.main_layout.addLayout(self.button_layout)

        self.back_button.clicked.connect(self.build_main_menu)
        self.oil_button.clicked.connect(lambda: self.update_status("oil"))
        self.wiperfluid_button.clicked.connect(lambda: self.update_status("wiper"))
        

    def show_wheels(self):
        self.clear_screen()

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.append("Wheels")
        wheel_services = service_by_category(self.data, "Wheels")
        for service in wheel_services:
            self.output_box.append(f"{service['name']} - every {service['interval']} miles")

        self.tirerotation_button = QPushButton("Tire Rotation")
        self.brakepads_button = QPushButton("Brake pads")
        self.back_button = QPushButton("Back")

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.tirerotation_button)
        self.button_layout.addWidget(self.brakepads_button)

        self.main_layout.addWidget(self.output_box)
        self.main_layout.addLayout(self.button_layout)

        self.back_button.clicked.connect(self.build_main_menu)
        self.tirerotation_button.clicked.connect(lambda: self.update_status("tire"))
        self.brakepads_button.clicked.connect(lambda: self.update_status("brake"))

    def update_status(self, service_name):
        current_miles = self.data["current_miles"]
        for category in ["Fluids" , "Wheels"]:
            services = service_by_category(self.data, category)
            for service in services:
                if service_name.lower() in service["name"].lower():
                    service["last_done"] = current_miles
                    self.output_box.clear()
                    self.output_box.append(f"{service['name']} updated at {current_miles} miles")


    def show_status(self):
        self.output_box.clear()

        self.output_box.append(f"Current Mileage: {self.data['current_miles']} miles")
        statuses = service_status(self.data, self.data["current_miles"])
        for item in statuses:
            self.output_box.append(item["message"])

    def mileage_editor(self):
        self.clear_screen()

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.append("Adjust Current Mileage")

        self.digit_layout = QHBoxLayout()
        self.digit_boxes = []
        for place in ["100000" , "10000" , "1000" , "100" , "10" , "1"]:
            box = QSpinBox()
            box.setRange(0,9)
            box.setFixedHeight(60)

            self.digit_boxes.append(box)
            self.digit_layout.addWidget(QLabel(place))
            self.digit_layout.addWidget(box)

        current = self.data["current_miles"]
        digits = list(f"{current:06d}")
        
        for i in range(len(self.digit_boxes)):
            self.digit_boxes[i].setValue(int(digits[i]))

        self.confirm_button = QPushButton("Confirm")
        self.back_button = QPushButton("Back")

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addSpacing(80)
        self.button_layout.addWidget(self.confirm_button)
        self.button_layout.addStretch()


        self.button_layout.setSpacing(10)
        self.button_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addWidget(self.output_box, 2)
        self.main_layout.addLayout(self.digit_layout, 1)
        
        

        self.main_layout.addLayout(self.button_layout, 1)

        self.back_button.clicked.connect(self.build_main_menu)
        self.confirm_button.clicked.connect(self.save_mileage)

    def save_mileage(self):
        digits = [100000, 10000, 1000, 100, 10, 1]
        mileage = 0

        for i in range(len(self.digit_boxes)):
            mileage += self.digit_boxes[i].value() * digits[i]

        self.data["current_miles"] = mileage
        save_data(self.data)

        self.build_main_menu()
        
    def build_main_menu(self):
        self.clear_screen()

        self.button_layout = QHBoxLayout() #Makes the bottom half of layout in horizontal
        self.output_box = QTextEdit() #Provides the space for text
        self.output_box.setReadOnly(True) #Makes this read only 

        self.update_mileage_button = QPushButton("Update Mileage") #Creates the button with title
        self.fluids_button = QPushButton("Fluids")
        self.wheels_button = QPushButton("Wheels")

        self.button_layout.addWidget(self.update_mileage_button) #Adding to Horizontal layout (button_layout)
        self.button_layout.addWidget(self.fluids_button)
        self.button_layout.addWidget(self.wheels_button)

        self.main_layout.addWidget(self.output_box) #Add the text box to main layout (must be above buttons) *ORDER MATTERS*
        self.main_layout.addLayout(self.button_layout)

        

        self.fluids_button.clicked.connect(self.show_fluids)
        self.wheels_button.clicked.connect(self.show_wheels)
        self.update_mileage_button.clicked.connect(self.mileage_editor)

        self.show_status()
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget() is not None:
                item.widget().deleteLater()

            elif item.layout() is not None:
                self.clear_layout(item.layout())

    def clear_screen(self):
        self.clear_layout(self.main_layout)


        





app = QApplication(sys.argv) #Creates the qt application
window = CarMaintenance() #Makes one actual window object from class *Triggers __init__*
window.show() #Tells window to appear on screen
sys.exit(app.exec()) #Starts the GUI loop so it stays open and listens for clicks

