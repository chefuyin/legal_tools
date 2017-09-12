import os
import re


class JudgementAnalysis():
    def __init__(self):
        self.path='E:\PycharmProjects\judgement_analysis\judgement_samples'


    def main(self):
        file_list = os.listdir(self.path)
        for file in self.get_file_paths(file_list):
            with open(file,'r') as f:
                lines = f.readlines()
                clear_lines =self.get_clear_text(lines)
                court = self.get_re_court(clear_lines)
                agent =self.get_re_agent(clear_lines)
                plantiff = self.get_re_plantiff(clear_lines)
                defendant = self.get_re_defendant(clear_lines)
                judgement_number = self.get_re_judgement_number(clear_lines)
                print(judgement_number)
                # print(court)
                # print(plantiff)
                # print(defendant)
                # print(agent)
                print('\n')






    def get_file_paths(self,file_list):
        new=[]
        for file in file_list:
            new.append(self.path+'\\'+file)
        return new


    def get_clear_text(self,text_list):
        if type(text_list) == type([]):
            new=[]
            for text in text_list:
                new.append(text.strip().replace(' ',''))
            return new
        else:
            print('请传入文本列表')

    def get_re_court(self,text_list):
        court = []
        for text in text_list:
            pattern = re.compile(r'\A.*人民法院*.\Z')
            match = pattern.search(text)
            if match != None:
                court.append(match.group())
        return court

    def get_re_judgement_number(self,text_list):
        judgement_number =[]
        for text in text_list:
            pattern = re.compile(r'\A（(.*)号\Z')
            match = pattern.search(text)
            if match !=None:
                judgement_number.append(match.group())
        return judgement_number


    def get_re_plantiff(self,text_list):
        plantiff =[]
        for text in text_list:
            pattern = re.compile(r'原告：(.*)')
            match= pattern.match(text)
            if match!=None:
                result =match.group().split('。')[0]
                plantiff.append(result)
        return plantiff

    def get_re_defendant(self,text_list):
        defendant =[]
        for text in text_list:
            pattern = re.compile(r'被告：(.*)')
            match = pattern.match(text)
            if match != None:
                result = match.group().split('。')[0]
                defendant.append(result)
        return defendant

    def get_re_agent(self,text_list):
        agent =[]
        for text in text_list:
            pattern =re.compile(r'代理人(.*)：(.*)|诉讼代理人(.*)：(.*)|法定代理人(.*)：(.*)|委托代理人(.*)：(.*)')
            match =pattern.search(text)
            if match !=None:
                agent.append(match.group())
        return agent







if __name__ =='__main__':
    a=JudgementAnalysis()
    a.main()











