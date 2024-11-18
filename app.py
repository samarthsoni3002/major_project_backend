from flask import Flask, send_file, request, jsonify
from excel_final_formation import final_formation
from recog import face_recog
from add_data import upload_data
from model import glove_detection

app = Flask(__name__)

# Function to create an Excel file
def create_excel_file():
    filename = final_formation()
    return filename

# Function to process face data
def process_face_data(icu):
    name, desg = face_recog()
    upload_data(desg, name, icu)
    return name

# Function to process gloves data
def process_gloves_data():
    predicted = glove_detection()
    if predicted:
        return "Gloves Predicted"
    else:
        return "Gloves not Predicted"

# Endpoint for root: simply prints "Running"
@app.route("/", methods=["GET"])
def home():
    return "Running"

# Endpoint to download an Excel file
@app.route("/download", methods=["GET"])
def download_excel():
    excel_file_path = create_excel_file()
    return send_file("HandHygiene_Compliance_Report.xlsx", as_attachment=True)

# Endpoint to handle "/face" logic
@app.route("/face", methods=["POST"])
def handle_face():
    input_string = request.json.get("input_string")
    if not input_string:
        return jsonify({"error": "Invalid input"}), 400
    result = process_face_data(input_string)
    return jsonify({"result": result})

# Endpoint to handle "/gloves" logic
@app.route("/gloves", methods=["GET"])
def handle_gloves():
    result = process_gloves_data()
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
