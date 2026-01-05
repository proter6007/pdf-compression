import os
import tempfile
import shutil
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PIL import Image
from fpdf import FPDF

def deep_compress_pdf_to_3mb(input_path, output_path, target_size_mb=3, dpi=120, quality=35):
    """
    Deep compress PDF to the specified size (adapted for Python 3.7 + old libraries + Windows system)
    Solve file occupation issues and ensure 5MB PDF can be compressed to below 3MB
    """
    # Check input file existence
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File does not exist: {input_path}")
    original_size = os.path.getsize(input_path) / 1024 / 1024
    print(f"Original file size: {original_size:.2f} MB, Target compression size: below {target_size_mb} MB")

    # Step 1: Create temporary directory (manually created to avoid permission issues of automatic cleanup)
    temp_dir = os.path.join(tempfile.gettempdir(), "pdf_compress_temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    img_paths = []
    try:
        # Step 2: Convert PDF to images (reduce dpi as core compression method)
        # dpi=60 ensures sufficient resolution and small file size
        pages = convert_from_path(input_path, dpi)  
        
        for i, page in enumerate(pages):
            # Step 3: Compress image quality (quality=35 ensures compression to below 3MB)
            img_path = os.path.join(temp_dir, f"page_{i}.jpg")
            # Close file handle immediately after saving to avoid occupation
            with open(img_path, 'wb') as f:
                page.save(f, "JPEG", quality=quality, optimize=True)
            img_paths.append(img_path)

        # Step 4: Regenerate PDF (adapted for old fpdf version, no file occupation)
        if img_paths:
            first_img = Image.open(img_paths[0])
            img_width, img_height = first_img.size
            first_img.close()  # Critical step: close image handle to release occupation
            
            # Initialize PDF with specified page size
            pdf = FPDF(unit="pt", format=(img_width, img_height))
            
            for img_path in img_paths:
                pdf.add_page()
                # Open image and close immediately to avoid long-term occupation
                with Image.open(img_path) as img:
                    pdf.image(img_path, x=0, y=0, w=img_width, h=img_height)

        # Save compressed PDF
        pdf.output(output_path)

        # Verify compression result
        compressed_size = os.path.getsize(output_path) / 1024 / 1024
        compression_ratio = (1 - compressed_size / original_size) * 100
        print(f"✅ Compression completed!")
        print(f"Compressed size: {compressed_size:.2f} MB")
        print(f"Compression ratio: {compression_ratio:.2f}%")
        
        if compressed_size > target_size_mb:
            print(f"⚠️ Target not achieved! Try modifying dpi to 50 and quality to 30")

    except Exception as e:
        print(f"❌ Compression failed: {e}")
    finally:
        # Step 5: Clean up temporary files (force delete to solve occupation issue)
        try:
            # Delay 1 second to ensure all handles are released
            import time
            time.sleep(1)
            # Recursively delete directory and all files (ignore occupation, for Windows only)
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"🗑️ Temporary files cleaned up")
        except:
            print(f"⚠️ Failed to clean temporary files, please delete manually: {temp_dir}")

# Example call
if __name__ == "__main__":
    input_pdf = "input.pdf"  # PDF file to be compressed
    output_pdf = "output.pdf"  # Output file
    # Parameter explanation:
    # - target_size_mb=3: The expected maximum size of the compressed PDF (unit: MB)
    # - dpi=120: Resolution of PDF-to-image conversion (dots per inch), 120 DPI ensures clear text while controlling size
    # - quality=35: JPEG image compression quality (range 0-100), 35 balances compression ratio and image readability
    deep_compress_pdf_to_3mb(input_pdf, output_pdf, target_size_mb=3, dpi=120, quality=35)