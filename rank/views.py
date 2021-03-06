#-*-coding:utf-8-*-
from member.models import *
from challenge.models import Problem, AuthLog

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

@login_required(login_url='/login/')
def ShowRankView(request):
    try:
        choice = open("rank_mode", "r").read()
    except:
        choice = "0"

    if choice == "1":
        solvers = AuthLog.objects.filter(auth_type=1).order_by('user_id', 'auth_time')
        users = UserProfile.objects.filter(~Q(score=0)).order_by('id')[:10]
        if solvers.count() == 0 or users.count() == 0:
            return render(request, 'rank/no_rank.html')

        solverList = [ solver.user_id.username for solver in solvers ]
        scores = [[0]*0 for i in xrange(users.count())]
        user = [ user.user.username for user in users ]

        sum = 0
        j = 0
        for i, solver in enumerate(solvers):
            print user[j], solverList[i]
            if user[j] == solverList[i]:
                sum += int(solver.prob_id.prob_point)
                scores[j].append(sum)
            else:
                sum = int(solver.prob_id.prob_point)
                j += 1
                try:
                    scores[j].append(sum)
                except IndexError:
                    break
        data = []
        for i, score in enumerate(scores):
            data.append(dict(name=user[i],scores=score))
        return render(request, 'rank/rank2.html', dict(users=users,
                                                       data=data))
    else:
        users = UserProfile.objects.filter(~Q(score=0)).order_by('-score', 'last_solve_time')[:30]
        return render(request, 'rank/rank.html', dict(users=users))
