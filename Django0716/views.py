import random

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render

from Django0716.utils import search, CaptchaCheck


def hello(request):
    return HttpResponse("Hello World")


def hello_name(request, name):
    return HttpResponse("Hello %s" % name)


def hello_add(request, x, y):
    return HttpResponse("Hello %d + %d = %d" % (x, y, (x+y)))


def hello2_add(request):
    x = int(request.GET['x'])
    y = int(request.GET['y'])
    return HttpResponse("Hello2 %d + %d = %d" % (x, y, (x+y)))


def hello_template(request):
    return render(request, 'hello.html')


def hello_template_name(request, name):
    dict = {'name':name, 'age':20}
    return render(request, 'hello_name.html', dict)


def hello_template_users(request):
    dict = {}
    users = [
             {'name': 'vincent', 'age': 30},
             {'name': 'anita', 'age': 28},
             {'name': 'howard', 'age': 15},
             {'name': 'joanna', 'age': 10}
            ]
    dict['users'] = users
    return render(request, 'hello_users.html', dict)


def fruit_form(request):
    return render(request, 'fruit_form.html' )


def fruit_result(request):
    dict = {}
    dict.update({request.GET['fruit_name1']: request.GET['fruit_vote1']})
    dict.update({request.GET['fruit_name2']: request.GET['fruit_vote2']})
    dict.update({request.GET['fruit_name3']: request.GET['fruit_vote3']})
    return render(request, 'fruit_result.html', {'data': dict})


def youbike_form(request):
    dict = {}
    dict['lat'] = request.COOKIES['lat'] if 'lat' in request.COOKIES else 24.990205
    dict['lng'] = request.COOKIES['lng'] if 'lng' in request.COOKIES else 121.312054
    dict['dist'] = request.COOKIES['dist'] if 'dist' in request.COOKIES else 500
    dict['sbi'] = request.COOKIES['sbi'] if 'sbi' in request.COOKIES else 20
    dict['bemp'] = request.COOKIES['bemp'] if 'bemp' in request.COOKIES else 20
    return render(request, 'youbike_form.html', {'data': dict})


def youbike_result(request):
    lat = float(request.GET['lat'])
    lng = float(request.GET['lng'])
    dist = int(request.GET['dist'])
    sbi = int(request.GET['sbi'])
    bemp = int(request.GET['bemp'])

    dict = search(lat, lng, dist, sbi, bemp)
    response = render(request, 'youbike_result.html', {'data': dict})
    # 存入 cookies
    response.set_cookie('lat', lat)
    response.set_cookie('lng', lng)
    response.set_cookie('dist', dist)
    response.set_cookie('sbi', sbi)
    response.set_cookie('bemp', bemp)
    # 存入 sesson
    request.session['youbike_dict'] = dict
    return response


def map(request):
    # 取得 sesson
    dict = request.session['youbike_dict']
    return render(request, 'map.html', {'data': dict})


def login_form(request):
    dict = {}
    dict['email'] = request.COOKIES['email'] if 'email' in request.COOKIES else ''
    dict['password'] = request.COOKIES['password'] if 'password' in request.COOKIES else ''
    dict['remember'] = 'checked' if 'remember' in request.COOKIES else ''
    return render(request, 'login_form.html', {'data': dict})


