import requests as r
import lxml.html as html
# from bs4 import BeautifulSoup

class LawLibTool():
    def __init__(self):
        self.url ="http://law-lib.com"
        self.headers = self.headers()
        self.law_url_xpath ='//div[@class="index_605graycon clear2"]/ul/li/a/@href'
        self.law_title_xpath = '//div[@class="index_605graycon clear2"]/ul/li/a/@title'
        self.law_content_xpath ='//div[@class="content_view"]/text()'
        self.law_source_xpath ='//li[@class="fglys"]/text()'
        # self.save_path ='E:/PycharmProjects/legal_tools/lawlib_tool/law/'
        self.save_path ='E:\PycharmProjects\legal_tools\legal_tools\lawlib_tool\law'

    def main(self):
        req = self.site_req_by_get(self.url)
        urls=self.parse_main_site_req(req,self.law_url_xpath)
        titles =self.parse_main_site_req(req,self.law_title_xpath)
        full_urls= self.get_full_law_urls(urls)
        for full_url,title in zip(full_urls,titles):
            law_req = self.site_req_by_get(full_url)
            law_content= self.parse_main_site_req(law_req,self.law_content_xpath)
            save_path=self.save_path+'\\'+title+'.txt'
            for line in law_content:
                new_line= self.remove_tags(line)
                self.write_txt(save_path,new_line)
            self.write_txt(save_path,'url:'+full_url)

        #     for line in law_content:
        #         with open(title + '.txt', 'a+') as file:
        #             file.write(line+'\n')
        #     with open(title + '.txt', 'a+') as file:
        #         file.write('url：'+law_url)
        # # for url,title in zip(urls,titles):
        # #     print(title+':'+self.url+url)


    def headers(self):
        headers ={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Cookie':'UM_distinctid=15e4aaee1a13a0-0eaf8be97449d4-3a3e5f04-1fa400-15e4aaee1a26f8; ASPSESSIONIDSCCSBSDC=GNONNGHDNNHKJKEMFCJBEBHL; CNZZDATA2022442=cnzz_eid%3D1572228151-1504490350-%26ntime%3D1504664877; Hm_lvt_6c1bd80d51cc3038f01dd6bae3abeb22=1504573269,1504595521,1504657780,1504665073; Hm_lpvt_6c1bd80d51cc3038f01dd6bae3abeb22=1504668730',
        }

        return headers

    def site_req_by_get(self,url,headers=None):
        req= r.get(url,headers=headers)
        return req

    def site_req_by_post(self,url,headers=None,data=None):
        req= r.post(url,headers=headers,data=data)
        return req

    def parse_main_site_req(self,req,xpath):
        req.encoding = 'gb2312'#声明编码
        selector = html.fromstring(req.text)
        content =selector.xpath(xpath)
        return content

    def write_txt(self,path,content):
        with open(path,'a+') as file:
            file.write(content+'\n')

    def remove_tags(self,content):
        new_content = content.strip()
        return new_content

    def get_full_law_urls(self,urls):
        full_law_urls=[]
        for url in urls:
            full_law_urls.append(self.url+url)
        return full_law_urls




if __name__ =='__main__':
    a=LawLibTool()
    a.main()












