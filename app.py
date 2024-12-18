from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.txt'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            sentences = content.split('. ')
            # print(sentences)
            return jsonify({'message': sentences}),200

    if file and file.filename.endswith(('.xls', '.xlsx')):
        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file)

            # Convert DataFrame to JSON (or process it as needed)
            data = df.to_dict(orient='records')
            return jsonify({"data": data}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)