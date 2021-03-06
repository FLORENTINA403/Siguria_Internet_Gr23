import tkinter as tk
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from tkinter.ttk import Combobox
import tkinter.scrolledtext as st
from tkinter import messagebox

def xss_target(url):
  target=url
  payload = "*script* alert('XSS'); /*script* "
  req = requests.post(target + payload)
  if payload in req.text:
    output.insert(tk.INSERT,"XSS Vulnerablity discovered!")
  else:
    output.insert(tk.INSERT,"Secure\n")


def get_all_forms(url):
    try:
        soup = bs(requests.get(url).content, "html.parser")
        
    except Exception as e:
        error = e.read()
        output.insert(tk.INSERT, error)
    return soup.find_all("form")


def get_form_details(form):
   try:
       details = {}
       action = form.attrs.get("action").lower()
       method = form.attrs.get("method", "get").lower()
       inputs = []
       for input_tag in form.find_all("input"):
           input_type = input_tag.attrs.get("type", "text")
           input_name = input_tag.attrs.get("name")
           inputs.append({"type": input_type, "name": input_name})
       details["action"] = action
       details["method"] = method
       details["inputs"] = inputs
       
   except Exception as e:
       error = e.read()
       output.insert(tk.INSERT, error)
   return details
def submit_form(form_details, url, value):
    try:
        target_url = urljoin(url, form_details["action"])
        inputs = form_details["inputs"]
        data = {}
        for input in inputs:
            if input["type"] == "text" or input["type"] == "search":
                input["value"] = value
            input_name = input.get("name")
            input_value = input.get("value")
            if input_name and input_value:
                data[input_name] = input_value
    except Exception as e:
        error = e.read()
        output.insert(tk.INSERT, error)
    if form_details["method"] == "post":
         return requests.post(target_url, data=data)
    else:
         return requests.get(target_url, params=data)
   

def scan_xss(url):
    try:
        # get all the forms from the URL
        forms = get_all_forms(url)
        rez1 = str(f"[+] Detected {len(forms)} forms on {url}.")
        js_script = "<Script>alert('hi')</scripT>"
        # returning value
        is_vulnerable = False
        # iterate over all forms

        for form in forms:
            form_details = get_form_details(form)
            content = submit_form(form_details, url, js_script).content.decode()
            if js_script in content:
                rez2 = str(f"[+] XSS Detected on {url}")
                rez3 = str(f"[*] Form details:")
            
                is_vulnerable = True
            # won't break because we want to print available vulnerable forms
    except Exception as e:
        error = e.read()
        return error        
    if True:        
         return rez1 +"\n" + rez2 + "\n" + rez3 + "\n"+str(form_details) + "\n"
    else:
         return "something went worng"
    
#window
window = tk.Tk()
window.title("XSS Testing")

#URL label
url_label = tk.Label(window, text = 'Enter URL')
url_label.configure(padx = 0, pady = 0)
url_label.configure(font="TkFixedFont")
url_label.configure(background="#EDF2F3")
url_label.configure(foreground="#000000")
url_label.place(x=10, y=12)

#URL field
url = tk.Entry(window)
url.place(x=110, y=13, relheight=0.05, relwidth=0.53)
url.configure(background="white")
url.configure(disabledforeground="#a3a3a3")
url.configure(font="TkFixedFont")
url.configure(foreground="#000000")
url.configure(highlightbackground="#d9d9d9")
url.configure(highlightcolor="black")
url.configure(insertbackground="black")
url.configure(selectbackground="#c4c4c4")
url.configure(selectforeground="black")

def clicked():
   full_scan = v1.get()
   forms = v2.get()
   res = url.get()

   if forms == 1:
        if res.startswith("http://") != True and res.startswith("https://") != True:
            messagebox.showerror("Error", "Please enter correct URL!")
        else:
            txt = scan_xss(res)
            output.insert(tk.INSERT, txt)
            
            

   elif full_scan == 1:
       if res.startswith("http://") != True and res.startswith("https://") != True:
           messagebox.showerror("Error", "Please enter correct URL!")
       else:
           xss_target(res)

   else:
       messagebox.showerror("Error", "Please select an option!")

def clear():
    output.delete('1.0', tk.END)
    v1.set(0)
    v2.set(0)
    url.delete(0,tk.END)
#BruteXSS button
button = tk.Button(window, width=15,activebackground='#FFFFFF',command=clicked)
button.configure(padx = 0, pady = 0,font =("Courier",10))
button.place(x=450,y=11)
button.configure(foreground="white")
button.configure(background="gray")
button.configure(activebackground="#FFFFFF")
button.configure(text='''BruteXSS''')

#Clear button
button = tk.Button(window, width=15,activebackground='#FFFFFF',command=clear)
button.configure(padx = 0, pady = 0,font =("Courier",10))
button.place(x=450,y=40)
button.configure(foreground="white")
button.configure(background="gray")
button.configure(activebackground="#FFFFFF")
button.configure(text='''Clear''')

#Full Scan
v1 = tk.IntVar()
c1 = tk.Checkbutton(window,variable = v1)
c1.place(x=170, y=70)
c1.configure(activebackground="#d9d9d9")
c1.configure(activeforeground="#000000")
c1.configure(background="#EDF2F3")
c1.configure(text='''Full Scan''')

#HTML Forms
v2 = tk.IntVar()
c2 = tk.Checkbutton(window,variable = v2)
c2.place(x=270, y=70)
c2.configure(activebackground="#d9d9d9")
c2.configure(activeforeground="#000000")
c2.configure(background="#EDF2F3")
c2.configure(text='''HTML Forms''')

#Output Label
TLabel5 = tk.Label(window)
TLabel5.place(relx=0.03, rely=0.22, height=19, width=42)
TLabel5.configure(background="#EDF2F3")
TLabel5.configure(foreground="#000000")
TLabel5.configure(text='''Output''')

#Output Box
output = st.ScrolledText(window,wrap=tk.WORD)
output.place(relx=0.07, rely=0.27, relheight=0.40, relwidth=0.84)
output.configure(background="white")
output.configure(font="TkTextFont")
output.configure(foreground="black")
output.configure(highlightbackground="#d9d9d9")
output.configure(insertborderwidth="3")
output.configure(width=10)
output.configure(state=tk.NORMAL)



#Exit Button
button = tk.Button(window, width=10, command=window.destroy)
button.place(x=515, y=475)
button.configure(foreground="white")
button.configure(background="gray")
button.configure(activebackground="#FFFFFF")
output.configure(font="TkTextFont")
button.configure(text='''Exit''')
button.configure(padx = 0, pady = 0)

window.geometry("600x500+200+200")
window['background']='#EDF2F3'
window.mainloop()








