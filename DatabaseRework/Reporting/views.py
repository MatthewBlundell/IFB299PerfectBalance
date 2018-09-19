from django.http import HttpResponse
from django.template import loader
from Search.models import Order, Vehicle, User


# Create your views here.

def Report(request):
    week1 = ["20070207", "20070220", "20070221", '20070222', '20070223', '20070224', '20070225']
    week1counts = []
    monthlength = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    monthcounts = []
    year = week1[0][0:4]
    month = week1[0][4:6]
    day = week1[0][6:8]

    ordersmonth = []
    ordersweek = []
    for i in range(28):
        intday = int(day)
        if i == 0:
            intday -= 1
        intday += 1

        if (intday > monthlength[int(month) - 1]):
            day = '01'
            intmonth = int(month)
            intmonth += 1

            if intmonth > 12:
                month = '01'
                intyear = int(year)
                intyear += 1
                year = str(intyear)
            elif intmonth < 10:
                month = '0' + str(intmonth)

        elif intday < 10:
            day = '0' + str(intday)
        else:
            day = str(intday)
        date = year + month + day

        if i < 7:
            week1counts.append(Order.objects.filter(pickupdate=date).count())

        monthcounts.append(Order.objects.filter(pickupdate=date).count())
        for z in Order.objects.filter(pickupdate=date).extra(
            {'carid_uint': "CAST(carid as UNSIGNED)", 'userid_uint': "CAST(userid as UNSIGNED)"}):
            ordersmonth.append(z)
            if i < 7:
                ordersweek.append(z)

    week1total = sum(monthcounts[0:6])
    week2total = sum(monthcounts[7:13])
    week3total = sum(monthcounts[14:20])
    week4total = sum(monthcounts[21:27])


    vehicles = []
    people = []
    for i in ordersmonth:
        vehicles.append(Vehicle.objects.get(carid=i.carid_uint))
        people.append(User.objects.get(userid=i.userid_uint))

    together = zip(vehicles, people, ordersmonth)

    template = loader.get_template('reporting.html')
    context = {
        'together': together,
        'day': week1counts[0],
        'day2': week1counts[1],
        'day3': week1counts[2],
        'day4': week1counts[3],
        'day5': week1counts[4],
        'day6': week1counts[5],
        'day7': week1counts[6],
        'week1total': week1total,
        'week2total': week2total,
        'week3total': week3total,
        'week4total': week4total,
    }

    return HttpResponse(template.render(context, request))


