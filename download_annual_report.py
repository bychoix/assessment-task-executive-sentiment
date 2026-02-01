import os
import random
import time
from playwright.sync_api import sync_playwright

d_companies = {
    "Tesla": {"ticker": "TSLA", "exchange": "NASDAQ", "country": "US"},
    "BMW": {"ticker": "BMW.DE", "exchange": "Xetra", "country": "EU"},
    "Volkswagen": {"ticker": "VOW3.DE", "exchange": "Xetra", "country": "EU"},
    "Benz": {"ticker": "MBG.DE", "exchange": "Xetra", "country": "EU"},
    "Toyota": {"ticker": "7203.T", "exchange": "Tokyo", "country": "JP"},
    "Stellantis": {"ticker": "STLA", "exchange": "NYSE", "country": "EU"},
    "Bosch": {"ticker": "BOS.IN", "exchange": "IN", "country": "IN"},
    "Apple": {"ticker": "AAPL", "exchange": "NASDAQ", "country": "US"},
    "Microsoft": {"ticker": "MSFT", "exchange": "NASDAQ", "country": "US"},
    "Intel": {"ticker": "INTC", "exchange": "NASDAQ", "country": "US"},
    "Qualcomm": {"ticker": "QCOM", "exchange": "NASDAQ", "country": "US"},
    "Nvdia": {"ticker": "NVDA", "exchange": "NASDAQ", "country": "US"},
    "SAP": {"ticker": "SAP", "exchange": "NYSE / Xetra", "country": "EU"},
    "IBM": {"ticker": "IBM", "exchange": "NYSE", "country": "US"},
    "Jpmorgan": {"ticker": "JPM", "exchange": "NYSE", "country": "US"},
    "Goldman": {"ticker": "GS", "exchange": "NYSE", "country": "US"},
    "HSBC": {"ticker": "HSBC", "exchange": "NYSE", "country": "EU"},
    "Blackrock": {"ticker": "BLK", "exchange": "NYSE", "country": "US"},
    "Citigroup": {"ticker": "C", "exchange": "NYSE", "country": "US"},
    "Pfizer": {"ticker": "PFE", "exchange": "NYSE", "country": "US"},
    "J&J": {"ticker": "JNJ", "exchange": "NYSE", "country": "US"},
    "Nestle": {"ticker": "NESN.SW", "exchange": "Swiss", "country": "EU"},
    "Loreal": {"ticker": "OR.PA", "exchange": "Paris", "country": "EU"},
    "Shiseido": {"ticker": "4911.T", "exchange": "Tokyo", "country": "JP"},
    "P&G": {"ticker": "PG", "exchange": "NYSE", "country": "US"}
}

output_dir = "annual_reports"

def get_slug(name, data):
    """Generates the AnnualReports.com slug logic."""
    if name == "Bosch": return None
    
    # --- UPDATED MANUAL OVERRIDES ---
    if name == "BMW": return "OTC_BAMGF"
    if name == "Volkswagen": return "OTC_VWAGY"
    if name == "Benz": return "OTC_MBGAF"
    if name == "Nestle": return "OTC_NSRGY"
    
    # Other Manual Overrides
    if name == "Toyota": return "NYSE_TM"
    if name == "Loreal": return "Loreal_SA"
    if name == "Shiseido": return "Shiseido_Company_Limited"

    # Standard "EXCHANGE_TICKER" logic
    exchange = data['exchange']
    ticker = data['ticker']
    if "NYSE" in exchange: return f"NYSE_{ticker}"
    if "NASDAQ" in exchange: return f"NASDAQ_{ticker}"
    return None

def download_reports_sync():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with sync_playwright() as p:
        # We still launch the browser to generate valid cookies/headers
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        # We don't even need 'page' for the download, we use the context's request API
        # but we create one just to hold the session alive visually if you want to watch
        page = context.new_page()

        print("--- Starting Download Loop (API Fetch Mode) ---")

        for company_name, data in d_companies.items():
            slug = get_slug(company_name, data)
            if not slug: continue

            # Clean slug logic
            clean_slug = slug.replace("NASDAQ_", "").replace("NYSE_", "").replace("OTC_", "")
            first_letter = clean_slug[0].lower()

            company_folder = os.path.join(output_dir, company_name)
            if not os.path.exists(company_folder):
                os.makedirs(company_folder)

            print(f"\nProcessing {company_name}...")

            for year in range(2010, 2026):
                filename = f"{slug}_{year}.pdf"
                url = f"https://www.annualreports.com/HostedData/AnnualReportArchive/{first_letter}/{filename}"
                save_path = os.path.join(company_folder, filename)

                if os.path.exists(save_path):
                    continue
                
                try:
                    # Random throttle
                    time.sleep(random.uniform(10, 15))

                    # --- THE FIX: USE API REQUEST, NOT PAGE NAVIGATION ---
                    # This fetches the file stream directly, bypassing the PDF Viewer
                    response = context.request.get(url)

                    if response.status == 200:
                        body = response.body()
                        
                        # Validate it is actually a PDF (Magic bytes %PDF)
                        if body.startswith(b'%PDF'):
                            with open(save_path, 'wb') as f:
                                f.write(body)
                            print(f"  [SUCCESS] {filename} ({len(body)//1024} KB)")
                        else:
                            # If it's 200 OK but not a PDF, it's likely the HTML redirect/error page
                            print(f"  [FAILED] {filename} - Content was HTML/Text, not PDF. (Size: {len(body)} bytes)")
                    
                    elif response.status == 404:
                        print(f"  [404] Not Found: {year}")
                    
                    elif response.status == 429:
                        print(f"  [429] Rate Limit. Pausing 60s...")
                        time.sleep(60)

                except Exception as e:
                    print(f"  [ERROR] {e}")

        browser.close()
        print("\n--- Done ---")

if __name__ == "__main__":
    download_reports_sync()