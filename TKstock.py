from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import tkinter as tk

def _hit1():#股價資訊
    global enT
    user_agent ={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    oP=wd.ChromeOptions()
    oP.add_argument("--user-agent=%s" % user_agent)
    oP.add_argument("headless")
    wwW=wd.Chrome(options=oP)
    urL="https://goodinfo.tw/tw/index.asp"

    wwW.implicitly_wait(10)
    wwW.maximize_window()
    wwW.get(urL)

    keyWord=wwW.find_element(By.ID,"txtStockCode")

    keyWord.send_keys(enT.get())
    keyWord.send_keys(Keys.ENTER)

    itemS=wwW.find_elements(By.TAG_NAME,"tbody")

    for item in itemS:
        listBox.insert(tk.END,item.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/th/table/tbody/tr/td[1]/nobr/a").text)
        listBox.insert(tk.END,"成交價:"+item.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td[1]").text+"、"+"漲跌價:"+item.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td[3]").text+"("+item.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td[4]").text+")")
        listBox.insert(tk.END,"成交張數:"+item.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[5]/td[1]").text+"、"+"成交金額:"+item.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[5]/td[2]/nobr").text)
        listBox.insert(tk.END,"成交筆數:"+item.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[5]/td[3]").text+"、"+"成交均價:"+item.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[5]/td[5]").text)
        listBox.insert(tk.END,"-"*50)
        break
       
