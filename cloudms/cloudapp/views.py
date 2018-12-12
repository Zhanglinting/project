from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse, FileResponse
import os
from django.views.decorators.http import require_http_methods
from django.template import Context, Template


# Create your views here
@require_http_methods(['GET', 'POST'])  # 此函数只处理post,get请求方式
def msg(request):
    datalist = []
    if request.method == 'POST':
        userA = request.POST.get('userA', None)
        userB = request.POST.get('userB', None)
        msg = request.POST.get('msg', None)
        time = datetime.now()
        with open('msg.txt', 'a+') as f:
            f.write('{}--{}--{}--{}--\n'.format(userB, userA, msg, time.strftime('%Y-%m&d %H:%M:%S')))
    if request.method == 'GET':
        userC = request.GET.get('userC', None)
        if userC != None:
            with open('msg.txt', 'r') as f:
                cnt = 0
                for line in f:
                    linedata = line.split('--')
                    if linedata[0] == userC:
                        cnt += 1
                        d = {'userA': linedata[1], 'msg': linedata[2], 'time': linedata[3]}
                        datalist.append(d)
                    if cnt >= 5:
                        break
    return render(request, 'msg.html', {'data': datalist})


def homeproc1(request):
    res = HttpResponse()
    res.write('<h1>这里是首页，具体功能请访问<a href="./msg">点击</a></h1>')
    return res
    # return HttpResponse('<h1>这里是首页，具体功能请访问<a href="./msg">这里</a></h1>')


def homeproc2(request):
    json = JsonResponse({'key': 'value'})
    return json


def download(request):
    # 图片下载
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    res = FileResponse(open(f'{cwd}/cloudapp/img/1.png', "rb"))
    res['Content-Type'] = 'application/octet-stream'
    res['Content-Disposition'] = 'attachment;filename=1.png'
    return res


def playground(request):
    template = Template('<h2>这一段{{name}}</h2>')
    ctx = Context({"name": "标题"})
    return HttpResponse(template.render(ctx))
