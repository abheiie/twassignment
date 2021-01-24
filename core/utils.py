import datetime
number_of_requests_per_minute = 5
number_of_requests_per_day = 100


def check_number_of_request_per_minute(request):
    """
    argument - request 
    function - check for Search limit per min(5)
    return - True if request is valid else false 
    """

    request.session['name'] = "abhishek"
    request.session.modified = True
    is_request_allowable = None

    if request.session.get('per_minute_check') == None:

        now = datetime.datetime.now()
        request_count = 1
        per_minut_value = {
            "previous_check_time" :  now,
            "request_count" : request_count
        }
        request.session['per_minute_check'] = per_minut_value

    else:
        now = datetime.datetime.now()
        session_data = request.session.get('per_minute_check')

        if (now - session_data.get("previous_check_time")).total_seconds() <= 60:
            """
            last request was within a minute
            """

            if session_data.get("request_count") <= number_of_requests_per_minute:
                """
                if request_count is less than permissible number of request_count
                """
                is_request_allowable = True
                request.session['per_minute_check']['request_count'] = session_data.get("request_count") + 1
            else:
                """
                if request_count is more than permissible number of request_count
                """
                is_request_allowable = False

        else:
            """
            last request was more than a minute ago 
            """
            now = datetime.datetime.now()
            is_request_allowable = True
            request.session['per_minute_check']['request_count'] = 1
            request.session['per_minute_check']['previous_check_time'] = datetime.datetime.now()

    return is_request_allowable


def check_number_of_request_per_day(request):
    """
    argument - request 
    function - check for Search limit per day(100)
    return - True if request is valid else false 
    """

    request.session['lastname'] = "singh"
    request.session.modified = True
    is_request_allowable = None

    if request.session.get('per_day_check') == None:
        now = datetime.datetime.now()
        request_count = 1
        per_day_value = {
            "previous_check_time" :  now,
            "request_count" : request_count
        }
        request.session['per_day_check'] = per_day_value
    else:
        session_data = request.session.get('per_day_check')
        now = datetime.datetime.now()
        if (now - session_data.get("previous_check_time")).total_seconds() <= 86400:
            """
            last request was within a day
            """
            if session_data.get("request_count") <= number_of_requests_per_day:
                """
                if request_count is less than permissible number of request_count
                """
                is_request_allowable = True
                request.session['per_day_check']['request_count'] = session_data.get("request_count") + 1
            else:
                """
                if request_count is more than permissible number of request_count
                """
                is_request_allowable = False

        else:
            """
            last request was more than a day ago 
            """
            now = datetime.datetime.now()
            is_request_allowable = True
            request.session['per_day_check']['request_count'] = 1
            request.session['per_day_check']['previous_check_time'] = now
            session_data = request.session.get('per_day_check')

    return is_request_allowable