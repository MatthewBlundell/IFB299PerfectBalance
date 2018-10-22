from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Search.models import Order, Vehicle, User
from django.shortcuts import redirect

# Main reporting page url request.
# Utilises the parameters of month and week in order to
# populate the charts on the reporting page.
def Report(request, date, weekNum):
    Check = False
    name = -1
    userid = -1
    auth = -1

# This code confirms whether the user is authentic. If not then
# the user will not be able to reach the reporting page.
    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        name = uservar.name
        userid = uservar.userid
        auth = uservar.authenticationlevel

    if request.session.has_key('email'):
        uservar = User.objects.get(username=request.session['email'])
        if uservar.authenticationlevel != 1:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Lists to hold data for the weekly and monthly data.
# Populated by data from the MYSQL database.
    week1counts = []
    monthlength = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    monthcounts = []
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]

    ordersmonth = []

# For loop that filters the weekly and monthly data for use in the charts
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

# Weekly data is placed into the week lists.
        if int(weekNum) == 1:
            if i < 7:
                week1counts.append(Order.objects.filter(pickupdate=date).count())
        elif int(weekNum) == 2:
            if i >= 7 and i < 14:
                week1counts.append(Order.objects.filter(pickupdate=date).count())
        elif int(weekNum) == 3:
            if i >= 14 and i < 21:
                week1counts.append(Order.objects.filter(pickupdate=date).count())
        elif int(weekNum) == 4:
            if i >= 21 and i < 28:
                print(i)
                week1counts.append(Order.objects.filter(pickupdate=date).count())

# Monthly data placed into month list.
        monthcounts.append(Order.objects.filter(pickupdate=date).count())
        for z in Order.objects.filter(pickupdate=date).extra(
            {'carid_uint': "CAST(carid as UNSIGNED)", 'userid_uint': "CAST(userid as UNSIGNED)"}):
            ordersmonth.append(z)

# Monthly data broken down into weekly segments.
# This is used in the Monthly rental chart.
    week1total = sum(monthcounts[0:6])
    week2total = sum(monthcounts[7:13])
    week3total = sum(monthcounts[14:20])
    week4total = sum(monthcounts[21:27])

# This for loop pulls all rentals matching the month requested, and
# prepares the data for displaying in a styled table in the HTML.
    vehicles = []
    people = []
    for i in ordersmonth:
        vehicles.append(Vehicle.objects.get(carid=i.carid_uint))
        people.append(User.objects.get(userid=i.userid_uint))

    together = zip(vehicles, people, ordersmonth)
    prevWeek = int(weekNum) - 1
    nextWeek = int(weekNum) + 1
    template = loader.get_template('reporting.html')


    print(week1counts[0])

# The following code is a library of all data
# that will be utilised in the HTML code of the reporting page.
    context = {
        'together': together,
        'day1': week1counts[0],
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
        'prevWeek' : prevWeek,
        'weekNum' : weekNum,
        'nextWeek' : nextWeek,
        'name': name,
        'userid': userid,
        'authlevel': auth,
        'Check': Check,
        'session': request.session.has_key('email'),
    }

# Returns the page request and data.
    return HttpResponse(template.render(context, request))

# This function returns the latest month on the reporting page.
# designed to be the default entry point to the reporting page.
def ReportRedirect(request):
    datesarray = Order.objects.order_by('pickupdate')

    yearmonth = datesarray[len(datesarray)-1].pickupdate

    latestdate = yearmonth[0:6] + "01"

    return redirect('../Reporting/' + latestdate + '/1')

# This function is called when the user utilises the
# month/year choice comboboxes.
def Redirect(request, date, weekNum):
    year = request.GET.get('Year')
    month = request.GET.get('Month')

    if(year == '-' or month == '-'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('../../../../Reporting/' + year+month+'01/1')
