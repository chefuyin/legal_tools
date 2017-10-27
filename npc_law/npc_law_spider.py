import random,requests,re
import lxml.html
from lxml.html import etree
import time
import pyquery



class NpcLawSpider():
    def __init__(self):
        self.request_url='http://law.npc.gov.cn/FLFG/getAllList.action'
        self.half_law_url='http://law.npc.gov.cn/FLFG/flfgByID.action?flfgID='
        self.index='http://law.npc.gov.cn/FLFG/'
        self.check_url='http://law.npc.gov.cn/FLFG/getAllList.action?SFYX=%E6%9C%89%E6%95%88&zlsxid=11&bmflid=&zdjg=&txtid=&resultSearch=false&lastStrWhere=&keyword=&pagesize=50'
    # 导入数据集并随机获取一个User-Agent
    def random_user_agent(self):
        user_agent_list = []
        f = open('user_agent.txt', 'r')
        for date_line in f:
            user_agent_list.append(date_line.replace('\n', ''))
        user_agent = random.choice(user_agent_list)
        return user_agent

    # def index_page_data(self):
    #     'goMore(zlsx, bmfl, zdjg, txtid)'
    #

    def index_page(self):
        user_agent = self.random_user_agent()
        '''参数引入及头信息'''
        if len(user_agent) < 10:
            user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'
        # 此处修改头字段,
        headers = {
            "User-Agent": user_agent,
            }
        html=requests.get(self.index,headers=headers)
        if html.status_code==200:
            return html.text

    def parse_index_page_rule(self):
        rule1='//div[@class="nav"]/a/@href'
        rule2='//a[@class="relative"]/div/span/@onclick'
        rule3='//ul[@class="threecloumntitle"]/li/a/@href'

        return rule3


    #generate request headers
    def request_headers(self):
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

    #input page and request data to get list page,
    def list_page(self,data):
        data=data
        headers=self.request_headers()
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
        law_info_dict = self.translate_to_english(law_info)
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
    def translate_to_english(self,text_list):
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
    html=a.index_page()
    print(html)
    rule=a.parse_index_page_rule()
    result=a.parse_html(html,rule)
    print(result)


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

