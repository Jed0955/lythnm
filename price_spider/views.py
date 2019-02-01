import datetime, re
import logging
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from .models import Goods, Category, Unit, LatestRecord, Price

# Create your views here.
LOGGER = logging.getLogger('spider')
LIST_PAGE_URL_FORMAT = 'http://www.lythnm.com/anli/list_4_{0}.html'
DETAIL_PAGE_URL_FORMAT = 'http://www.lythnm.com{0}'

GOODS_DICT = {}
CATEGORY_DICT = {}
UNIT_DICT = {}
LATEST_RECORD = None

def spider_data():
    load_base_data()
    page = 1
    while True:
        page_url = LIST_PAGE_URL_FORMAT.format(page)
        try:
            page_html = request.urlopen(page_url).read()
        except HTTPError as ex:
            break
        else:
            detail_url_list = get_detail_url_list(page_html)
            for url in detail_url_list:
                detail_url = DETAIL_PAGE_URL_FORMAT.format(url)
                try:
                    LOGGER.info('************************************')
                    LOGGER.info(detail_url)
                    detail_html = request.urlopen(detail_url).read()
                except HTTPError as ex1:
                    LOGGER.error('获取数据失败：')
                    LOGGER.error(ex1)
                    pass
                else:
                    spider_price_data(detail_html)
            page += 1


def get_detail_url_list(html):
    detail_url_list = []
    html = html.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    item_list = soup.select('.news .news_list')
    for item in item_list:
        str_date = item.select_one('.riqi').text[3:13]
        date_date = parse_date(str_date)
        item_url = item.select_one('.news_listimg a')['href']
        detail_url_list.append(item_url)
    return detail_url_list


def spider_price_data(html):
    html = html.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    str_date = clean_blank(soup.select_one('.news_txt').text)[:10]
    date_date = parse_date(str_date)
    goods_price_list = []
    price_list = soup.select('.news_detailscontent table table tbody tr')
    for i in range(2, len(price_list)):
        items = price_list[i].select('td')
        goods_price = Price()
        if len(items) in (4, 5):
            price= clean_blank(items[-1].text)
            try:
                goods_name = clean_blank(items[-4].text)
                goods_price.goods = check_get_goods(goods_name)
                goods_price.category = check_get_category(clean_blank(items[-3].text))
                goods_price.unit = check_get_unit(clean_blank(items[-2].text))
                goods_price.price = float(price)
                goods_price.date = date_date
            except ValueError as ex:
                LOGGER.error('数据转换异常：' + goods_name + ' | ' + str(ex))
            else:
                goods_price_list.append(goods_price)
        else:
            LOGGER.error('数据格式未能识别')
    if goods_price_list:
        Price.objects.bulk_create(goods_price_list)
        LOGGER.info('抓取' + str_date + '数据共计' + str(len(goods_price_list)) + '条')
    else:
        LOGGER.error('未能抓取到数据')


# 清洗空白（\r、\n、\t和空格）
def clean_blank(html):
    clean_pattern = re.compile('[\r, \n, \t, ' ', ' ', \u3000]')
    return clean_pattern.sub('', html).strip()


# 日期转换
def parse_date(str_date):
    d_format = '%Y-%m-%d'
    return datetime.datetime.strptime(str_date, d_format).date()


# 加载基础数据，商品、商品类型、单位和最新记录日期
def load_base_data():
    goods_list = Goods.objects.all()
    global GOODS_DICT
    for goods in goods_list:
        GOODS_DICT[goods.name] = goods

    category_list = Category.objects.all()
    global CATEGORY_DICT
    for category in category_list:
        CATEGORY_DICT[category.name] = category

    unit_list = Unit.objects.all()
    global UNIT_DICT
    for unit in unit_list:
        UNIT_DICT[unit.name] = unit

    record_date = LatestRecord.objects.all()
    global LATEST_RECORD
    if record_date:
        LATEST_RECORD = record_date[0]


# 检查获取商品
def check_get_goods(goods_name):
    if goods_name:
        if goods_name not in GOODS_DICT:
            goods = Goods(name=goods_name)
            goods.save()
            GOODS_DICT[goods.name] = goods
        return GOODS_DICT[goods_name]
    else:
        return None


# 检查获取商品类型
def check_get_category(category_name):
    if category_name:
        if category_name not in CATEGORY_DICT:
            category = Category(name=category_name)
            category.save()
            CATEGORY_DICT[category.name] = category
        return CATEGORY_DICT[category_name]
    else:
        return None


# 检查获取单位
def check_get_unit(unit_name):
    if unit_name:
        if unit_name not in UNIT_DICT:
            unit = Unit(name=unit_name)
            unit.save()
            UNIT_DICT[unit.name] = unit
        return UNIT_DICT[unit_name]
    else:
        return None


# 检查更新最新记录日期
def check_update_record_date(current_record_date):
    global LATEST_RECORD
    if not LATEST_RECORD:
        LATEST_RECORD = LatestRecord(date=current_record_date)
        LATEST_RECORD.save()
    else:
        if LATEST_RECORD.date < current_record_date:
            LATEST_RECORD.date = current_record_date
            LATEST_RECORD.save()

