# Excel GPT Processor

A web-based application that processes Excel files row by row using OpenAI's GPT models. Upload your Excel file through an intuitive interface and get AI-powered analysis for each row of your data.

## Features

- 🌐 Web-based interface with drag-and-drop file upload
- 📊 Excel file processing (.xlsx and .xls support)
- 🤖 GPT-powered analysis of each row
- ⚡ Real-time processing feedback
- 🎨 Clean, responsive UI using Tailwind CSS
- 🔒 Secure file handling and validation

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/excel-gpt-processor.git
cd excel-gpt-processor
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install flask pandas openpyai python-dotenv
```

4. Create environment file:
```bash
# Create .env file in the project root
touch .env

# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=your-api-key-here" >> .env
```

## Project Structure

```
excel-gpt-processor/
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   └── index.html     # Main interface
├── uploads/           # Temporary file storage
├── .env              # Environment variables
└── README.md         # This file
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload an Excel file using either:
   - Drag and drop into the designated area
   - Click to select file from your computer

4. Wait for processing to complete
5. View results for each row in the results section

## Customization

### Modifying GPT Prompts

To customize how GPT processes each row, modify the prompt in `app.py`:

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Your custom system prompt here"},
        {"role": "user", "content": f"Your custom prompt here: {row_text}"}
    ]
)
```

### Adjusting File Size Limits

The default maximum file size is 16MB. To change this, modify in `app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Change to desired size in bytes
```

## Security Considerations

- Files are automatically deleted after processing
- Filenames are sanitized using `secure_filename`
- File type validation prevents non-Excel uploads
- Maximum file size limit prevents large file uploads

## Error Handling

The application includes error handling for:
- Missing files
- Invalid file formats
- Processing errors
- API failures

Error messages are displayed in the UI for user feedback.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Flask framework
- Uses OpenAI's GPT API
- Styled with Tailwind CSS

## Support

For support, please open an issue in the repository or contact [your-email@example.com].

## Roadmap

- [ ] Add batch processing capabilities
- [ ] Implement progress tracking for large files
- [ ] Add export options for results
- [ ] Include template system for custom prompts
- [ ] Add user authentication