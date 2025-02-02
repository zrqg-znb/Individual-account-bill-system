from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch


def generate_pdf(export_info, output_filename):
    # 注册自定义字体
    pdfmetrics.registerFont(TTFont('CustomFont', 'app/utils/Arial.ttf'))

    # 创建横版文档
    doc = SimpleDocTemplate(output_filename, pagesize=landscape(A4), encoding='utf-8')

    # 创建样式
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomTitle',
                              fontName='CustomFont',
                              fontSize=16,
                              leading=20,
                              spaceAfter=12))
    styles.add(ParagraphStyle(name='CustomBody',
                              fontName='CustomFont',
                              fontSize=10,
                              leading=12,
                              spaceAfter=6))

    content = []

    # 客户信息
    content.append(Paragraph("客户信息", styles['CustomTitle']))
    customer_info = [
        f"姓名：{export_info['owner_name']}",
        f"电话：{export_info['owner_phone']}",
        f"邮箱：{export_info['owner_email']}",
        f"别名：{export_info['owner_alias']}",
        f"地址：{export_info['owner_dept']}",
    ]
    for info in customer_info:
        content.append(Paragraph(info, styles['CustomBody']))

    # 添加一些空间
    content.append(Spacer(1, 0.2 * inch))

    # 账单信息
    content.append(Paragraph("账单信息", styles['CustomTitle']))
    bill_info = [
        f"状态：{export_info['status']}",
        f"总金额：{export_info['total_amount']}",
        f"已付金额：{export_info['paid_amount']}",
        f"创建时间：{export_info['created_at']}",
        f"导出时间：{export_info['export_time']}"
    ]
    for info in bill_info:
        content.append(Paragraph(info, styles['CustomBody']))

    # 添加一些空间
    content.append(Spacer(1, 0.2 * inch))

    # 商品信息
    content.append(Paragraph("商品信息", styles['CustomTitle']))

    # 准备表格数据
    table_data = [
        ['名称', '单价', '数量', '单位', '购买时间', '结算时间', '购买人', '状态', '支付方式', '结算人', '金额',
         '已付金额', '备注']
    ]
    for item in export_info['items']:
        table_data.append([
            item['product_name'],
            item['price'],
            item['quantity'],
            item['unit'],
            item['purchase_time'],
            item['settle_time'],
            item['buyer_name'],
            item['status'],
            item['payment_method'],
            item['settler_name'],
            item['amount'],
            item['paid_amount'],
            item['remark']
        ])

    # 创建表格
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'CustomFont'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 减小字体大小以适应更多内容
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # 表头上方的线
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        # 表头下方的线
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        # 表格最后一行下方的线
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        # 设置表头行的背景色（可选）
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        # 设置表头的字体样式（可选）
        ('FONTNAME', (0, 0), (-1, 0), 'CustomFont'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        # 设置行高
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))

    content.append(table)

    # 构建PDF
    doc.build(content)
