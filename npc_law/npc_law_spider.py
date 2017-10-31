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
        self.advanced_search_url='http://law.npc.gov.cn/FLFG/flfgGjjsAction.action'
        self.id='1,101,102,2,201,202,3,4,5,500,50101,50102,50103,50104,50117,50204,50105,50106,50107,50108,50109,50110,50111,50113,50402,50114,50116,50115,50118,50119,50180,50121,50122,50205,50801,50301,501,50263,502,50302,50401,50407,50410,50404,50303,50408,50405,50463,50406,50409,50412,50413,50414,50601,50415,50466,503,50502,50522,50501,50602,504,51001,50901,50902,50903,51201,50904,50442,50444,50264,50210,50211,50276,50265,50274,50504,50505,50436,505,50464,50416,50467,50203,50425,50427,50468,50428,50429,50403,50430,50431,50411,50432,50433,50462,50441,50469,50470,50471,50207,50439,506,50250,50266,50267,50268,50209,50249,50215,50534,50269,50700,50270,50524,50212,50271,50507,50721,50258,50239,50729,50736,50167,50732,50735,50236,50238,50280,50190,50245,50281,50519,507,50416,50112,50120,50123,50124,50125,50126,50127,50128,50129,50130,50131,50132,50133,50134,50135,50136,50137,50138,50139,50140,50141,50142,50143,50144,50145,50146,50147,50148,50149,50150,50151,50152,50153,50154,50155,50156,50164,50157,50158,50159,50160,50161,50162,50163,50165,50166,50168,50169,50170,50171,50272,50206,50208,50213,50214,50216,50217,50218,50219,50220,50221,50222,50223,50202,50224,50225,50226,50227,50228,50229,50230,50231,50232,50233,50234,50235,50237,50273,50240,50241,50242,50243,50244,50246,50247,50248,50251,50252,50253,50254,50255,50256,50257,50259,50260,50261,50275,50410,50434,50411,50417,50418,50419,50420,50421,50422,50423,50424,50426,50435,50437,50438,50440,50443,50445,50446,50447,50448,50449,50450,50451,50452,50453,50454,50455,50456,50457,50458,50459,50460,50461,50540,50503,50506,50508,50509,50510,50511,50512,50513,50514,50515,50516,50517,50518,50520,50521,50541,50523,50525,50526,50527,50528,50529,50530,50531,50532,50533,50535,50536,50537,50538,50540,50731,50733,50728,50734,50539,50740,50741,50701,50702,50703,50704,50705,50706,50707,50708,50709,50710,50711,50712,50713,50714,50715,50716,50717,50718,50719,50720,50722,50723,50724,50725,50726,50727,50802,50803,50804,50805,50806,50807,50808,50809,50810,50811,50812,50813,50814,50815,50816,50817,50818,51002,51003,51101,51102,51103,51104,51105,51106,51107,51108,51108,51202,51203,51204,51205,51301,51302,51303,51304,51305,51306,51307,51308,51309,51310,51311,51312,51313,51314,51315,51316,51317,51318,51319,51320,51401,6,601,60101,60102,60103,60104,60105,60106,60107,60108,60109,60110,602,60201,60202,60203,60204,60205,60206,603,60301,60302,60303,60304,60305,60306,60307,60308,60309,60310,60311,60312,604,60401,60402,60403,60404,605,60501,60503,60504,60505,60506,60507,60508,60509,60510,60511,60512,60513,60514,60515,60516,60517,60518,60519,60520,60521,60522,60523,60524,60525,60526,60527,60528,7,701,d,z'

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
            'pageCount':'200',
            'pagesize':'50',
            'resultSearch':'false',
            'sxrqbegin':'',
            'sxrqend':'',
            'sxx':'有效',
            'xldj':'',
            'zdjg':self.id,
            'zlsxid':'',
        }
        return data

    def advanced_search_page(self,page):
        data = self.advanced_search_request_data(page)
        header = self.common_headers()
        html=requests.post(self.advanced_search_url,headers=header,data=data)
        if html.status_code==200:
            return html.text


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
    for page in range(1,3):
        html=a.advanced_search_page(page)
        print(html)
        rule=a.parse_law_id_rule()
        ids=a.parse_html(html,rule)
        id=a.parse_id(ids)
        print(id)



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

