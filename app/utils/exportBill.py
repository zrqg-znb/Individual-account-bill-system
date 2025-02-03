import os
import re
import oss2
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from datetime import datetime

# 阿里云OSS配置
OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
OSS_ACCESS_KEY_ID = 'LTAI5tPhNDpozr7h8HN2RQhb'
OSS_ACCESS_KEY_SECRET = '27EePBSxtwGkTIhe3G3CishirtEDVq'
OSS_BUCKET_NAME = 'individual-bill-system'


def upload_to_oss(file_path, object_name):
    # 创建Bucket实例
    auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)
    # 上传文件
    bucket.put_object_from_file(object_name, file_path)

    # 返回文件的URL
    return f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{object_name}"


def parse_time(time_str):
    if re.search(r'\.\d+', time_str):
        return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    else:
        return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S%z')


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
        f"用户名：{export_info['owner_name']}",
        f"电话：{export_info['owner_phone']}",
        f"邮箱：{export_info['owner_email']}",
        f"姓名：{export_info['owner_alias']}",
        f"地址：{export_info['owner_dept']}",
    ]
    for info in customer_info:
        content.append(Paragraph(info, styles['CustomBody']))

    # 添加一些空间
    content.append(Spacer(1, 0.2 * inch))

    # 账单信息
    content.append(Paragraph("账单信息", styles['CustomTitle']))

    export_info['created_at'] = datetime.strptime(export_info['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
    bill_info = [
        f"状态：{'已支付' if export_info['status'] == 'paid' else '未支付'}",
        f"总金额：{export_info['total_amount']}",
        f"已付金额：{export_info['paid_amount']}",
        f"创建时间：{export_info['created_at'].strftime('%Y-%m-%d %H:%M:%S')}",
        f"导出时间：{export_info['export_time'].strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    for info in bill_info:
        content.append(Paragraph(info, styles['CustomBody']))

    # 添加一些空间
    content.append(Spacer(1, 0.2 * inch))

    # 商品信息
    content.append(Paragraph("商品信息", styles['CustomTitle']))

    # 准备表格数据
    table_data = [
        ['名称', '单价', '数量', '单位', '购买时间', '购买人', '状态', '支付方式', '金额',
         '已付金额', '结算时间', '结算人', '备注']
    ]
    for item in export_info['items']:
        if item['status'] == 'unpaid':
            status = '未结算'
        else:
            if item['status'] == 'paid':
                status = '已结算'
            else:
                status = '已退款'
        if item['payment_method'] == 'cash':
            payment_method = '现金'
        else:
            if item['payment_method'] == 'credit':
                payment_method = '记账'
            else:
                if item['payment_method'] == 'alipay':
                    payment_method = '支付宝'
                else:
                    payment_method = '微信'

        item['purchase_time'] = parse_time(item['purchase_time'])
        settle_time = '---'
        if item['settle_time']:
            settle_time = parse_time(item['settle_time']).strftime('%Y-%m-%d %H:%M:%S')
        table_data.append([
            item['product_name'],
            item['price'],
            item['quantity'],
            item['unit'],
            item['purchase_time'].strftime('%Y-%m-%d %H:%M:%S'),
            item['buyer_name'],
            status,
            payment_method,
            item['amount'],
            item['paid_amount'],
            settle_time,
            item['settler_name'],
            item['remark'],
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

    object_name = os.path.basename(output_filename)
    pdf_url = upload_to_oss(output_filename, object_name)

    # 删除本地PDF文件
    os.remove(output_filename)

    return pdf_url
