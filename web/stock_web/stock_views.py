from django.http import HttpResponse
from django.shortcuts import redirect, render
from . import mission_manager
from . import label_data_manager
from dateutil.parser import parse
import datetime


def home(request):
    ctx = dict()
    menu_dict = dict()
    menu_dict['task info'] = 'www.baidu.com'
    menu_dict['label data'] = 'www.163.com'
    menu_dict['update data'] = 'www.sina.com'
    ctx['menu_dict'] = menu_dict
    return render(request, 'home.html', ctx)

def show_last_image(request):
    ctx = dict()
    ctx['last_png_name'] = mission_manager.get_last_completed_image()
    return render(request, 'image_view.html', ctx)

def stop_cur_mission(request):
    #mission_manager.stop_cur_mission()
    ctx = dict()
    ctx['result_message'] = 'The current mission is killed'
    ctx['flush_home'] = 'window.location.href = document.referrer;'
    return render(request, 'submit_result.html', ctx)

def add_data(request):
    ctx = dict()
    return render(request, 'add_data.html', ctx)

def add_label_line(request):
    ctx = dict()
    ctx['flush_home'] = ''
    if 'trust_code' in request.GET and request.GET['trust_code']:
        trust_code = request.GET['trust_code']
        if trust_code != 'stock':
            ctx['result_message'] = '"trust code" is err'
            return render(request, 'submit_result.html', ctx)
    else:
        ctx['result_message'] = 'Please input "trust code"'
        return render(request, 'submit_result.html', ctx)

    fields = ['date', 'end', 'high', 'low', 'volume', 'amount']
    submit_data = dict()
    if 'date' in request.GET and request.GET['date']:
        submit_data['date'] = request.GET['date']
    if 'end' in request.GET and request.GET['end']:
        submit_data['end'] = request.GET['end']
    if 'high' in request.GET and request.GET['high']:
        submit_data['high'] = request.GET['high']
    if 'low' in request.GET and request.GET['low']:
        submit_data['low'] = request.GET['low']
    if 'volume' in request.GET and request.GET['volume']:
        submit_data['volume'] = request.GET['volume']
    if 'amount' in request.GET and request.GET['amount']:
        submit_data['amount'] = request.GET['amount']

    
    for item in fields:
        if item not in submit_data.keys():
            ctx['result_message'] = 'please input field "%s"' % item
            return render(request, 'add_data_result.html', ctx)

    label_data_manager.add_new_line(submit_data) 
    
    ctx['result_message'] = 'Update label data success!'
    ctx['flush_home'] = 'window.location.href = document.referrer;'
    return render(request, 'add_data_result.html', ctx)

def mission(request):
    ctx = dict()
    ctx['status_message'] = 'hello world'
    last_index, last_date = label_data_manager.get_last_date()
    ctx['last_label_date'] = last_date
    status = mission_manager.has_running_mission()
    ctx['last_mission'] = mission_manager.get_last_completed_mission()
    if status is None:
        ctx['status_message'] = 'has no running mission'
    else:
        if len(status) > 2:
            ctx['status_message'] = '%s mission is traing, current N is %s, epoch is %s' % (status[2], status[1], status[3])
        else:
            ctx['status_message'] = '%s mission is predicting' % status[1]
    return render(request, 'mission.html', ctx)

def test(request):
    return render(request, 'test.html', None)

def submit(request):
    ctx = dict()
    ctx['flush_home'] = ''
    if 'trust_code' in request.GET and request.GET['trust_code']:
        trust_code = request.GET['trust_code']
        if trust_code != 'stock':
            ctx['result_message'] = '"trust code" is err'
            return render(request, 'submit_result.html', ctx)
    else:
        ctx['result_message'] = 'Please input "trust code"'
        return render(request, 'submit_result.html', ctx)

    mission_manager.stop_cur_mission()
    mission_date_info = None
    if 'date' in request.GET and request.GET['date']:
        mission_date_info = request.GET['date']
    else:
        ctx['result_message'] = 'Please input "Mission Date"'
    last_label_index, last_label_date = label_data_manager.get_last_date()
    last_date = parse(last_label_date)
    mission_date = parse(mission_date_info)
    diff = mission_date - last_date
    if diff.days > 0:
        ctx['result_message'] = 'Error: Mission Date is later than label date!'
    else:
        if mission_manager.start_mission(mission_date_info.replace('-','/')) is True:
            ctx['result_message'] = 'OK: Start Mission %s Success' % mission_date_info
        else:
            ctx['result_message'] = 'Error: Start Mission %s Failed' % mission_date_info
    return render(request, 'submit_result.html', ctx)