def login_result(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    remember = request.POST.get('remember', False)
    response = HttpResponse("Hello " + email + ", " + password + ", " + str(remember))
    # 將資料存進 cookie
    if remember:
        response.set_cookie('email', email)
        response.set_cookie('password', password)
        response.set_cookie('remember', remember)
    else:
        response.delete_cookie('email')
        response.delete_cookie('password')
        response.delete_cookie('remember')
    return response


def macdonald_form(request):
    try:
        email = request.session['email']
        return render(request, 'macdonald_form.html', locals())
    except:
        #return render(request, 'login_session.html')
        return get_login_session_html(request)


def macdonald_result(request):
    try:
        email = request.session['email']
    except:
        #return render(request, 'login_session.html')
        return get_login_session_html(request)

    if request.method == 'POST':  # POST
        # 取得表單資料
        product = request.POST.get('product', '')
        amount = request.POST.get('amount', 0)

        # 組合 dict 資料
        obj = {'product': product, 'amount': amount}

        # 是否有名為 saved 的 session 資料 ?
        if not 'saved' in request.session or not request.session['saved']:
            request.session['saved'] = [obj]
        else:
            saved_list = request.session['saved']  # 取得 session list 資料
            saved_list.append(obj)  # 加入元素
            request.session['saved'] = saved_list  # 回存到 session 中

        return render(request, 'macdonald_result.html', {'data': request.session['saved']})
        # return HttpResponse('macdonald_result POST, ' + str(request.session['saved']))
    else:  # GET
        # 是否有名為 saved 的 session 資料 ?
        if not 'saved' in request.session or not request.session['saved']:
            return render(request, 'macdonald_result.html')
            #return HttpResponse('macdonald_result GET empty !')
        else:
            return render(request, 'macdonald_result.html', {'data': request.session['saved']})
            #return HttpResponse('macdonald_result GET, ' + str(request.session['saved']))


def macdonald_clear(request):
    try:
        del request.session['saved']
        return HttpResponse('清除完畢 !')
    except: # 例外處理
        return HttpResponse('沒有東西可以清 !')


def login_session(request):
    #return render(request, 'login_session.html')
    return get_login_session_html(request)


def login_session_check(request):
    # 取得表單資料
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    if email == 'admin@gmail.com' and password == '1234':
        request.session['email'] = email
        response = render(request, 'macdonald_form.html', locals())
        # 將資料存進 cookie
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        remember = request.POST.get('remember', False)
        if remember:
            response.set_cookie('email', email)
            response.set_cookie('password', password)
            response.set_cookie('remember', remember)
        else:
            response.delete_cookie('email')
            response.delete_cookie('password')
            response.delete_cookie('remember')
        return response
    else:
        return HttpResponse('login error !')


def login_session_out(request):
    request.session.clear()
    return get_login_session_html(request)

def get_login_session_html(request):
    dict = {}
    dict['email'] = request.COOKIES['email'] if 'email' in request.COOKIES else ''
    dict['password'] = request.COOKIES['password'] if 'password' in request.COOKIES else ''
    dict['remember'] = 'checked' if 'remember' in request.COOKIES else ''
    return render(request, 'login_session.html', {'data': dict})


def ajax_lotto_form(request):
    return render(request, 'ajax_lotto_form.html')


def ajax_lotto_result(request):
    lotto = set()
    while len(lotto) < 6:
        lotto.add(random.randint(0, 49))
    return HttpResponse(str(lotto))


def ajax_rating_form(request):
    return render(request, 'ajax_rating_form.html')


def ajax_rating_result(request):
    return HttpResponse("ajax_rating_result")


def user_login_form(request):
    # Cookies
    username = request.COOKIES['username'] if 'username' in request.COOKIES else ''
    password = request.COOKIES['password'] if 'password' in request.COOKIES else ''
    remember = request.COOKIES['remember'] if 'remember' in request.COOKIES else ''

    # 圖片驗證碼
    # hashkey 驗證碼生成的祕鑰
    hashkey = CaptchaStore.generate_key()
    # image_url驗證碼的圖片地址
    image_url = captcha_image_url(hashkey)
    response = render(request, 'user_login_form.html', locals())
    return response


# 登入後台
def user_login(request):
    # 取得驗證碼
    captchaCheck = CaptchaCheck(request.POST)
    # 驗證驗證碼
    if captchaCheck.is_valid():
        # 取得使用者(帳號、密碼)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 驗證使用者(帳號、密碼)
        user = auth.authenticate(username=username, password=password)
        # 確認使用者
        if user is not None and user.is_active:
            # 進行登入並存入session 物件
            auth.login(request, user)
            response = HttpResponse("登入 success " + str(user))

            # Cookies
            remember = request.POST.get('remember', False)
            if remember:
                response.set_cookie('username', username)
                response.set_cookie('password', password)
                response.set_cookie('remember', 'checked')
            else:
                response.delete_cookie('username')
                response.delete_cookie('password')
                response.delete_cookie('remember')
            return response
        else:
            return HttpResponse("登入 error")
    else:
        return HttpResponse("驗證碼錯誤 error")


def user_logout(request):
    auth.logout(request)
    return HttpResponse('登出_logout')


def user_crud_form(request):
    flag = request.user.is_authenticated
    if flag:
        return render(request, 'user_crud_form.html')
    else:
        return HttpResponse('登入逾時/尚未登入~')

