from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

# check if sequence is right by automating TAB
def compare_focus_elements(elements,j=0):
    temp = []
    flag = 0
    total_length = len(elements)
    body = driver.find_element_by_tag_name('body')
    el = driver.execute_script("return document.activeElement")
    j = elements.index(el)
    try:         
        for i in range(j+1,total):
            body.send_keys(Keys.TAB)
            el = driver.execute_script("return document.activeElement")
            temp.append(el)
            if el.id != elements[i].id:
                print("not-true",end=" ")
                flag = 1
    except:
        print("An exception occurred")
        return False
    return flag == 0


def get_data(URL):
    print("get data")
    driver = webdriver.Chrome(executable_path=r"C:\Users\Sumax\Desktop\Selenium\chromedriver.exe")

    #URL = 'https://www.facebook.com/'
   
    driver.maximize_window()
    driver.get(URL)

    # get the current page title
    page_title = driver.execute_script("return document.title")
    print(page_title)
    # -- java-script
    # get the focusable elements then filter the elements that are present in current DOM state
    elements = driver.execute_script("""
    return [...document.querySelectorAll(
    'a, button, input, textarea, select, details, [tabindex]:not([tabindex="-1"])'
    )]
    .filter(el => !el.hasAttribute('disabled')).filter(el=> el.offsetParent!==null)
    """)

    # traverse the array and print in formatted way
    total = len(elements)
    print("total elements ",total)

    data = [] # final array of objects
    for el in range(total):
        
        # create object for each element
        d = {
            'page_name':page_title,
            'id':elements[el].id
            }
        name = elements[el].get_attribute("name")
        text = elements[el].text
        title = elements[el].get_attribute("title")
        value = elements[el].get_attribute("value")
        label = elements[el].get_attribute("aria-label")
        outerHTML = elements[el].get_attribute("outerHTML")
        # if name:d['name'] = name
        # if text:d['text'] = text
        # if title:d['title'] = title
        # if value:d['value'] = value
        # if label: d['label'] =label
    
        if name:d['element'] = name
        elif text:d['element'] = text
        elif title:d['element'] = title
        elif value:d['element'] = value
        elif label: d['element'] =label

        d['HTML_tag'] = outerHTML
        data.append(d)

    return data

# this function gets fired at endpoint '/'
def index(request):

    if request.method == 'POST':  
        body_unicode = request.body.decode('utf-8')
        url = json.loads(body_unicode)
        
        data = get_data(url) # util_function ; returns array of objects 
        return JsonResponse(data, safe=False)
    return render(request, 'index.html')

