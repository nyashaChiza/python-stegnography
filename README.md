# Django Steganography App

## Overview

This project is a Django web application that allows users to securely hide text messages or files within images using steganography. Users can upload a file or message, encode it into an image, and later decode the image to retrieve the hidden data.

## Features

- **User Authentication:** Users can log in to access the app's features.
- **File Upload:** Users can upload text files or other documents to be hidden inside an image.
- **Steganography:** The app encodes the uploaded file or message into an image using the Least Significant Bit (LSB) method.
- **Image Download:** After encoding, users can download the stego image that contains the hidden data.
- **File Retrieval:** Users can upload a stego image to decode and retrieve the hidden file or message.

## Requirements

- Python 3.8+
- Django 3.2+
- Pillow (Python Imaging Library)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/django-steganography.git
   cd django-steganography
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the app:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

### Encoding Data into an Image

1. Log in to the application.
2. Go to the "Hide File in Image" page.
3. Upload the file or message you want to hide and select a cover image.
4. Click "Encode" to generate the stego image.
5. Download the generated stego image.

### Decoding Data from an Image

1. Log in to the application.
2. Go to the "Retrieve File from Image" page.
3. Upload the stego image.
4. Click "Decode" to retrieve and download the hidden file or message.

## Project Structure

- `stego_app/` - Main Django project directory.
- `steganography/` - Django app handling the steganography functionality.
  - `models.py` - Optional database models (if needed).
  - `views.py` - Handles the encoding and decoding logic.
  - `forms.py` - Forms for file uploads.
  - `stego_utils.py` - Contains the steganography functions for encoding and decoding.
  - `templates/steganography/` - HTML templates for encoding and decoding pages.
- `static/` - Static files (CSS, JavaScript).
- `media/` - Directory for uploaded files and images (if configured).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Contact

For any inquiries or support, please contact [yourname@example.com](mailto:yourname@example.com).
```

Replace placeholders like `yourusername` and `yourname@example.com` with your actual GitHub username and contact email. This `README.md` provides an overview, installation steps, usage instructions, and project structure details for your Django Steganography app.
