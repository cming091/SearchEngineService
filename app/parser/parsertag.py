import re
import json
import time
from lxml.html import tostring
from lxml import etree
from datetime import datetime
from util import log
from pyquery import PyQuery as pq
from html import unescape
from util.utils import get_text


log = log.LogHandler(__name__)

_html = ''

class Saved:
    def __init__(self, elements):
        self.elements = elements

    def happyjuzi_star(self):
        doc = pq(self.elements)
        base = list(doc('.li_detial_personal').map(lambda i, e:pq(e).text()))
        base_dic ={}
        for item in base:
            if '\n' in item:
                base_dic[item.split('\n')[0]] = item.split('\n')[1]
            else:
                if item:
                    base_dic[item]=''
        intro = list(doc('.top_starindex p,.top_starindex h2').map(lambda i, e: pq(e).text()))
        if not intro:
            return
        return {'base':base_dic,'intro':intro}

    def douban_movie(self):
        doc = pq(self.elements)
        name = doc('#content h1').text()
        info = list(doc('#info').map(lambda i, e: pq(e).text()))[0].split('\n')
        base_dic = {}
        for i in info:
            if ':' in i:
                base_dic[i.split(':')[0]] = i.split(':')[1]
            elif '：' in i:
                base_dic[i.split('：')[0]] = i.split('：')[1]
            else:
                if i:
                    base_dic[i] = ''
        if not name:
            return
        return {'desc':base_dic,'name':name}

    def sina_sport(self):
        doc = pq(self.elements)
        info = list(doc('.page_con_b_lb').map(lambda i, e: pq(e)('li').map(lambda i, e:pq(e).text())))
        ctype = doc('.blk_03_r_b05_b02 h2').text()
        if not info:
            return
        return {'desc': info,'type':ctype}

    def wandoujia_game(self):
        data = json.loads(self.elements)
        data =data.get('data',{})
        html = data.get('content','')
        if not html:
            return
        doc = pq(html)
        #doc = pq(self.elements)
        info = list(doc('.card').map(lambda i, e: {'type':pq(e)('.tag-link').text(),'name':pq(e)('.app-desc .app-title-h2 a').attr('title')}))
        return info

    def ibagua_anchor(self):
        doc = pq(self.elements)
        name = doc('.iitoptitle h1').text()
        desc = list(doc('.zbinfo.l').map(lambda i, e:{pq(e)('strong').text():pq(e)('p').map(lambda i, e:pq(e).text())}))
        if not name:
            return
        return {'name': name,'desc':desc}

    def autohome_car(self):
        doc = pq(self.elements)
        info = list(doc('.list-dl').map(lambda i, e: {pq(e)('dt').text().strip():pq(e)('div').map(
            lambda i, e: pq(e)('div').text() if i%2==0 else pq(e)('a').text())}))
        base_dic = {}
        for item in info:
            for i,values in item.items():
                values = list(values)
                inner_dic = {}
                for num, j in enumerate(values):
                    if (':' in j) or ('：' in j):
                        inner_dic[j.strip(':|：')] = values[num+1]
                base_dic[i] =inner_dic
        ctype = doc('.fn-left.name').text()
        if not info:
            return
        return {'desc': base_dic,'type':ctype}

    def steampowered_game(self):
        data = json.loads(self.elements)
        html = data.get('results_html', '')
        if not html:
            return
        doc = pq(html)
        #doc = pq(self.elements)
        info = list(doc('.tab_item_content').map(lambda i, e: {'name':pq(e)('.tab_item_name').text(),'tag':pq(e)('.tab_item_top_tags .top_tag').text()}))
        return info

    def huanqiuweapon_guns(self):
        doc = pq(self.elements)
        info = list(doc('.picList li').map(lambda i, e: {'name':pq(e)('.name a').text(),'country':pq(e)('.country b i').text(),'category':pq(e)('.category').text()}))
        if not info:
            return
        return info

    def huanqiuweapon_term(self):
        doc = pq(self.elements)
        class1 = doc('.select_type1.current .title').text()
        class2 = list(doc('.select_type1.current .cur').map(lambda i, e:pq(e).text()))
        if not class2:
            class2 = doc('.select_type1.current .selectList b').text()
        else:
            class2=' '.join(class2)
        info = list(doc('.isList').map(lambda i, e:pq(e).map(lambda i, e:pq(e)('.con').text())))
        if not info:
            return
        return {'desc': info,'type':class1+' '+class2}

    def baikefenlei_history(self):
        doc = pq(self.elements)
        tag = doc('.grid-list.grid-list-spot .clearfix').text()
        info = list(doc('.grid-list.grid-list-spot li').map(
            lambda i, e: {'name': pq(e)('.list a').eq(0).text(), 'desc': pq(e)('.content-abstract').text(),
                          'text': pq(e)('.text').text()}))
        if not info:
            return
        return {'desc': info,'tag':tag}

    def ctrip_hotels(self):
        doc = pq(self.elements)
        city = doc('#city_tab .current').text()
        pro = doc('#province_tab .current').text()
        info = list(doc('.mkt_tab_list li').map(
            lambda i, e: pq(e)('.need_redate').text()))
        if not info:
            return
        return {'spots': info,'city':city,'pro':pro}

    def ctrip_ticker(self):
        doc = pq(self.elements)
        name = doc('.brief-box.clearfix .brief-right h2').text()
        desc = doc('.brief-box.clearfix .brief-right .spot-grade ').text()
        city = doc('.brief-box.clearfix .brief-right li span').eq(0).text()
        if not name:
            return
        return {'name': name,'city':city,'desc':desc}

    def meishi_caixi(self):
        doc = pq(self.elements)
        ctype = doc('.ui_title_wrap.clear .on a').attr('title')
        info = doc('#J_list li').map(
            lambda i, e: {'name':pq(e)('.detail h2 a').attr('title'),'info':pq(e)('.detail .subline a').text(),'desc':pq(e)('.detail .subcontent').text()})
        if not info:
            return
        return {'type': ctype,'list':info}

    def meishij_caixi(self):
        doc = pq(self.elements)
        ctype1 = doc('.listnav_dl_style1.w990.clearfix dt').eq(0).text()
        ctype = doc('.listnav_dl_style1 .current').text()
        info = doc('#listtyle1_list .listtyle1').map(
            lambda i, e: pq(e)('a').attr('title'))
        if not info:
            return
        return {'type1': ctype,'list':info,'type':ctype1}

    def sina_sport_detail(self):
        doc = pq(self.elements)
        info = list(doc('[cellpadding="3"] tr').map(
            lambda i, e: pq(e).text()))
        base_dic = {}
        for i in info:
            if '：' in i:
                base_dic[i.split('：')[0]] = i.split('：')[1]
            elif ':' in i:
                base_dic[i.split(': ')[0]] = i.split(': ')[1]
            else:
                if i:
                    base_dic[i] = ''
        if not info:
            return
        return base_dic

    def tostring(self, element):
        return tostring(element, encoding="utf-8", pretty_print=True).decode()


class Parser(Saved):
    slots = ("pattern", "result")

    def __init__(self, channel: str, html: str, url=''):
        self.channel = channel
        self.html = html
        self.url = url
        super(Parser, self).__init__(self.html)

    @property
    def result(self):
        method = getattr(self, self.channel)
        if not method():
            raise AttributeError("body is empty..")
        return method()



if __name__ == "__main__":
    parser = Parser("wandoujia_game", _html,'http://weapon.huanqiu.com/weaponlist/term/list_0_0_0_0_0_2')
    print(parser.result)
    #print(json.dumps(parser.result, ensure_ascii=False, indent=4))
