import random,requests
import lxml.html
import json,time,pymysql
class GetLawFirmID():
    def __init__(self):
        self.base_url='http://caseshare.cn'
        self.lawfirm_lawyer_index='http://caseshare.cn/search/lawfirmorlawyer'
        self.default_headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'User-Agent':self.random_user_agent()
        }
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='alvincha',
            db='lawdata',
            charset='utf8'
        )

    def get_provinceid(self):
        response=requests.get(self.lawfirm_lawyer_index,headers=self.default_headers)
        selector=lxml.html.fromstring(response.text)
        urls=selector.xpath('//div[@class="crumbsType"]/a/@href')
        provinces=selector.xpath('//div[@class="crumbsType"]/a/text()')
        data_list=[]
        for url,province in zip(urls,provinces):
            province_code=url.split('=')[1]
            data={
                'url':self.base_url+url,
                'province_name':province,
                'province_code':province_code
            }
            data_list.append(data)
        return data_list

    def get_cityid(self,url):
        response=requests.get(url,headers=self.default_headers)
        selector=lxml.html.fromstring(response.text)
        city_hrefs=selector.xpath('//div[@class="crumbsType"]/a/@href')
        city_names=selector.xpath('//div[@class="crumbsType"]/a/text()')
        data_list=[]
        for city_href,city_name in zip(city_hrefs,city_names):
            city_id=city_href.split('=')[1]
            new_url=self.base_url+city_href
            data={
                'city_id':city_id,
                'city_name':city_name,
                'url':new_url
            }
            data_list.append(data)
        return data_list

    def get_lawfirm(self,pageindex,areacode):
        try:
            url='http://caseshare.cn/Tool/NavLawFirm?pagesize=18&pageindex={}&areacode={}&firstletter='.format(pageindex,areacode)
            response=requests.get(url,headers=self.default_headers,timeout=10)
            if response.status_code==200:
                if response.text is None:
                    print('None')
                    pass
                else:
                    data=json.loads(response.text)
                    if data!='':
                        time.sleep(1)
                        return data
            else:
                pass
        except TypeError as e:
            return e




    def random_user_agent(self):
        user_agent_list = []
        f = open('user_agent.txt', 'r')
        for date_line in f:
            user_agent_list.append(date_line.replace('\n', ''))
        user_agent = random.choice(user_agent_list)
        return user_agent

    def write_data(self,name,areaCode,areaName):
        conn=self.conn
        cursor = conn.cursor()
        sql = "INSERT INTO lawfirmlist (`name`,`areaCode`,`areaName`) VALUES(%(name)s,%(areaCode)s,%(areaName)s)"
        values={
            'name':name,
            'areaCode':areaCode,
            'areaName':areaName,
        }
        if self.data_check(name)[0]:
            print('already exsist')
        else:
            cursor.execute(sql,values)
            conn.commit()
    def data_check(self,name):
        conn = self.conn
        cursor = conn.cursor()
        sql = "SELECT EXISTS (SELECT 1 FROM lawfirmlist WHERE name=%(name)s)"
        value = {
            'name': name        }
        cursor.execute(sql, value)
        return cursor.fetchall()[0]



if __name__=='__main__':
    a=GetLawFirmID()
    list=a.get_provinceid()
    for i in list:
        url=i['url']
        city=a.get_cityid(url)
        for j in city:
            id=j['city_id']
            for k in range(1,60):
                try:
                    data=a.get_lawfirm(k,id)
                    for l in data:
                        if l:
                            print(l)
                            name=l['name']
                            areaCode=l['areaCode']
                            areaName=l['areaName']
                            a.write_data(name,areaCode,areaName)
                except:
                    print('error')
                    pass

