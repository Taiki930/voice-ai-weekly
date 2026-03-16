"""
Email sender module using Resend API.
"""

import os
import logging
import markdown
import resend

logger = logging.getLogger(__name__)

EMAIL_FROM = "Voice AI Weekly <weekly@vocust.com>"
EMAIL_TO = "nhwang@vocust.com"


def _render_html(md_content: str, date_str: str) -> str:
    """Render Markdown report into styled HTML email."""
    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code"],
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:0; background-color:#f4f4f7; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f7; padding:32px 0;">
<tr><td align="center">
<table width="640" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.06);">

<!-- Header -->
<tr>
<td style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%); padding:32px 40px; text-align:center;">
  <h1 style="color:#ffffff; margin:0; font-size:24px; font-weight:600; letter-spacing:1px;">
    Voice AI Weekly
  </h1>
  <p style="color:#a0aec0; margin:8px 0 0; font-size:14px;">
    语音AI行业周报 | {date_str}
  </p>
</td>
</tr>

<!-- Body -->
<tr>
<td style="padding:32px 40px; color:#2d3748; font-size:15px; line-height:1.8;">
{html_body}
</td>
</tr>

<!-- Footer -->
<tr>
<td style="background-color:#f7fafc; padding:20px 40px; text-align:center; border-top:1px solid #e2e8f0;">
  <p style="color:#a0aec0; font-size:12px; margin:0;">
    此邮件由自动化系统生成 | Powered by Firecrawl + Claude + Resend
  </p>
</td>
</tr>

</table>
</td></tr>
</table>
</body>
</html>"""


def send_report(
    md_content: str,
    date_str: str,
    api_key: str | None = None,
    to_email: str | None = None,
    from_email: str | None = None,
) -> dict:
    """
    Send the weekly report via Resend.

    Args:
        md_content: Markdown formatted report.
        date_str: Date string for subject line (e.g. "2026-03-16").
        api_key: Resend API key.
        to_email: Recipient email address.
        from_email: Sender email address.

    Returns:
        Resend API response dict.
    """
    api_key = api_key or os.environ.get("RESEND_API_KEY", "")
    if not api_key:
        raise ValueError("RESEND_API_KEY is required")

    resend.api_key = api_key

    to = to_email or os.environ.get("REPORT_TO_EMAIL", EMAIL_TO)
    sender = from_email or os.environ.get("REPORT_FROM_EMAIL", EMAIL_FROM)
    subject = f"语音AI行业周报 | {date_str}"
    html = _render_html(md_content, date_str)

    logger.info(f"Sending report to {to}...")
    params = resend.Emails.SendParams(
        from_=sender,
        to=[to],
        subject=subject,
        html=html,
    )
    response = resend.Emails.send(params)
    logger.info(f"Email sent successfully: {response}")
    return response


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_md = "# Test\n\nThis is a test report."
    print(_render_html(test_md, "2026-03-16"))
