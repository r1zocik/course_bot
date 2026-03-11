import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def generate_receipt_pdf(
    user_name: str,
    amount: float,
    from_cur: str,
    to_cur: str,
    result: float,
    rate: float,
    source: str = "ЦБ Узбекистана"
) -> bytes:
    """
    Генерирует PDF чек конвертации и возвращает байты.
    """
    buffer = io.BytesIO()
    w, h = A4
    c = canvas.Canvas(buffer, pagesize=A4)

    CURRENCY_SYMBOLS = {
        "UZS": "so'm",
        "USD": "$",
        "RUB": "₽",
        "EUR": "€",
    }

    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    time_str = now.strftime("%H:%M:%S")
    receipt_id = now.strftime("%Y%m%d%H%M%S")

    # Фон шапки
    c.setFillColor(colors.HexColor("#1a73e8"))
    c.rect(0, h - 80*mm, w, 80*mm, fill=1, stroke=0)

    # Заголовок
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(w / 2, h - 25*mm, "UzRate Bot")
    c.setFont("Helvetica", 12)
    c.drawCentredString(w / 2, h - 35*mm, "Чек конвертации валюты")

    # Логотип иконка
    c.setFont("Helvetica", 28)
    c.drawCentredString(w / 2, h - 58*mm, "💱")

    # Белый блок
    margin = 20*mm
    box_y = h - 200*mm
    box_h = 130*mm
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#e0e0e0"))
    c.roundRect(margin, box_y, w - 2*margin, box_h, 5*mm, fill=1, stroke=1)

    # Содержимое чека
    def draw_row(label, value, y, bold_value=False):
        c.setFillColor(colors.HexColor("#666666"))
        c.setFont("Helvetica", 10)
        c.drawString(margin + 8*mm, y, label)
        c.setFillColor(colors.HexColor("#111111"))
        if bold_value:
            c.setFont("Helvetica-Bold", 11)
        else:
            c.setFont("Helvetica", 10)
        c.drawRightString(w - margin - 8*mm, y, value)

    def draw_divider(y):
        c.setStrokeColor(colors.HexColor("#eeeeee"))
        c.line(margin + 5*mm, y, w - margin - 5*mm, y)

    row_y = box_y + box_h - 15*mm
    step = 13*mm

    draw_row("Номер чека:", f"#{receipt_id}", row_y)
    draw_divider(row_y - 3*mm)
    row_y -= step

    draw_row("Дата:", date_str, row_y)
    draw_divider(row_y - 3*mm)
    row_y -= step

    draw_row("Время:", time_str, row_y)
    draw_divider(row_y - 3*mm)
    row_y -= step

    draw_row("Клиент:", user_name, row_y)
    draw_divider(row_y - 3*mm)
    row_y -= step

    sym_from = CURRENCY_SYMBOLS.get(from_cur, from_cur)
    draw_row("Исходная сумма:", f"{amount:,.2f} {from_cur} ({sym_from})", row_y)
    draw_divider(row_y - 3*mm)
    row_y -= step

    sym_to = CURRENCY_SYMBOLS.get(to_cur, to_cur)
    draw_row("Результат:", f"{result:,.2f} {to_cur} ({sym_to})", row_y, bold_value=True)
    draw_divider(row_y - 3*mm)
    row_y -= step

    draw_row("Курс:", f"1 {from_cur} = {rate:,.4f} {to_cur}", row_y)
    draw_divider(row_y - 3*mm)
    row_y -= step

    draw_row("Источник курса:", source, row_y)

    # Большая сумма результата
    result_y = box_y - 25*mm
    c.setFillColor(colors.HexColor("#1a73e8"))
    c.roundRect(margin, result_y - 10*mm, w - 2*margin, 22*mm, 4*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(
        w / 2, result_y,
        f"{amount:,.2f} {from_cur}  →  {result:,.2f} {to_cur}"
    )

    # Подвал
    footer_y = 20*mm
    c.setFillColor(colors.HexColor("#999999"))
    c.setFont("Helvetica", 8)
    c.drawCentredString(w / 2, footer_y + 6*mm, "Этот чек сформирован автоматически ботом UzRate")
    c.drawCentredString(w / 2, footer_y, "Курсы предоставлены ЦБ Узбекистана • t.me/ecogorod01_bot")

    c.save()
    buffer.seek(0)
    return buffer.read()
