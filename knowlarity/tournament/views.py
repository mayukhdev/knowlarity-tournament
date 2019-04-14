from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Sport, Team, Employee
from django.http import JsonResponse


MAX_PER_TEAM = 2
MAX_TEAM_PER_EVENT = 2


def index(request):
    context = {
        "teams": Team.objects.all()
    }
    return render(request, "tournament/index.html", context)


def bookscore(request):
    context = {
        "employees": Employee.objects.all(),
        "max_per_team": range(MAX_PER_TEAM),
        "max_team_per_event": range(MAX_TEAM_PER_EVENT),
        "sports": Sport.objects.all(),
    }
    return render(request, "tournament/bookscore.html", context)


def addscore(request):
    try:
        if request.POST:
            score_dict = {}
            for items in range(MAX_TEAM_PER_EVENT):
                key = "TEAM_SCORE_{}".format(items)
                score_dict[key] = int(request.POST[key])
            for score in score_dict:
                if score_dict[score] < 0 or score_dict[score] > 9:
                    return render(request, "tournament/error.html", {"message": "Invalid Score"})
            emp_list = []
            sport_id = int(request.POST['sport'])
            sport = Sport.objects.get(pk=sport_id)
            for event in range(MAX_TEAM_PER_EVENT):
                for team in range(MAX_PER_TEAM):
                    key = "EMP_{}_{}".format(event, team)
                    emp_list.append(int(request.POST[key]))
            employee_check = Employee.objects.filter(id__in=emp_list)
            if len(set(employee_check)) != (MAX_TEAM_PER_EVENT * MAX_PER_TEAM):
                return render(request, "tournament/error.html", {"message": "Invalid Employee"})
        else:
            return JsonResponse({"message": "Invalid Method"})
        first_team = Employee.objects.get(pk=emp_list[0])
        second_team = Employee.objects.get(pk=emp_list[1])
        third_team = Employee.objects.get(pk=emp_list[2])
        fourth_team = Employee.objects.get(pk=emp_list[3])
        # if len(set([id.id for id in first_team.team.all()]).intersection(set([id.id for id in second_team.team.all()]))) not in [0,1] or len(set([id.id for id in third_team.team.all()]).intersection(set([id.id for id in fourth_team.team.all()]))) not in [0,1]:
        #     return render(request, "tournament/error.html", {"message": "Invalid teams"})
        first_team = [first_team, second_team, third_team, fourth_team]
        for first_team_index in range(0, MAX_TEAM_PER_EVENT*MAX_PER_TEAM, MAX_PER_TEAM):
            score_value = score_dict['TEAM_SCORE_0']
            if first_team_index:
                score_value = score_dict['TEAM_SCORE_1']
            if (not first_team[first_team_index].team.exists()) or (not first_team[first_team_index+1].team.exists()):
                create_team = Team(name="", sport=sport, score=score_value)
                create_team.save()
                first_team[first_team_index].team.add(create_team)
                first_team[first_team_index+1].team.add(create_team)
            else:
                fetch_first_id = [id.id for id in first_team[first_team_index].team.all()]
                fetch_second_id = [id.id for id in first_team[first_team_index+1].team.all()]
                common_team_id = set(fetch_first_id).intersection(set(fetch_second_id))
                # print(sport)
                # print(fetch_first_id)
                # print(fetch_second_id)
                # print(common_team_id)
                # if len(common_team_id) not in [0, 1]:
                #     return render(request, "tournament/error.html", {"message": "Invalid teams"})
                # Team does exist but not common
                if not len(common_team_id):
                    create_team = Team(name="", sport=sport, score=score_value)
                    create_team.save()
                    first_team[first_team_index].team.add(create_team)
                    first_team[first_team_index+1].team.add(create_team)
                # Common team but sport different, new team
                elif Team.objects.get(pk=list(common_team_id)[0]).sport != sport:
                    create_team = Team(name="", sport=sport, score=score_value)
                    create_team.save()
                    first_team[first_team_index].team.add(create_team)
                    first_team[first_team_index+1].team.add(create_team)
                # Common Team Common Sport
                else:
                    common_team_id = common_team_id.pop()
                    team_common_team_id = Team.objects.get(pk=common_team_id)
                    # team_common_team_id.score =
                    team_common_team_id.score = team_common_team_id.score + score_value
                    # team_common_team_id.objects.update(score=new_score)
                    team_common_team_id.save()
    except KeyError:
        return render(request, "tournament/error.html", {"message": "No selection"})
    except Employee.DoesNotExist:
        return render(request, "tournament/error.html", {"message": "No Passenger"})
    except ValueError:
        return render(request, "tournament/error.html", {"message": "Improper Employee Selection"})
    except Exception as error:
        return render(request, "tournament/error.html", {"message": str(error)})

    return HttpResponseRedirect(reverse("index"))


def leaderboard(request, sport_id=None, offset=0, limit=10):
    if not sport_id:
        context = {
            "sports": Sport.objects.all()
        }
        return render(request, "tournament/leaderboard.html", context)
    else:
        try:
            if int(sport_id) in [1, 2]:
                context = {
                    "teams": Team.objects.filter(sport=int(sport_id)).order_by('-score')[int(offset):int(limit)],
                    "offset": int(offset),
                    "limit": int(limit),
                    "sport_id": int(sport_id)
                }
            else:
                return render(request, "tournament/error.html", {"message": "Improper Sport"})
        except ValueError:
            return render(request, "tournament/error.html", {"message": "Invalid Sport"})
        except Exception as error:
            return render(request, "tournament/error.html", {"message": str(error)})

        return render(request, "tournament/leaderboard-view.html", context)


def autocomplete(request):
    if request.is_ajax():
        queryset = Employee.objects.all()
        list = []
        for i in queryset:
            list.append(str(i))
        data = {
            'list': list,
        }
        return JsonResponse(data)
