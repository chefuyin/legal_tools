import random,requests,re
import lxml.html
from lxml.html import etree
from bs4 import BeautifulSoup
import time
import pyquery
import json



class NpcLawSpider():
    def __init__(self):
        self.request_url='http://law.npc.gov.cn/FLFG/getAllList.action'
        self.half_law_url='http://law.npc.gov.cn/FLFG/flfgByID.action?flfgID='
        self.index='http://law.npc.gov.cn/FLFG/'
        self.constitution_url='http://law.npc.gov.cn/FLFG/index/xianfamore.jsp'
        self.criminal_law_url='http://law.npc.gov.cn/FLFG/index/xingfamore.jsp'
        self.local_regulation_url='http://law.npc.gov.cn/FLFG/ksjsCateGroup.action'
        self.check_url='http://law.npc.gov.cn/FLFG/getAllList.action?SFYX=%E6%9C%89%E6%95%88&zlsxid=11&bmflid=&zdjg=&txtid=&resultSearch=false&lastStrWhere=&keyword=&pagesize=50'
        self.department_id_url='http://law.npc.gov.cn/FLFG/zdjg.action?_=1509374098898'
    # 导入数据集并随机获取一个User-Agent
    def random_user_agent(self):
        user_agent_list = []
        f = open('user_agent.txt', 'r')
        for date_line in f:
            user_agent_list.append(date_line.replace('\n', ''))
        user_agent = random.choice(user_agent_list)
        return user_agent

    def common_headers(self):
        user_agent = self.random_user_agent()
        '''参数引入及头信息'''
        if len(user_agent) < 10:
            user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'
        # 此处修改头字段,
        headers = {
            "User-Agent": user_agent,
        }
        return headers

    # generate request headers,just for request the law list by province number , law type number etc.
    def special_request_headers(self):
        user_agent = self.random_user_agent()
        '''参数引入及头信息'''
        if len(user_agent) < 10:
            user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'
        # 此处修改头字段,
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            'Cache-Control': 'max-age=0',
            "Connection": "keep-alive",
            "User-Agent": user_agent,
            'Referer': '',
        }
        return headers

    ##already write the ids in to the json file
    # def department_id(self):
    #     url=self.department_id_url
    #     headers=self.common_headers()
    #     response=requests.get(url,headers=headers)
    #     if response.status_code==200:
    #         with open('department_id.json','w') as file:
    #             file.write(response.text)

    def read_department_id(self):
        id_list=[]
        with open("department_id.json","r") as file:
            json_text= file.read()
            department_id_dict=json.loads(json_text)
            # print(department_id_dict)
            for item in department_id_dict:
                id=item["zdxid"]
                id_list.append(id)

        return id_list

    def advanced_search_request_data(self,page):
        data={
            'bbrqbegin':'',
            'bbrqend':'',
            'bbwh':'',
            'bmflid':'',
            'bt':'',
            'curPage':page,
            'flfgnr':'',
            'lastStrWhere': 'SFYX:(有效) ^ ZLSX:(01~02~03~04~05~06~08~09~10~11~12~23) ^ DWDMCODE:(3) ^ SFFB=Y ',
            'pageCount':'133',
            'pagesize':'50',
            'resultSearch':'false',
            'sxrqbegin':'',
            'sxrqend':'',
            'sxx':'有效',
            'xldj':'',
            'zdjg':'3',
            'zlsxid':'',
        }
        return data


    def index_page(self):
        headers = self.common_headers()
        html=requests.get(self.index,headers=headers)
        if html.status_code==200:
            return html.text

    def parse_index_page_law(self,html):
        soup=BeautifulSoup(html,'lxml')
        spans=soup.find_all('span',class_="blue")
        for span in spans:
            datas = {}
            if span.get_text()=='宪法':
                pass
            elif span.get_text()=='刑法':
                pass
            else:
                ptn=re.compile(r"'(.*?)'")
                results=ptn.findall(span["onclick"])
                types=['zlsxid', 'bmflid', 'zdjg', 'txtid']
                data={}
                for type,result in zip(types,results):
                    dict={
                        type:result
                    }
                    data.update(dict)
                law_name=self.translate_law_name(span.get_text())
                datas.update({law_name:data})
                print(datas)
            # print(xianfa)

    def translate_law_name(self,chinese_law_name):
        name_dict={
            '宪法相关法':'constitutional_law',
            '民法商法':'civil_commercial_law',
            '行政法': 'administrative_law',
            '经济法': 'economic_law',
            '社会法': 'social_law',
            '诉讼与非诉讼程序法': 'procedure_law',
            '有关法律问题的决定': 'decisions_on_law',
            '关于修改批准废止法律的决定': 'decision_on_amending',
            '关于批准缔结条约的决定': 'decision_on_treaty',
        }
        english_law_name='other_law'
        for k,v in name_dict.items():
            if chinese_law_name==k:
                english_law_name=v
        return english_law_name

    #get the city number in the index page and use the number to get the number of regulations in this province
    #return a dict of provinces
    def parse_provinces(self,html):
        soup=BeautifulSoup(html,'lxml')
        results=soup.select('ul[class="threecloumntitle"] > li > a')
        province_num_dict={}
        for result in results:
            # print(result)
            href=result["href"]
            ptn=re.compile(r"'(.*?)'")
            province_num=ptn.findall(href)[-1]
            province_name=self.translate_province_name(result.get_text())
            data={province_name:province_num}
            province_num_dict.update(data)
        return province_num_dict

    #translate Chinese province name into english
    def translate_province_name(self,chinese_province_name):
        dict={
            '北京':'Beijing','天津': 'Tianjin','河北': 'Hebei',
            '山西': 'Shanxi','内蒙古': 'InnerMongol','辽宁': 'Liaoning',
            '吉林': 'Jilin','黑龙江': 'Heilongjiang','上海': 'Shanghai',
            '江苏': 'Jiangsu','浙江': 'Zhejiang', '安徽': 'Anhui',
            '福建': 'Fujian','江西': 'Jiangxi','山东': 'Shandong',
            '河南': 'Henan', '湖北': 'Hubei', '湖南': 'Hunan',
            '广东': 'Guangdong', '广西': 'Guangxi', '海南': 'Hainan',
            '重庆': 'Chongqing', '四川': 'Sichuan', '贵州': 'Guizhou',
            '云南': 'Yunnan', '西藏': 'Tibet', '陕西': 'Shaanxi',
            '甘肃': 'Gansu', '青海': 'Qinghai', '宁夏': 'Ningxia',
            '新疆': 'Xinjiang'
        }
        english_province_name=''
        for k,v in dict.items():
            if chinese_province_name==k:
                english_province_name=v
        return english_province_name


    #generate list page requests data,such as page pagesize
    def list_page_request_data(self,page):
        data = {
            'pagesize': '20',
            'ispage': '1',
            'pageCount': '500',
            'curPage': str(page),
            'SFYX': '有效',
            'zlsxid': '03',
            'fenleigengduo': '',
            'bmflid': '',
            'zdjg': '',
            'txtid': '',
            'resultSearch': 'false',
            'lastStrWhere': '',
            'keyword': '',
        }
        return data

    #request data for getting the number of every city's regulations
    def local_regulation_request_data(self,txtid,keyword=None,zlsxid=None,bmflid=None,zdjg=None):
        data={
        'keyword':keyword,
        'zlsxid':zlsxid,
        'bmflid':bmflid,
        'zdjg':zdjg,
        'txtid':str(txtid),
        }
        return data

    #parse local regulation number and use the number to calculate the total page in request functions
    def parse_local_regulation_number_rule(self):
        rule='//span[@id="resultCount_span"]/text()'
        return rule


    #get the number of local regulations
    def local_regulation_number(self,province_num):
        url=self.local_regulation_url
        headers = self.common_headers()
        data=self.local_regulation_request_data(province_num)
        html = requests.post(url, headers=headers,data=data)
        if html.status_code == 200:
            return html.text



    #input page and request data to get list page
    def list_page(self,data):
        data=data
        headers=self.special_request_headers()
        try:
            url = self.request_url
            req = requests.post(url, headers=headers, data=data)
            print(req.status_code,req.headers)
            html=req.text#,timeout=20
            print (html)

            return html
        except Exception as e:
            print(Exception, e)
            return -1

    #set law id parse rule from law list page
    def parse_law_id_rule(self):
        rule='//td[@class="td"]/a[1]/@href'#抓取第一个a标签，因为会重复
        return rule

    #parse html and return result
    def parse_html(self,html,xpath_rule):
        selector = lxml.html.fromstring(html)
        result=selector.xpath(xpath_rule)
        return result

    def parse_id(self,id_list):
        pattern=re.compile(r"'(.*?)'")
        new_id_list=[]

        for i in id_list:
            # print(i)
            match= pattern.findall(i)
            if match:
                id=match[0]
                # print(law_url)
                new_id_list.append(id)
        return new_id_list

    #merge full law url to get law content
    def merge_law_url(self,id):
        full_law_url=self.half_law_url+id
        return full_law_url

    #get the law content html by requests.get method
    def law_content_html(self,full_law_url):
        headers={
            'User-Agent':self.random_user_agent()
        }
        html=requests.get(full_law_url,headers=headers).text
        return html

    # set law title parse rule
    def parse_law_tiltle_rule(self):
        rule='//div[@class="bt"]/text()'
        return rule

    #set law information parse rule
    def parse_law_info_rule(self):
        rule='//table/tr[td]'
        return rule

    #set law content text parse rule
    def parse_law_content_rule(self):
        rule='//div[@class="nr"]/div[3]'
        return rule

    # set law decription text parse rule
    def parse_law_description_rule(self):
        rule='//div[@style="text-indent: 2em;"]/text()'
        return rule

    def parse_relate_law_in_content(self):
        pass

    def parse_ralate_file_in_footer(self):
        pass

    #parse law title from law content page
    def law_title(self,html,rule):
        law_title= self.parse_html(html,rule)[0].strip()
        return law_title

    # parse law information from law content page
    # it's containing a table of law info such as date,type
    # complicated
    # it's a dict, be careful,easy to write in database
    def law_info(self,html,rule):
        law_info=self.parse_html(html,rule)#get table
        law_info_dict = self.translate_law_info(law_info)
        return law_info_dict

    #parse content,it's diffrent from others,as there are many <a> elements in the content
    #use etree.HTML and xpath('string(.)') to get the text in <a> elements
    def law_content(self,html,rule):
        tree=etree.HTML(html)
        law_content=tree.xpath(rule)
        law_content_list = []
        for paras in law_content:
            para = str(paras.xpath('string(.)'))
            list = para.split()
            law_content_list = law_content_list + list
        law_content_lines = '\r\n'.join(law_content_list)
        return law_content_lines

    # parse law information from law content page
    def translate_law_info(self,text_list):
        replace_words = {
            '资料属性：': 'file_type',
            '部门分类：': 'classification',
            '制定机关：': 'department',
            '颁布文号：': 'file_number',
            '颁布日期：': 'publish_date',
            '施行日期：': 'enforcement_date',
            '时 效 性：': 'valid_invalid',
            '失效日期：': 'invalid_date',
        }
        new_data = {}
        for text in text_list:
            english_text_list = []
            for i in text.itertext():
                # if i.strip()!='':
                i = i.strip()
                for k, v in replace_words.items():
                    if k == i:
                        i = v
                english_text_list.append(i)

            if len(english_text_list) == 9:
                data = {
                    english_text_list[1]: english_text_list[3],
                    english_text_list[5]: english_text_list[7],
                }
                # print(data)
                new_data.update(data)

            elif len(english_text_list) == 5:
                data = {
                    english_text_list[1]: english_text_list[3],
                }
                # print(data)
                new_data.update(data)
        return new_data

    #law description under law title
    def law_description(self,html,rule):
        law_discription = self.parse_html(html,rule)[0].strip()
        return law_discription

    def relate_law_in_content(self,html,rule):
        pass

    def relate_file_in_footer(self,html,rule):
        pass




if __name__== '__main__':
    a=NpcLawSpider()
    a.read_department_id()



    # for page in range(501,502):
    #     print(page)
    #     req_data=a.list_page_request_data(page)
    #     html=a.list_page(req_data)
    #     rule=a.parse_law_id_rule()
    #     ids=a.parse_html(html,rule)
    #     print(ids)
    #     id_list=a.parse_id(ids)
    #     print(id_list)
    #     for id in id_list:
    #         print(a.merge_law_url(id))
    #     print('*'*20)
    #     time.sleep(5)




    # url = 'http://law.npc.gov.cn/FLFG/flfgByID.action?flfgID=36698822'
    # html=a.law_content_html(url)
    # # print(html)
    # rule=a.parse_law_info_rule()
    # lawinfo=a.law_info(html,rule)
    # print(lawinfo)

    # for i in range(1,3):
    #     result=a.get_request(str(i))
    #     # print(result)
    #     if result==-1:
    #         print('error')
    #     else:
    #         ids=a.parse_html(result)
    #         a.parse_id(ids)

