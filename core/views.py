from django.shortcuts import render
import requests
import json 
from django.core.cache import cache
import datetime
from .utils import check_number_of_request_per_minute
from .utils import check_number_of_request_per_day


def search_question(request):
    data = {}

    if request.method == 'POST':
        """
        get the POST request
        """

        is_request_allowable_for_per_day = check_number_of_request_per_day(request)
        is_request_allowable_for_per_minute = check_number_of_request_per_minute(request)

        if is_request_allowable_for_per_minute and is_request_allowable_for_per_day:
            """
            request is allowable for this minute as well as this day
            """

            # returnable data varianles 
            response = None
            total = None
            showing_page_number = None
            pagesize = 10
            total_pages = None
            items_not_present = None
            is_from_search_field = None
            page = None
            url = None
            is_first_page = None
            is_last_page = None

            # get the data from form 
            query = (str(request.POST.get('search_query','')).strip()).replace(" ", "%20")
            tag = (str(request.POST.get('tag','')).strip()).replace(" ", "%20")
            user = (str(request.POST.get('user','')).strip()).replace(" ", "%20")
            form_url = (str(request.POST.get('url','')).strip()).replace(" ", "%20")
            body = (str(request.POST.get('body','')).strip()).replace(" ", "%20")
            answers = (str(request.POST.get('answers','')).strip()).replace(" ", "%20")
            title = (str(request.POST.get('title','')).strip()).replace(" ", "%20")
            nottagged = (str(request.POST.get('nottagged','')).strip()).replace(" ", "%20")
            views = (str(request.POST.get('views','')).strip()).replace(" ", "%20")
            is_from_search_field = request.POST.get('is_from_search_field','')
            next_page = request.POST.get('next_page','')
            prev_page = request.POST.get('prev_page','')

            # check if request is coming from search field or pagination button
            if is_from_search_field == "true":
                page = str(1)
                request.session['page'] = "1"
                url = "https://api.stackexchange.com/2.2/search/advanced?page="+str(page)+"&pagesize=10&order=desc&sort=votes&views="+str(views)+"&body="+str(body)+"&url="+str(form_url)+"&user="+str(user)+"&q="+str(query)+"&title="+str(title)+"&tagged="+str(tag)+"&answers="+str(answers)+"&site=stackoverflow"
                request.session['current_url'] = url
                is_first_page = True
                
            # check if request is coming from "next" pagination button
            if next_page == "true":
                page = request.session.get('page')
                request.session['page'] = str(int(request.session.get('page'))+1)
                url = request.session.get('current_url')
                first_part_url = url[:55]
                first_and = int(url.find("&"))
                last_part_url = url[first_and:]
                middle_part_url = request.session['page']
                url = first_part_url+middle_part_url+last_part_url

           # check if request is coming from "prev" pagination button
            if prev_page == "true":
                page = request.session.get('page')
                request.session['page'] = str(int(request.session.get('page'))-1)
                url = request.session.get('current_url')
                first_part_url = url[:55]
                first_and = int(url.find("&"))
                last_part_url = url[first_and:]
                middle_part_url = request.session['page']
                url = first_part_url+middle_part_url+last_part_url

            urlkey = url

            if cache.get(urlkey) == None:
                url_to_get_total = url+"&filter=total"
                response = requests.get(url).json()
                total = requests.get(url_to_get_total).json()
                total = total.get("total")
                urlvalue = {
                    "response":response,
                    "total":total
                }
                cache.set(urlkey, urlvalue, None)
            else:
                cached_data = cache.get(urlkey) 
                response = cached_data["response"]
                total = cached_data["total"]

            #check if atleast single item present in response
            if int(total) == 0:
                items_not_present = True

            # count total number of pages
            total_pages = int(total) // pagesize

            # check for last page
            if int(request.session['page']) == int(total_pages):
                is_last_page = True
            
            # check for first page
            if int(request.session['page']) == 1:
                is_first_page = True

            data = {
                "response" : response,
                "total" : total,
                "total_pages" : total_pages,
                "page_no" : request.session['page'],
                "items_not_present": items_not_present,
                "show_pagination": True,
                "is_first_page": is_first_page,
                "is_last_page":is_last_page,
            }

            return render(request, 'core/index.html', data )

        else:
            if not is_request_allowable_for_per_day:
                data["status"] = "You have reached the number of request limit for this day"

            elif not is_request_allowable_for_per_minute:
                data["status"] = "You have reached the number of request limit for this minute"

            else:
                data["status"] = "Some thing went wrong.."

            return render(request, 'core/index.html', data )

    else:
        """
        get the GET request
        """
        data["showsearchresulttitle"] = True

        return render(request, 'core/index.html', data)