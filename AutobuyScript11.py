# -*- coding:utf-8 _*-
import urllib.request as url_req
import urllib.parse
from bs4 import BeautifulSoup
import time
import concurrent.futures


def FreshSearch(params,userAgent):
        url = 'https://www.autobuy.tw/'
        args='ajax_do_search'
        search_url=url+args
        datas = urllib.parse.urlencode(params).encode('utf8')
        request = url_req.Request(search_url,data=datas,headers=userAgent,method='POST')
        url_req.urlopen(request).read().decode('utf-8')


def getTotalPage(userAgent):
        while True:
                try:
                        url = 'https://www.autobuy.tw/'
                        args = 'search_s20'
                        search_url=url+args
                        request = url_req.Request(search_url,headers=userAgent)
                        with url_req.urlopen(request,timeout=10) as resopnse:
                                data = resopnse.read().decode("utf-8")
                        root = BeautifulSoup(data,"html.parser")
                        FindLi = root.find("ul",{"class":"secondary"}).findAll("a")
                        ChildHouse = []
                        for i in range(len(FindLi)):
                                abc = FindLi[i].attrs["onclick"].split('(')[2].split(')')[0]
                                ChildHouse.append(abc)
                        return int(root.find("li",{"class":"last_page"}).find("a").attrs['href'][7:]),int(root.find("p",{"id":"search_result"}).find("strong").text),ChildHouse
                except Exception as e:
                        print(e)
                        with open('logs.txt','a',encoding="utf-8") as f:
                                        f.write(str(time.strftime("%Y-%m-%d", time.localtime()))+" Script "+str(e)+"\n")
                                        f.close()
                        time.sleep(5)
                        print("re-start totalpage")

def getProductInfo(PageProductsID):
        while True:
                try:
                        url = 'https://www.autobuy.tw/'
                        userAgent = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',
                        'Cookie':'ABSESSID=5m7lngc49uvdji89m34mh9o444'
                }
                        PageURL = url+"3c/"+PageProductsID
                        ProductReq = url_req.Request(PageURL,headers=userAgent)
                        with url_req.urlopen(ProductReq,timeout=10) as ProductResopnse:
                                if ProductResopnse.geturl()!=PageURL:
                                        print("being redirect need return "+PageURL)
                                        return None,None
                                ProductData = ProductResopnse.read().decode("utf-8")
                                ProductResopnse.close()
                        ProductRoot = BeautifulSoup(ProductData,"html.parser")
                        ProductTags = ProductRoot.find("ol").find_all("li")
                        ProductTagsCollect=[]
                        ProductTagsCollect2 = []

                        PageProductsName = ProductRoot.find("h1",{"class":"prod_name"}).text
                        PageProductsPrice = ProductRoot.find("strong",{"id":"purchase_price"}).text
                        for tags in range(2,len(ProductTags),1):
                                tagname = ProductTags[tags].find("a").attrs['href']
                                tagtext = ProductTags[tags].find("a").text
                                tag = {tagname : tagtext}
                                ProductTagsCollect.append(tagname)
                                ProductTagsCollect2.append(tag)
                        ProdctJson = {"id":PageProductsID,"name":PageProductsName,"price":PageProductsPrice,"tags":ProductTagsCollect}
                        # print(PageProductsID)
                        return ProdctJson,ProductTagsCollect2
                except Exception as e:
                        print(e)
                        with open('logs.txt','a',encoding="utf-8") as f:
                                        f.write(str(time.strftime("%Y-%m-%d", time.localtime()))+" Script "+str(e)+"\n")
                                        f.close()
                        time.sleep(5)
                        print("re-start "+PageURL)
                

def searchPage(page):
        while True:
                try:
                        url = 'https://www.autobuy.tw/'
                        userAgent = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',
                        'Cookie':'ABSESSID=5m7lngc49uvdji89m34mh9o444'
                }
                        searchInfo=[]
                        searchInfo2=[]
                        futures=[]
                        args = 'search_'+str(page)
                        search_url=url+args
                        request = url_req.Request(search_url,headers=userAgent)
                        print("start "+search_url)
                        with url_req.urlopen(request,timeout=10) as resopnse:
                                data = resopnse.read().decode("utf-8")
                                resopnse.close()
                        root = BeautifulSoup(data,"html.parser")
                        PageProducts = root.find("div",{"class":"products_shelf"}).find_all("section")
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                                for product in range(len(PageProducts)):
                                        try:
                                                future = executor.submit(getProductInfo,PageProducts[product].find("a").attrs['href'][3:])
                                                futures.append(future)
                                        except Exception as e:
                                                print(e)
                                                with open('logs.txt','a',encoding="utf-8") as f:
                                                        f.write(str(time.strftime("%Y-%m-%d", time.localtime()))+" Script "+str(e)+"\n")
                                                        f.close()
                        for future in futures:
                                getProdctJson,getProdctJson2 =future.result()
                                if getProdctJson!=None:
                                        searchInfo.append(getProdctJson)
                                if getProdctJson2!=None:
                                        searchInfo2.append(getProdctJson2)
                        return searchInfo,searchInfo2
                except Exception as e:
                        print(e)
                        with open('logs.txt','a',encoding="utf-8") as f:
                                        f.write(str(time.strftime("%Y-%m-%d", time.localtime()))+" Script "+str(e)+"\n")
                                        f.close()
                        time.sleep(5)
                        print("re-start "+search_url)
               
