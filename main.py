from operator import ge
from requests_html import HTMLSession
import json, sys

def get(ip):
    return HTMLSession().get('https://ipinfo.io/{}'.format(ip), headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"})

ip = sys.argv[1] if len(sys.argv) > 1 else input('Enter ip: ')
html = get(ip)
try:
    summary_data = html.html.find('.table.table-striped.table-borderless.table-sm.two-column-table.mb-0', first=True).text.split('\n')
    summary = dict(zip(summary_data[::2], summary_data[1::2]))
except:
    summary = {}
try:
    geo_data = html.html.find('.table.table-borderless.table-xs.geo-table', first=True).text.split('\n')
    try:
        int(geo_data[geo_data.index('Postal') + 1])
    except:
        geo_data.remove('Postal')
    geo = dict(zip(geo_data[::2], geo_data[1::2]))
except:
    geo = {}
try:
    privacy = {}
    for i in html.html.find('.col-lg-3.d-flex.align-items-center.mt-2'):
        privacy[i.text] = 'False' if 'wrong-big.svg' in i.xpath('//img')[0].attrs['src'] else 'True'
except:
    privacy = {}
try:
    asn_data = html.html.find('#block-asn')[0].text.split('\n')
    asn = dict(zip(asn_data[:8:2], asn_data[1:8:2]))
except:
    asn = {}
try:
    hosted = html.html.find('.row.border.my-3.mx-1', first=True).text.split('\n')
except:
    hosted = []
print(json.dumps({"summary":summary, "geo":geo, "privacy":privacy, "asn":asn, "hosted":hosted}, indent=4))
