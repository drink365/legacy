# utils/pdf.py
from typing import Dict, Any, List
import io

def export_proposal_pdf(title: str, sections: List[Dict[str, str]]):
    """嘗試用 reportlab 產出 PDF；若無套件則回傳純文字檔案位元組。

    sections: [{"heading": str, "content": str}]
    回傳: (bytes, mime, filename)
"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        width, height = A4
        y = height - 2*cm
        c.setFont("Helvetica-Bold", 16)
        c.drawString(2*cm, y, title)
        y -= 1.2*cm
        for sec in sections:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2*cm, y, sec.get("heading",""))
            y -= 0.6*cm
            c.setFont("Helvetica", 10)
            text = c.beginText(2*cm, y)
            for line in sec.get("content","").splitlines():
                text.textLine(line)
            c.drawText(text)
            y = text.getY() - 0.8*cm
            if y < 2*cm:
                c.showPage()
                y = height - 2*cm
        c.showPage()
        c.save()
        packet.seek(0)
        return packet.read(), "application/pdf", "proposal.pdf"
    except Exception as e:
        # Fallback 純文字
        buf = io.StringIO()
        buf.write(title + "\n\n")
        for sec in sections:
            buf.write("# " + sec.get("heading","") + "\n")
            buf.write(sec.get("content","") + "\n\n")
        data = buf.getvalue().encode("utf-8")
        return data, "text/plain", "proposal.txt"
