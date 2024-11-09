# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from openai import OpenAI
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize OpenAI client
client = OpenAI(api_key='your-api-key-here')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Invalid file format. Please upload an Excel file.'}), 400

    try:
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read Excel file
        df = pd.read_excel(filepath)
        
        # Process each row
        results = []
        for index, row in df.iterrows():
            # Convert row to string for GPT processing
            row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
            
            # Process with GPT
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant processing Excel data."},
                    {"role": "user", "content": f"Please analyze this data: {row_text}"}
                ]
            )
            
            # Store results
            results.append({
                'row_number': index + 1,
                'original_data': row_text,
                'gpt_response': response.choices[0].message.content
            })
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
