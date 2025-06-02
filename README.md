# Local AI Writer with LM Studio

Simple web interface for text generation using LM Studio's local API.

## Quick Start

1. **Start LM Studio**
   - Start local server at http://127.0.0.1:1234

2. **Install & Run**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

3. **Use App**
   - Open http://localhost:5000
   - Enter prompt
   - Adjust temperature
   - Click Generate

## Features

- Clean web interface
- Temperature control
- Response logging
- Local inference only

## Project Structure

```
├── app.py              # Main application
├── requirements.txt    # Dependencies
└── logs/              # Interaction logs
```

## Requirements

- Python 3.8+
- LM Studio running locally

## Troubleshooting

- Verify LM Studio is running on port 1234
- Check port 5000 is available
- See logs for details

## License

MIT