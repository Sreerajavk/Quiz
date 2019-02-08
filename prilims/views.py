from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from random import randint
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from prilims.models import Questions , ScoreCard


def index(request):
    return redirect('/home')

@csrf_exempt
@login_required
def home(request):


    if request.user_agent.os.family == 'Android':

        return HttpResponse("Mobile Version of site is not available")


    if request.method == 'POST':


        print("sdfsdfsdfsfsdfsdfsd")

        random_list = []
        count = 0
        details = []

        while count<=2:

            random_num = randint(1,4)
            print(random_num)
            if random_num not in random_list:

                try:
                    obj = Questions.objects.get(id = random_num )
                    dic = {}
                    dic['id'] = random_num
                    dic['question'] = obj.question
                    dic['choice1'] = obj.choice1
                    dic['choice2'] = obj.choice2
                    dic['choice3'] = obj.choice3
                    dic['choice4'] = obj.choice4
                    dic['correct_answer'] = obj.correct_answer
                    details.append(dic)
                    random_list.append(random_num)
                    count += 1
                    print(dic)

                except:
                    pass

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
            print('sdfdfwerwer')
            return JsonResponse({'status': '300'})

        u = authenticate( username = username , password = password )
        if u:

            login( request , u)
            return JsonResponse({'status': '200'})
        else:

            print("s=invalid")
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


    print('=tttt')

    logout(request)
    return JsonResponse({'status': '200'})

