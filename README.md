# Text to Image Conversion

This directory contains scripts and resources for converting text into images and decoding images back into text. The primary purpose is to visualize text data in a graphical format and ensure accurate reconstruction of the original text.

## Files

- **`coscode.py`**: The main Python script that combines the functionality of text-to-image conversion and image-to-text decoding. It supports multiple encodings such as UTF-8, KOI8-U, Windows-1251, and ASCII.
- **`output_ascii.png`**: Example output image generated from ASCII-encoded text.
- **`output_koi8-u.png`**: Example output image generated from KOI8-U-encoded text.
- **`output_utf-8.png`**: Example output image generated from UTF-8-encoded text.
- **`output_windows-1251.png`**: Example output image generated from Windows-1251-encoded text.

## Usage

1. **Run the script**:
   ```bash
   python3 coscode.py
   ```
   This will generate images for predefined text samples in various encodings and attempt to decode them back to verify accuracy.

2. **Supported Encodings**:
   - UTF-8
   - KOI8-U
   - Windows-1251
   - ASCII

3. **Output**:
   - The script generates PNG images for each encoding and saves them in this directory.
   - It also validates the consistency of the conversion process by comparing the original text with the decoded text.

## Example

For the encoding `ASCII`, the script will:
- Convert the text `"Hello, world! This is a test."` into an image.
- Decode the image back into text.
- Verify that the decoded text matches the original.

## Dependencies

- Python 3.x
- Pillow library for image processing

Install dependencies using pip:
```bash
pip install pillow
```

## Notes

- Ensure that the `text_to_image` directory is writable, as the script saves output images here.
- The script is designed to handle encoding errors gracefully and will skip unsupported text for a given encoding.

## License

This project is open-source and available under the MIT License.