import random,requests,re
import lxml.html
from lxml.html import etree



class NpcLawSpider():
    def __init__(self):
        self.request_url='http://law.npc.gov.cn/FLFG/getAllList.action'

    def get_request(self,page):
        user_agent=self.random_user_agent()
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
            'Referer': 'http://law.npc.gov.cn/FLFG/getAllList.action'
        }
        data={
            'pagesize': '50',
            'ispage': '1',
            'pageCount': '24',
            'curPage': page,
            'SFYX': '有效',
            'zlsxid': '02',
            'fenleigengduo': '',
            'bmflid':'',
            'zdjg':'',
            'txtid':'',
            'resultSearch':'false',
            'lastStrWhere': '法律',
            'keyword': '法律',
        }
        try:
            url = self.request_url
            html = requests.post(url, headers=headers, data=data,timeout=20).text
            # print html
            return html
        except Exception as e:
            print(Exception, e)
            return -1

        # 导入数据集并随机获取一个User-Agent
    def random_user_agent(self):
        user_agent_list = []
        f = open('user_agent.txt', 'r')
        for date_line in f:
            user_agent_list.append(date_line.replace('\n', ''))
        user_agent = random.choice(user_agent_list)
        return user_agent

    def parse_html(self,html):
        selector = lxml.html.fromstring(html)
        info=selector.xpath('//td[@class="td"]/a/@href')
        return info

    def parse_id(self,id_list):
        pattern=re.compile(r"'(.*?)'")
        for i in id_list:
            match= pattern.findall(i)
            if match:
                id=match[0]
                law_url='http://law.npc.gov.cn/FLFG/flfgByID.action?flfgID='+id
                print(law_url)

    def parse_law_content_html(self,url):
        headers={
            'User-Agent':self.random_user_agent()
        }
        html=requests.get(url,headers=headers).text
        selector=lxml.html.fromstring(html)
        law_info=selector.xpath('//table/tr[td]')
        law_title=selector.xpath('//div[@class="bt"]/text()')[0].strip()
        law_discription=selector.xpath('//div[@style="text-indent: 2em;"]/text()')[0].strip()
        tree=etree.HTML(html)
        law_content=tree.xpath('//div[@class="nr"]/div[3]')
        new_data = {}
        replace_words={
            '资料属性：':'file_type',
            '部门分类：': 'classification',
            '制定机关：': 'department',
            '颁布文号：': 'file_number',
            '颁布日期：': 'publish_date',
            '施行日期：': 'enforcement_date',
            '时 效 性：': 'valid_invalid',
            '失效日期：': 'invalid_date',
        }
        for row in law_info:
            info_list=[]
            for i in row.itertext():
                # if i.strip()!='':
                i=i.strip()
                for k,v in replace_words.items():
                    if k==i:
                        i=v
                info_list.append(i)

                # info_list.append(i.strip())
            if len(info_list)==9:
                data={
                    info_list[1]:info_list[3],
                    info_list[5]: info_list[7],
                }
                # print(data)
                new_data.update(data)

            elif len(info_list)==5:
                data = {
                    info_list[1]: info_list[3],
                }
                # print(data)
                new_data.update(data)
        law_content_list=[]
        for paras in law_content:
            para=str(paras.xpath('string(.)'))
            list=para.split()
            law_content_list=law_content_list+list
        law_content_lines='\r\n'.join(law_content_list)
        new_data.update({'law_title': law_title},)
        new_data.update({'law_discription': law_discription})
        new_data.update({'law_content_lines':law_content_lines})
        print(new_data)












if __name__== '__main__':
    a=NpcLawSpider()
    url = 'http://law.npc.gov.cn/FLFG/flfgByID.action?flfgID=36384972'
    a.parse_law_content_html(url)
    # for i in range(1,3):
    #     result=a.get_request(str(i))
    #     # print(result)
    #     if result==-1:
    #         print('error')
    #     else:
    #         ids=a.parse_html(result)
    #         a.parse_id(ids)

