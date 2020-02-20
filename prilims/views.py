import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from random import randint
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from prilims.models import Questions, ScoreCard, TimeStats


def index(request):
    return redirect('/home')

@csrf_exempt
@login_required
def home(request):
    total_questions = 10
    if request.user_agent.os.family == 'Android':
        return HttpResponse("Mobile Version of site is not available")

    if request.method == 'POST':
        random_list = []
        count = 0
        details = []

        obj_id = []
        obj = Questions.objects.all()
        c = obj.count()
        for item in obj:
            obj_id.append(item.id)

        print(obj_id)
        print (c)
        while count<total_questions:

            random_num = randint(1,c)
            print(random_num)
            if random_num not in random_list:

                try:
                    print(count)
                    obj = Questions.objects.get(id = obj_id[random_num-1] )
                    dic = {}
                    dic['id'] = obj_id[random_num-1]
                    dic['question'] = obj.question
                    dic['choice1'] = obj.choice1
                    dic['choice2'] = obj.choice2
                    dic['choice3'] = obj.choice3
                    dic['choice4'] = obj.choice4
                    dic['correct_answer'] = obj.correct_answer
                    details.append(dic)
                    random_list.append(random_num)
                    count += 1
                    # print(dic)

                except:
                    pass

        # user_obj  = User.objects.get(username = request.user)
        #
        # date_obj = TimeStats.objects.filter(user = user_obj)
        # if date_obj:
        #     date_obj = date_obj.first()
        #     print(date_obj.time)
        #     print(datetime.datetime.now())
        #     datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        #     # date1 = datetime.datetime.strftime(datetime.datetime.now() ,datetimeFormat)
        #     # date2 = datetime.datetime.strftime(date_obj.time , datetimeFormat)
        #     time = datetime.datetime.strptime(str(datetime.datetime.now()) ,datetimeFormat) \
        #            - datetime.datetime.strptime(str(date_obj.time).split('+')[0] , datetimeFormat)
        #     time = 30 * 60 * 1000 - time.seconds
        # else:
        #     date_obj = TimeStats.objects.create(user = user_obj , time = datetime.datetime.now(),status=True)
        #     time = 30 * 60 * 1000
        # print(time)
        return JsonResponse({ 'data' : details})



    return render( request , 'home.html' , {})


@csrf_exempt
def login_fn ( request ):


    if request.user_agent.os.family == 'Android':
        return HttpResponse("Mobile Version of site is not available")

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)
        print(password)

        done_users = ScoreCard.objects.all()
        done_usernames = [str(x.username) for x in list(done_users)]

        print(done_usernames)

        if username in done_usernames:
            return JsonResponse({'status': '300'})

        u = authenticate( username = username , password = password )
        if u:

            login( request , u)
            return JsonResponse({'status': '200'})
        else:
            return JsonResponse({'status': '400'})

    else:

        return render(request , 'login.html')





def validate_username(request):


    print("sdfsdfsdf")
    print('sdfsd')
    response = {}
    username = request.GET.get('username')
    all_users = User.objects.all()
    usernames = [str(x.username) for x in list(all_users)]






    if username in usernames:
        response['status']= '200'
        response['text']= 'username exists'
    else:
        response['status'] = '400'

    return JsonResponse(response)


@csrf_exempt
def score_calculate(request):


    answer_list = (request.POST.getlist('data[]'))
    score = 0

    for i in answer_list:

        l = i.split(',')
        try:
            obj = Questions.objects.get(id = l[0])
            if ( l[1] == obj.correct_answer ):
                print(l[1] , obj.correct_answer)
                score+=1

        except:
            pass

    userobj = User.objects.get(pk = request.user.id)
    u = ScoreCard.objects.create( username = userobj,score = score )
    u.save()
    logout(request)
    return JsonResponse({'status': '200'})

