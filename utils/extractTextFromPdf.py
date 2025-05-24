import os
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import fitz  # PyMuPDF

def extract_text_from_pdf_url(pdf_url: str, download_dir: str = None, wait_time: int = 7) -> str:
    """
    Downloads PDF from the URL using Selenium and extracts text with PyMuPDF.

    Args:
        pdf_url (str): URL of the PDF file.
        download_dir (str, optional): Directory to download PDF. Defaults to current working directory.
        wait_time (int, optional): Seconds to wait for download to complete. Default is 7.

    Returns:
        str: Extracted text from PDF.
    """
    download_dir = download_dir or os.getcwd()
    pdf_filename = "temp_downloaded.pdf"
    pdf_path = os.path.join(download_dir, pdf_filename)

    # Create temporary Chrome profile directory
    temp_profile = tempfile.mkdtemp()

    options = Options()
    options.headless = True
    prefs = {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument(f"--user-data-dir={temp_profile}")

    driver = webdriver.Chrome(options=options)
    driver.get(pdf_url)

    time.sleep(wait_time)  # wait for the PDF to download

    driver.quit()

    # Find the downloaded PDF file in download_dir (newest PDF file)
    pdf_files = [f for f in os.listdir(download_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        raise FileNotFoundError("No PDF file found in download directory after download attempt.")

    # Get the most recently modified PDF file
    latest_pdf = max(pdf_files, key=lambda f: os.path.getmtime(os.path.join(download_dir, f)))

    # Rename it to our target file (overwrite if exists)
    src = os.path.join(download_dir, latest_pdf)
    if src != pdf_path:
        os.replace(src, pdf_path)

    # Extract text from the downloaded PDF
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()

    # Optional: clean up the downloaded PDF file if you want
    # os.remove(pdf_path)

    return text
