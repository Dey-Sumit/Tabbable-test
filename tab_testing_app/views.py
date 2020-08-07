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

# set up
driver=None
window_handles = None
globalData = []

def set_up(URL):
    # URL = 'https://www.google.com/'
    
    try:
        global driver,window_handles,globalData
        globalData = []
        driver = webdriver.Chrome(executable_path=r"C:\Users\Sumax\Desktop\Selenium\chromedriver.exe")
        driver.maximize_window()
        driver.get(URL)
        window_handles = driver.window_handles
        return True
    except Exception:
        print(Exception);
        return False
    

def get_data():

    global window_handles,driver
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[len(window_handles)-1])
    
    # get the current page title
    print(driver.title)
    page_title = driver.title

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
    
        if name:d['element'] = name
        elif text:d['element'] = text
        elif title:d['element'] = title
        elif value:d['element'] = value
        elif label: d['element'] =label

        d['HTML_tag'] = outerHTML
        data.append(d)
    print(len(data))
    return data

# this function gets fired at endpoint '/'
def index(request):

    if request.method == 'POST':  
        body_unicode = request.body.decode('utf-8')
        req_data = json.loads(body_unicode)
        if req_data['type'] == 'SET_UP':
            print("setup called")
            result = set_up(req_data['url'])
            if result:
                return JsonResponse({"res":"True"}, safe=False)
            else:
                return JsonResponse({"res":"False"}, safe=False)

        elif req_data['type'] == 'GET_DATA':
            print("get_data")
            result = get_data()    
            global globalData
            globalData = globalData + result
        return JsonResponse(globalData, safe=False)
    return render(request, 'index.html')

