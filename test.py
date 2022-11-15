import os
import requests
from bs4 import BeautifulSoup as bs
import json
import sys

os.system('cls')
_s = requests.Session()

def _post(url, header, payload):
    return _s.post(url, headers=header, json=payload)

def _JSON(x):
    return json.dumps(json.loads(x), indent=3)

def _LOAD(x):
    return json.loads(x)

_url = 'https://icv.boq.ph/'

_payload = {
    'username': 'hevoc66222@kixotic.com',
    'password': 'boqSample123.'
}

_res = _s.get(_url)
soup = bs(_res.content, 'html.parser')

_token = soup.find('meta', {'name' : 'csrf-token'}).get('content')
try:
    _login = 'https://icv.boq.ph/login/authenticate?_token={}'.format(_token)
except Exception as e:
    print(e)

_account_isValid = _s.post(_login, json=_payload)

if _account_isValid.json()['response']:
    # print('Account Verified!')
    pass
else:
    print('Account not found!')
    sys.exit(0)

header = {
    'referer': 'https://icv.boq.ph/account/services?listType=2',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36 Edg/107.0.1418.35',
    'x-csrf-token': _token
}

_branches = {
    1: 'BOQ-MOA',
    2: 'BOQ-ROBINSONS-MANILA',
    3: 'BOQ-RESORTS-WORLD-MANILA',
    # 4: 'BOQ-MANILA',
    5: 'BOQ-SM-NORTH',
    6: 'BOQ-EASTWOOD',
    7: 'BOQ-MCKINLEY',
    8: 'BOQ-AYALA-FAIRVIEW'
}

for i in _branches.keys():

    _branch_payload = {
        'branch_code': _branches[i],
        'item_code': 'CVC2019'
    }
    _dates = _s.post('https://icv.boq.ph/account/appointment/earliest', headers=header, json=_branch_payload)


    _branchID = _LOAD(_dates.content)['data']['branch']
    _Available = json.loads(_dates.content)['data']['date_format']

    if not _Available:
        print('No available date')
        sys.exit(0)
    else:
        print('Available date found!')

    pickDate = {
        'itemCode': 'CVC2019',
        'date': json.loads(_dates.content)['data']['date_format']+'T00:00'
    }

    _pickDate = _s.post('https://icv.boq.ph/account/appointment/pickDateSlots', headers=header, json=pickDate)

    soup = bs(_pickDate.content, 'html.parser')
    _getTimeSlot = soup.find('ul').find_all('input')

    timeslot = ''

    if len(_getTimeSlot) > 1:
        timeslot = _getTimeSlot[1].get('value')
    elif len(_getTimeSlot) == 1:
        timeslot = _getTimeSlot[0].get('value')
    else:
        print('no valid time timeslot')
    # print(_getTimeSlot)
    _timeslot = timeslot.translate({ ord(c): None for c in '"\_' })

    _verify_date = {
        'branch': _branchID,
        'timeSlot': _timeslot 
    }

    _timeslot_isValid = _s.post('https://icv.boq.ph/account/appointment/pickTimeSlotCheck', headers=header, json=_verify_date)
    print(_LOAD(_timeslot_isValid.text).get('msg'),"on", json.loads(_dates.content)['data']['date'] + " " + _branches.get(i))
    print('-------------------------------------------------')

# _createPayload = {
#     'branch_id': _branchID,
#     'appointment_type': 'APPOINTMENT',
#     'time_slot_id': _timeslot,
#     'item': 'Certification of Vaccine for COVID 19',
#     'item_code': 'CVC2019'
# }

# _create = _post('https://icv.boq.ph/account/appointmentlist/create', header, _createPayload)
# # print(_create.text)


# _regionPayload = {
#     'region_code': '13', #NCR default
# }
# _getProvinces = _post('https://icv.boq.ph/account/services/getprovinces', header, _regionPayload)

# # print(_JSON(_getProvinces.text))

# key = 'NCR, FOURTH DISTRICT'
# _provincePayload = None

# match key:
#     case 'MANILA':
#         {'province_code':'1339'}
#     case 'NCR, FIRST DISTRICT':
#         _provincePayload = {'province_code':'1339'}
#     case 'NCR, SECOND DISTRICT':
#         _provincePayload = {'province_code':'1374'}
#     case 'NCR, THIRD DISTRICT':
#         _provincePayload = {'province_code':'1375'}
#     case 'NCR, FOURTH DISTRICT':
#         _provincePayload = {'province_code':'1376'}

# _getCity = _post('https://icv.boq.ph/account/services/getcitymunic', header, _provincePayload)
# print(_JSON(_getCity.text))
