from bs4 import BeautifulSoup
import requests, json, lxml, sys, re, os, copy, textwrap
from time import sleep
from urllib.request import urlopen

def clear():
    os.system('clear')
times = 0
def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        if 1/(len(s)/3) > .075:
            sleep(.075)
        else:
            sleep(1/(len(s)/4))
def fullclean(title):
    CLEANR = re.compile('<.*?>') 
    title = cleanhtml(title, CLEANR)
    CLEANR = re.compile('&.*?;')
    title = cleanhtml(title, CLEANR)   
    CLEANR = re.compile('{.*?}')
    title = cleanhtml(title, CLEANR)
    CLEANR = re.compile('@.*?}')
    title = cleanhtml(title, CLEANR)
    return title
def cleanhtml(raw_html,CLEANR):
      cleantext = re.sub(CLEANR, '', raw_html)
      return cleantext
url = ""
class DocumentWrapper(textwrap.TextWrapper):

    def wrap(self, text):
        split_text = text.split('\n')
        lines = [line for para in split_text for line in textwrap.TextWrapper.wrap(self, para)]
        return lines
while True:
    memory = url

    if times == 0:
        params = {
        "q": input("What do you want to know? "),
        "hl": "en",          
        "gl": "us",          
        "start": 0,          
        "num": 10         
    }
    else:
        params = {
            "q": input("What else do you want to know? "), 
            "hl": "en",          
            "gl": "us",          
            "start": 0,          
            "num": 10         
        }
    if "how" in params["q"].lower().replace("?", " ").split(" "):
        type = "how"
        params["q"] = "wikihow " + params["q"]
    else:
        type = "what"
        params["q"] += ' wikipedia'
    
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    clear()
    page_limit = 1
    
    page_num = 0
    
    data = []
    
    for i in range(page_limit):
        page_num += 1
            
        html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
        soup = BeautifulSoup(html.text, 'lxml')
        
        for result in soup.select(".tF2Cxc"):
            title = result.select_one(".DKV0Md").text
            try:
               snippet = result.select_one(".lEBKkf span").text
            except:
               snippet = None
            links = result.select_one(".yuRUbf a")["href"]
          
            data.append({
              "title": title,
              "snippet": snippet,
              "links": links
            })
    
        if page_num == page_limit:
            break
        if soup.select_one(".d6cvqb a[id=pnnext]"):
            params["start"] += 10
        else:
            break
    if type == "what":
        for i in data:
            if i["links"].find("wikipedia.org/wiki") == -1:
                continue
            else:
                url = i["links"]
                break

        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
    
        open("memory.py", "w").write("last_question = \"{0}\"".format(params["q"]))
        p_index=html.find("<p>")
        b_index = p_index+len("<p>")
        title = html[b_index:-1]
        open("txt.txt", "w").write(title)
        
        
    
    
        if url != memory:
            end_index = title.find("<div class=\"mw-heading mw-heading2\"><h2 ")
            title = title[0:end_index]
            title = fullclean(title)
            new_input = ""
        else:
            see_also_heading = soup.find('h2', id='See_also')
    
            if see_also_heading:
                end_index = see_also_heading.find_parent('div').find_next_sibling('div').find_previous_sibling('div').get_text() 
                title = title[0:end_index]
            else:
                title = title
    
            dict = {}
            go = True
            time = 0
            tcopy = copy.copy(title)
            zcopy = copy.copy(title)
            while go:
    
                p_index=tcopy.find("<h2 id=\"")
                b_index = p_index+len("<h2 id=\"")
                temp = tcopy[b_index:-1]
                tcopy = copy.copy(temp)
                end_index = temp.find("\"")
                temp = temp[0:end_index]
                if temp.lower() == temp:
                    break
                    go = False
                dict[temp] = temp
                t = copy.copy(temp)
                temp = temp.replace("_", " ")
                temp = temp.replace("-", " ")
                dict[t] = temp
    
                time+=1
            str = ""
            for i in dict.values():
                str += i +"\n"
            new_input = input("Choose one of these sections to go into further detail on: \n{0}".format(str))
            while True:
                clear()
                if new_input in dict.values():
                    break
                elif new_input == "None" or new_input == "none" or new_input == "nope" or new_input  == "no" or new_input == "Nope" or new_input == "No":
                    break 
                else:
                    new_input = input("Sorry, that is not an option. Please put one of these: \n{0}".format(str))
            if new_input == "None" or new_input == "none" or new_input == "nope" or new_input  == "no" or new_input == "Nope" or new_input == "No":
                    break
            p_index=html.find("<div class=\"mw-heading mw-heading2\"><h2 id=\"{0}\">".format(list(dict.keys())[list(dict.values()).index(new_input)]))
            b_index = p_index+len("<div class=\"mw-heading mw-heading2\"><h2 id=\"{0}\">".format(list(dict.keys())[list(dict.values()).index(new_input)]))
            title = html[b_index:-1]
            end_index = title.find("<div class=\"mw-heading mw-heading2\"><h2 ")
            title = title[0:end_index]
            title = fullclean(title)
        if new_input == "None" or new_input == "none" or new_input == "nope" or new_input  == "no" or new_input == "Nope" or new_input == "No":
            continue
            
        d = DocumentWrapper(width=60)
        wrapped_str = d.fill(title)
        delay_print(wrapped_str + "\n\n\n\n\n\n")
        times += 1
    else:
        for i in data:
            if i["links"].find("wikihow.com") == -1:
                continue
            else:
                url = i["links"]
                break

        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        open("txt.txt", "w").write(html)
        soupy = BeautifulSoup(html, 'html.parser')
        div = soupy.find_all('p')
        printable = "Introduction:\n"
        a = 0
        for i in div:
            if a == 2:
                printable += i.get_text() + "\n"
            a += 1
        div = soupy.find_all('div', {"class": "step_num"})
        div2 = soupy.find_all('div', {"class": "step"})
        method = 1
        for i in range(len(div)):
            if div[i].get_text()=="1":
                printable += "Method {0}:\n\n".format(method)
                method+=1
            printable += "Step {0}:\n\n".format(div[i].get_text())+div2[i].get_text()+"\n".replace("Research source", "")
        d = DocumentWrapper(width=60)
        wrapped_str = d.fill(printable)
        delay_print(wrapped_str + "\n\n\n\n\n\n")
        times += 1
