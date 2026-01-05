# PDF Compression Tool
For scenarios where large PDFs (e.g., 10MB+) need to be compressed to a specified size (e.g., below 3MB), this tool resolves file occupation issues on Windows and compatibility problems with Python 3.7 and older dependency libraries. It achieves high compression ratios by converting PDFs to compressed images and reconstructing PDFs.

## Environment Requirements
1. Python Version: Python 3.7
2. Dependency Installation:

```bash
pip install -r requirements.txt
```


3. Additional Dependency: Install Poppler (for Windows) and add its `bin` directory to the system environment variables (Download link: https://github.com/oschwartz10612/poppler-windows/releases)

