from django.shortcuts import render
import csv,codecs
from datetime import datetime,timedelta
# Create your views here.
DAYNAMES = [ "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
def home(request):
    ctx = {}

    if request.method == 'POST':
        file = request.FILES.get('csv')
        earnings_data = []
        reader = csv.reader(codecs.iterdecode(file.file, 'utf-8'))
        for index,row in enumerate(reader):
            if index>0:
                
                earned = row[4]
                earning_time = row[5]
                earnings_data.append((earned,earning_time))
        ctx['data'] = process(earnings_data)
        return render(request,'app/hourlyrate.html',ctx)

    return render(request,'app/home.html',ctx)


def process(data) :
    """takes tupples and returns hourly income array of tupples """
    max_time = datetime.strptime(data[len(data)-1][1], '%Y-%m-%dT%H:%M:%S+13:00') 
    min_time = datetime.strptime(data[1][1], '%Y-%m-%dT%H:%M:%S+13:00')
    good_data_aray = []
    total = 0
    number_of_hours_between_max_and_min_time = int((max_time - min_time ).total_seconds()/3600)
    for i in range(number_of_hours_between_max_and_min_time):
        from_time = min_time +timedelta(hours=i)
        to_time = min_time +timedelta(hours=i+1)
        earned = get_earned_between_hours(from_time, to_time,data)
        to_time_str = f'{DAYNAMES[to_time.weekday()] }  {to_time.hour}:{to_time.minute}' 
        time_str = f'{from_time}   to   {to_time_str} ->  {earned/100}'
        if earned > 0:
            if earned > 2000:
                time_str += '  above minimum wage' 
            elif earned < 1700:
                time_str += ' BAD'

            good_data_aray.append(time_str)
        total +=earned
    totalHoursworked = len(good_data_aray)-1
    good_data_aray.append(f'total =   {str(total/100)} in about {totalHoursworked } hours so net = { round((total/totalHoursworked)/100,2) }' )
    return good_data_aray 

    # for tupple in data:
    #     earned = tupple[4]
    #     earning_time = datetime.strptime(tupple[5], '%Y-%m-%dT%H:%M:%S+12:00')


def get_earned_between_hours(from_time, to_time,data) -> int:
    """Returns dollar int earned   """
    earned = 0
    for tupple in data:
        try:
        	time = datetime.strptime(tupple[1], '%Y-%m-%dT%H:%M:%S+13:00') 
       	except ValueError:
		
		time = datetime.strptime(tupple[1], '%Y-%m-%dT%H:%M:%S+12:00') 

		if time < to_time and time > from_time:
            		if float(tupple[0])>float(0.00):
                		earned += int(float(tupple[0])*100)
            
    return earned


    
