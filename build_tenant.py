__author__ = 'apple'
import json, mini_rest, logging

APIC_TOKEN = None
CONTROLLER = 'https://x.x.x.x'
CERT = './cert.pem'

logging.basicConfig(
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

def _build_everything(url=None, jsonfile=None):
    fp = open(jsonfile, 'r')
    body = json.load(fp)
    fp.close()

    a = mini_rest.rest_it()
    a.Controller = CONTROLLER
    a.URI = url
    a.Action = 'POST'
    a.Body = body
    a.APIC_Token = APIC_TOKEN
    a.SCert = CERT
    return a.rest_run()

def main():
    'Initate APIC Token and conduct following operations'
    global APIC_TOKEN
    a=mini_rest.rest_it()
    a.init_conf(conf=[
        CONTROLLER,
        '/api/aaaLogin.json',
        'POST',
        {"aaaUser" : {"attributes" : {"name" : "xxx","pwd" : "xxxxx"}}},
        CERT
    ])
    result = a.rest_run()
    APIC_TOKEN = result['imdata'][0]['aaaLogin']['attributes']['token']

    'Create Tenant'
    _build_everything(url='/api/mo/uni.json', jsonfile='./json/tenant.json')
    logging.warning('Tenant Created')

    'Create 2 BDs'
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/BD-BD1.json', jsonfile='./json/bd1.json')
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/BD-BD2.json', jsonfile='./json/bd2.json')
    logging.warning('BDs Created')

    'Create AP'
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/ap-WebApplicationProfile.json', jsonfile='./json/apf.json')
    logging.warning('ApplicationProfile Created')

    'Create 3 EPGs with proper phy and vmm domains'
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/ap-WebApplicationProfile/epg-Web.json', jsonfile='./json/epgweb.json')
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/ap-WebApplicationProfile/epg-App.json', jsonfile='./json/epgapp.json')
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/ap-WebApplicationProfile/epg-DB.json', jsonfile='./json/epgdb.json')
    logging.warning('EPGs Created with physical/vmm domain assigned')

    'Create 2 filters'
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/flt-sql_ft.json', jsonfile='./json/ftsql.json')
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/flt-app_ft.json', jsonfile='./json/ftapp.json')
    logging.warning('Filters Created')

    'Create 2 contract and assign filters accordingly'
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/brc-SQLCtrct.json', jsonfile='./json/ctrctsql.json')
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/brc-AppCtrct.json', jsonfile='./json/ctrctapp.json')
    logging.warning('Contracts Created')

    'Assign Contracts to EPGs'
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/ap-WebApplicationProfile/epg-App.json', jsonfile='./json/appctrctprov.json')
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/ap-WebApplicationProfile/epg-Web.json', jsonfile='./json/appctrctcons.json')
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/ap-WebApplicationProfile/epg-App.json', jsonfile='./json/sqlctrctcons.json')
    _build_everything(url='/api/node/mo/uni/tn-Test-Corp/ap-WebApplicationProfile/epg-DB.json', jsonfile='./json/sqlctrctprov.json')
    logging.warning('Contacts assigned to EPGs')


if __name__ == "__main__":
    main()