def doChildSearch(TotalPage):
        futures=[]
        with concurrent.futures.ThreadPoolExecutor() as executor:
                for page in range(2,TotalPage+1,1):
                        try:
                                future = executor.submit(searchPage,page)
                                futures.append(future)
                        except Exception as e:
                                print(e)
                                with open('logs.txt','a',encoding="utf-8") as f:
                                        f.write(str(time.strftime("%Y-%m-%d", time.localtime()))+" Script "+str(e)+"\n")
                                        f.close()
        return futures


def searchonePage(root):
        while True:
                try:
                        searchInfo=[]
                        searchInfo2=[]
                        futures=[]
                        PageProducts = root.find("div",{"class":"products_shelf"}).find_all("section")
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                                for product in range(len(PageProducts)):
                                        try:
                                                future = executor.submit(getProductInfo,PageProducts[product].find("a").attrs['href'][3:])
                                                futures.append(future)
                                        except Exception as e:
                                                print(e)
                                                with open('logs.txt','a',encoding="utf-8") as f:
                                                        f.write(str(time.strftime("%Y-%m-%d", time.localtime()))+" Script "+str(e)+"\n")
                                                        f.close()
                        for future in futures:
                                getProdctJson,getProdctJson2 =future.result()
                                if getProdctJson!=None:
                                        searchInfo.append(getProdctJson)
                                if getProdctJson2!=None:
                                        searchInfo2.append(getProdctJson2)
                
                        return searchInfo,searchInfo2
                except Exception as e:
                        print(e)
                        with open('logs.txt','a',encoding="utf-8") as f:
                                        f.write(str(time.strftime("%Y-%m-%d", time.localtime()))+" Script "+str(e)+"\n")
                                        f.close()
                        time.sleep(5)
                        print("re-start searchonePage")


def getChild(param,userAgent):
        while True:
                try:
                        print("start "+param)
                        childurl = "https://www.autobuy.tw/search_shop"+param+"_min0_max100000000"
                        request = url_req.Request(childurl,headers=userAgent)
                        with url_req.urlopen(request,timeout=15) as resopnse:
                                        data = resopnse.read().decode("utf-8")
                                        resopnse.close()
                        root = BeautifulSoup(data,"html.parser")
                        return root
                except Exception as e:
                        print(e)
                        with open('logs.txt','a',encoding="utf-8") as f:
                                        f.write(str(time.strftime("%Y-%m-%d", time.localtime()))+" Script "+str(e)+"\n")
                                        f.close()
                        time.sleep(5)
                        print("re-start child "+param)
        


if __name__ == '__main__':
        params = {
                "search":'" "',
                "shop":"20"
        }
        userAgent = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',
                'Cookie':'ABSESSID=5m7lngc49uvdji89m34mh9o444'
        }
        timetag = time.strftime("%Y-%m-%d", time.localtime())
        start_time = time.time()
        FreshSearch(params,userAgent)
        TotalPage,TotalProductNum,ChildHouse = getTotalPage(userAgent)
        ChildHouseNum = []
        retDict=[]
        retDict2=[]
        print(len(ChildHouse))
        for i in range(len(ChildHouse)):
                        root = getChild(ChildHouse[i],userAgent)
                        try:  
                                TotalPage = int(root.find("li",{"class":"last_page"}).find("a").attrs['href'][7:])
                                tmp1,tmp2 = searchonePage(root)
                                retDict+=tmp1
                                for firstlist in tmp2:
                                        for secondlist in firstlist:
                                                if secondlist not in retDict2:
                                                        retDict2.append(secondlist)
                                

                                getfutures = doChildSearch(TotalPage)
                                for future in getfutures:
                                        tmp1,tmp2 =future.result()
                                        retDict+=tmp1
                                        for firstlist in tmp2:
                                                for secondlist in firstlist:
                                                        if secondlist not in retDict2:
                                                                retDict2.append(secondlist)


                                print("finish "+ChildHouse[i])
                        except Exception as e:
                                tmp1,tmp2 = searchonePage(root)
                                retDict+=tmp1
                                for firstlist in tmp2:
                                        for secondlist in firstlist:
                                                if secondlist not in retDict2:
                                                        retDict2.append(secondlist)

                                print("finish "+ChildHouse[i])
                
                

        print(TotalProductNum)

        print("compiling......")
        final = str(retDict).replace("\"","吋").replace("'","\"").replace("[email\\xa0protected]","@")
        with open('./AutobuyJson/autobuy'+timetag+'.json','w',encoding="utf-8") as f:
                f.write(final)
                f.close()
        final2 = str(retDict2).replace("\"","吋").replace("'","\"").replace("[email\\xa0protected]","@")
        with open('./AutobuyJson/autobuy_tag'+timetag+'.json','w',encoding="utf-8") as f:
                f.write(final2)
                f.close()
        print ("總花費:"+str(time.time() - start_time)+"秒")


