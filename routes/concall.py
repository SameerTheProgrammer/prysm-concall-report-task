from fastapi import APIRouter, HTTPException, status
from config.db import get_db_connection
from utils.getGeminiResponse import analyze_concall_report
from utils.extractTextFromPdf import extract_text_from_pdf_url

concall_router = APIRouter()

@concall_router.get("/")
def read_all_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT ID, TickerName, Links FROM Concall_links")
        data = cursor.fetchall()

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch data: {err}")
    finally:
        cursor.close()
        connection.close()
    return {
        "message": "Concall data fetched for all tickers successfully",
        "status": "success",
        "data": data
    }

# Fetch the last 2 earnings conference calls (concall) transcripts link for a given stock ticker, extract the relevant content from file link, and analyze it using an AI model to generate insights and a concise summary.
@concall_router.get("/{ticker_name}")
def read_summary_of_concall_report_by_ticker(ticker_name: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT ID, TickerName, Links FROM Concall_links WHERE TickerName = %s", (ticker_name,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Concall data not found")
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch data: {err}")
    finally:
        cursor.close()
        connection.close()

    content = []
    try:
        for report_link in data[2][:2]:
            text = extract_text_from_pdf_url(pdf_url=report_link)
            print(text)
            if not text:
                raise ValueError(f"No text extracted from {report_link}")
            content.append(text)
            break
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract content from {ticker_name}'s concall report: {err}"
        )

    try:
        full_transcript = "\n\n".join(content)
        ai_response = analyze_concall_report(transcript=full_transcript)
    except Exception as err:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to analyse {ticker_name}'s concall reports: {err}")

    return {
        "message": f"Concall data fetched for ticker {ticker_name} successfully",
        "status": "success",
        "data": ai_response
    }
