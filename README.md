To gauge the sentiment of company executives for Task1, Shareholder Letters from the annual reports published by the companies as well as MD&A (Management’s Discussion and Analysis) from 10-Ks submitted to the SEC were used.  These sources were chosen as they are formally published by a team of executives of the firm on an annual basis and are expected to be scrutinized by the public as well as governmental regulators.  The data was scraped by accessing EDGAR (SEC) and annualreport.com using several python scripts found in the Github repo, CEO/China Sentiment Analysis-Task1: EDGAR.ipynb and CEO/China Sentiment Analysis-Task1: Annual Report.py.  While EDGAR has a public API, the annual reports needed to be downloaded through an actual browser using playwright.  The texts were then filtered for any mentions of the word “China” and the filtered texts were further fed into Gemini 3 for a short summary and sentiment analysis.  The final output is 125 rows of summarized commentary saved in *CEO Sentiment (Shareholder Letter, 10-K MD&A).xlsx*.

Regarding identifying the policies affecting the company for Task2, 10 policies have been handpicked based on media exposure, and saved in *Policy and Regulation (Official Documents from US and China).xlsx*.


# Executive Sentiment Analysis: CEO Narratives and Policy Exposure

## Overview

This project analyzes the sentiment of company executives and their exposure to regulatory policies through analysis of CEO narratives from shareholder letters and Management's Discussion & Analysis (MD&A) sections of 10-K annual reports.

## Project Structure

### Task 1: Executive Sentiment Analysis
Analyzes the sentiment expressed by company executives in:
- **Shareholder Letters** - Direct communications from annual reports
- **MD&A (Management's Discussion and Analysis)** - From 10-K filings

This sentiment analysis helps understand executive outlook, confidence levels, and strategic positioning.

### Task 2: Policy Impact Assessment
Examines how regulatory policies affect companies through:
- Analysis of **10 handpicked policies** with high media exposure
- **Official documents** from US and China regulatory sources
- Cross-referencing executive narratives with relevant policy exposure

## Data Files

- `CEO Sentiment (Shareholder Letter, 10-K Management Discussion).xlsx` - Sentiment analysis dataset from executive communications
- `Policy and Regulation (Official Documents from US and China).xlsx` - Policy documents and regulatory information
- `From CEO Narratives and Policy Exposure to Research Questions.pdf` - Detailed research framework and methodology
- `Synthesis Memo.pdf` - Summary findings and key insights

## Scripts

- `download_annual_report.py` - Utility script for downloading annual reports
