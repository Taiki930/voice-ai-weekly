"""
Voice AI Weekly Report - Main entry point.

Orchestrates: search → summarize → send email.
"""

import os
import sys
import logging
from datetime import datetime

from search import search_voice_ai_news
from summarize import summarize_results
from email_sender import send_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("voice-ai-weekly")


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"=== Voice AI Weekly Report: {date_str} ===")

    # Step 1: Search
    logger.info("Step 1/3: Searching for Voice AI news...")
    try:
        results = search_voice_ai_news()
    except Exception as e:
        logger.error(f"Search failed: {e}")
        sys.exit(1)

    if not results:
        logger.warning("No search results found. Exiting.")
        sys.exit(0)

    logger.info(f"Found {len(results)} unique results.")

    # Step 2: Summarize with Claude
    logger.info("Step 2/3: Summarizing with Claude API...")
    try:
        report_md = summarize_results(results)
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        sys.exit(1)

    # Save a local copy for debugging
    report_path = f"report_{date_str}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    logger.info(f"Report saved to {report_path}")

    # Step 3: Send email
    logger.info("Step 3/3: Sending email via Resend...")
    try:
        response = send_report(report_md, date_str)
        logger.info(f"Email sent: {response}")
    except Exception as e:
        logger.error(f"Email send failed: {e}")
        sys.exit(1)

    logger.info("=== Done ===")


if __name__ == "__main__":
    main()