def _hit11():#公司基本資料
    global enT
    user_agent ={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    oP=wd.ChromeOptions()
    oP.add_argument("--user-agent=%s" % user_agent)
    oP.add_argument("headless")
    wwW=wd.Chrome(options=oP)
    urL="https://goodinfo.tw/tw/index.asp"

    wwW.implicitly_wait(10)
    wwW.maximize_window()
    wwW.get(urL)

    keyWord=wwW.find_element(By.ID,"txtStockCode")

    keyWord.send_keys(enT.get())
    keyWord.send_keys(Keys.ENTER)

    itemS=wwW.find_elements(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody")

    for item in itemS:
        listBox.insert(tk.END,item.find_element(By.CLASS_NAME,"bg_h0").text)
        listBox.insert(tk.END,item.find_element(By.CLASS_NAME,"bg_h1").find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[2]/td[2]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[3]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[4]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[5]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[6]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[7]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[8]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[9]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[10]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[11]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[12]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[13]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[14]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[15]').text)
        listBox.insert(tk.END,item.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[1]/tbody/tr[16]').text)
        listBox.insert(tk.END,"-"*50)
        break    
    
def _hit12():#三率
    global enT
    user_agent ={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    oP=wd.ChromeOptions()
    oP.add_argument("--user-agent=%s" % user_agent)
    oP.add_argument("headless")
    wwW=wd.Chrome(options=oP)
    urL="https://goodinfo.tw/tw/index.asp"

    wwW.implicitly_wait(10)
    wwW.maximize_window()
    wwW.get(urL)

    keyWord=wwW.find_element(By.ID,"txtStockCode")

    keyWord.send_keys(enT.get())
    keyWord.send_keys(Keys.ENTER)    
    GG=wwW.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/th/table/tbody/tr/td[1]/nobr/a')
    
    listBox.insert(tk.END,GG.text)
    per=wwW.find_elements(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody')
    
    for p in per:
        
        listBox.insert(tk.END,p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[3]/td[1]').text+":"+"毛利率:"+p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[3]/td[4]').text+"營益率:"+p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[3]/td[5]').text+"淨利率:"+p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[3]/td[6]').text)
        listBox.insert(tk.END,p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[4]/td[1]').text+":"+"毛利率:"+p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[4]/td[4]').text+"營益率:"+p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[4]/td[5]').text+"淨利率:"+p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[4]/td[6]').text)
        listBox.insert(tk.END,p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[5]/td[1]').text+":"+"毛利率:"+p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[5]/td[4]').text+"營益率:"+p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[5]/td[5]').text+"淨利率:"+p.find_element(By.XPATH,'//*[@id="FINANCE_INCOME_M"]/div/div/table/tbody/tr[5]/td[6]').text)
        listBox.insert(tk.END,"-"*50)
        
def _hit13():#股東持股結構
    global enT
    user_agent ={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    oP=wd.ChromeOptions()
    oP.add_argument("--user-agent=%s" % user_agent)
    oP.add_argument("headless")
    wwW=wd.Chrome(options=oP)
    urL="https://goodinfo.tw/tw/index.asp"

    wwW.implicitly_wait(10)
    wwW.maximize_window()
    wwW.get(urL)

    keyWord=wwW.find_element(By.ID,"txtStockCode")

    keyWord.send_keys(enT.get())
    keyWord.send_keys(Keys.ENTER)   
    GG=wwW.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/th/table/tbody/tr/td[1]/nobr/a')
    listBox.insert(tk.END,GG.text)
    companY=wwW.find_elements(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[1]/div[9]/div/table/tbody')
    for C in companY:
        listBox.insert(tk.END,"外資:"+C.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[1]/div[9]/div/table/tbody/tr[3]/td[5]').text+"%"+","+"散戶:"+C.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[1]/div[9]/div/table/tbody/tr[4]/td[5]/nobr').text+"%"+","+"政府:"+C.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[1]/div[9]/div/table/tbody/tr[5]/td[5]/nobr').text+"%"+","+"金融機構:"+C.find_element(By.XPATH,'/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[1]/div[9]/div/table/tbody/tr[6]/td[5]/nobr').text+"%,"+"法人:"+C.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[1]/div[9]/div/table/tbody/tr[7]/td[5]/nobr").text+"%,"+"庫藏股:"+C.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[1]/div[9]/div/table/tbody/tr[8]/td[5]/nobr").text+"%")
        listBox.insert(tk.END,"-"*50)
    
    
def _hit2():
    wiN.destroy()
def _hit3():
    listBox.delete(0,tk.END)
    enT.delete(0,tk.END)

wiN=tk.Tk()

wiN.title("股票資料查詢")

wiN.geometry("900x700+200+10")


enT=tk.Entry(wiN,font=("標楷體",12),bd=6)
enT.place(x=50,y=30)
lbL=tk.Label(wiN,text="請輸入股票代號",width=15,bg="yellow")
lbL.place(x=60,y=60)
btN1 = tk.Button(wiN, text="股價資訊",fg="green", font=("Arial", 16), width=8, height=1, command=_hit1)
btN1.place(x=230,y=25) 
btN2 = tk.Button(wiN, text="離開!!",fg="green", font=("Arial", 16), width=5, height=1, command=_hit2)
btN2.place(x=560,y=25) 
btN3 = tk.Button(wiN, text="清除!!",fg="green", font=("Arial", 16), width=5, height=1, command=_hit3)
btN3.place(x=485,y=25)
btN4 = tk.Button(wiN, text="基本資料",fg="green", font=("Arial", 16), width=8, height=1, command=_hit11)
btN4.place(x=230,y=70)
btN5 = tk.Button(wiN, text="三率",fg="green", font=("Arial", 16), width=5, height=1, command=_hit12)
btN5.place(x=340,y=70)
btN6 = tk.Button(wiN, text="股東持股結構",fg="green", font=("Arial", 16), width=11, height=1, command=_hit13)
btN6.place(x=340,y=25)


sBar=tk.Scrollbar(wiN)
sBar.pack(side=tk.RIGHT,fill=tk.Y)

listBox=tk.Listbox(wiN, font=("Arial", 16),height=22,yscrollcommand=sBar.set)
listBox.pack(side=tk.BOTTOM, fill=tk.BOTH)
sBar.config(command=listBox.yview)
wiN.mainloop()