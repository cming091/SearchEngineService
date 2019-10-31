# -*- coding: utf-8 -*-

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
from util.utils import zcompress

log = log.LogHandler(__name__)

_html = """

<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="utf-8">
    <link rel="dns-prefetch" href="//h5.sinaimg.cn">
    <link rel="icon" sizes="any" mask href="//h5.sinaimg.cn/upload/2015/05/15/28/WeiboLogoCh.svg" color="black">
    <link rel="apple-touch-icon" href="https://h5.sinaimg.cn/upload/2017/03/16/16/icon.png">
    <meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
    <meta name="format-detection" content="telephone=no">
    <title>微博</title>
    <meta content="随时随地发现新鲜事！微博带你欣赏世界上每一个精彩瞬间，了解每一个幕后故事。分享你想表达的，让全世界都能听到你的心声！" name="description">
    <meta name="theme-color" content="#F3F3F3">
    <link rel="amphtml" href="https://media.weibo.cn/article/amp?id=2309404319715983019118">        <link rel="stylesheet" href="//h5.sinaimg.cn/marvel/v1.4.0/css/lib/base.css">
    <link rel="stylesheet" href="//h5.sinaimg.cn/marvel/v1.4.0/css/card/cards.css">
            <script>!function(e){var a,i=navigator.userAgent.toLowerCase(),n=document.documentElement,t=parseInt(n.clientWidth);if(/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)||i.indexOf("like mac os x")>0){var s=/os [\d._]*/gi,o=i.match(s);a=(o+"").replace(/[^0-9|_.]/gi,"").replace(/_/gi,".")}var r=a+"";"undefined"!=r&&r.length>0&&(a=parseInt(r),a>=8&&(375==t||667==t||320==t||568==t||480==t)?n.className="iosx2":(a>=8&&414==t||736==t)&&(n.className="iosx3")),/(Android)/i.test(navigator.userAgent)&&(n.className="android")}(window);</script>
        <style>html, body, #app {height: 100%;}[v-cloak] {display: none;}</style>
    <link href="//h5.sinaimg.cn/m/v8/css/app.a37ad339.css" rel="stylesheet">
        </head>
<body>
        <div id="app" class="m-container-max">
        <router-view></router-view>
        <mv-modal></mv-modal>
    </div>
            <script>
        var config = {
            env: 'prod',
            st: '',
            login: [][0],
            uid: '',
            pageConfig: [null][0] || {},
            wm: '',
            preferQuickapp: 0,
            version: 'v1.14.59',
            url: location.href.split('#')[0]
        };
        var $render_data = [{
    "object_id": "1022:2309404319715983019118",
    "title": "【周末娱乐指南】关晓彤探索乾隆最爱女儿 《蜘蛛侠：平行宇宙》热映",
    "summary": "本周娱乐指南精彩连连，等你来看！",
    "url": "https://media.weibo.cn/article?id=2309404319715983019118",
    "status": "1",
    "object_type": "article",
    "article_type": "top_article",
    "content": "<h1>​【综艺】​</h1><img src=\"https://wx3.sinaimg.cn/wap720/61e7f4aaly1fyecwviy5dj20hs0a0wlv.jpg\" alt=\"《上新了•故宫》关晓彤扮十公主探索乾隆最宠爱的女儿\"/><div class=\"hl-img-desc\">《上新了•故宫》关晓彤扮十公主探索乾隆最宠爱的女儿</div><img src=\"https://wx3.sinaimg.cn/wap720/61e7f4aaly1fyecwwqdf2j20hr0kr4mg.jpg\" alt=\"《锋味》谢霆锋宋茜同游布拉格\"/><div class=\"hl-img-desc\">《锋味》谢霆锋宋茜同游布拉格</div><p>12月21日（周五）</p><p>20:00 爱奇艺《国风美少年》（鞠婧祎同门师妹遇危机）</p><p>20:00 湖南卫视《声入人心》（阿云嘎郑云龙、王晰周深默契开唱）</p><p>21:05北京卫视《上新了•故宫》（关晓彤扮十公主探索乾隆最宠爱的女儿）</p><p>21:10 浙江卫视《梦想的声音》（谭维维献“导演”首秀 林俊杰改编《像我这样的人》）</p><p>22:00 湖南卫视《亲爱的客栈》（王鹤棣沈月吴希泽重聚）</p><p>22:00 江苏卫视《最美的时光》（吴尊打篮球意外受伤）</p><p> </p><p>12月22日（周六）</p><p>12:00 芒果TV《野生厨房》（杨芸晴大跳魔性采茶舞）</p><p>12:00 优酷《挑战吧太空》（朱正廷谈男人关键词吴宣仪被恐高支配）</p><p>20:00 腾讯 《即刻电音》（迎团队突围战  大张伟泪洒现场）</p><p>20:20 湖南卫视《快乐大本营》（许魏洲盛一伦彭昱畅等白衣少年集结）</p><p>20:30 东方卫视《没想到吧》（萧敬腾劈叉唱《王妃》 池子在线相亲自我吐槽）</p><p>22:00 浙江卫视《锋味》（谢霆锋宋茜同游布拉格）</p><p><br/></p><p>12月23日（周日）</p><p>12:00 优酷《完美的餐厅》（尤长靖做创意菜佘诗曼吃出初恋感觉）</p><p>19:30 CCTV-3《国家宝藏》（宋佳化身国宝守护人 动情演绎前世传奇）</p><p>20:00 腾讯《吐槽大会》（周笔畅回应超女三强被比较 曝杨幂是自己粉丝）</p><p>21:00 东方卫视《下一站传奇》（吴亦凡缺席录制郑恺代班）</p><p>21:10 江苏卫视《蒙面唱将猜猜猜》（猜评团大发力 《蒙面》再现双揭面）</p><p>22:00 湖南卫视《天天向上》（“双云组合”阿云嘎郑云龙友爱“互怼”）</p><h1>【电影】</h1><img src=\"https://wx1.sinaimg.cn/wap720/61e7f4aaly1fyeeihqgy0j20c80hd4f4.jpg\" alt=\"《蜘蛛侠：平行宇宙》\"/><div class=\"hl-img-desc\">《蜘蛛侠：平行宇宙》</div><p><b>《蜘蛛侠：平行宇宙》</b></p><p>导演: 鲍勃·佩尔西凯蒂 / 彼得·拉姆齐 / 罗德尼·罗斯曼</p><p>主演: 沙梅克·摩尔 / 杰克·约翰逊 / 海莉·斯坦菲尔德 / 马赫沙拉·阿里 / 布莱恩·泰里·亨利 </p><p>类型: 动作 / 科幻 / 动画 / 冒险​</p><p>简介：蜘蛛侠不止一个！漫威超英动画巨制《蜘蛛侠：平行宇宙》将经典漫画与CGI技术完美呈现，讲述了普通高中生迈尔斯·莫拉斯如何师从蜘蛛侠彼得·帕克，成长为新一代超级英雄的故事。影片中迈尔斯和从其它平行宇宙中穿越而来的彼得、女蜘蛛侠格温、暗影蜘蛛侠、潘妮·帕克和蜘猪侠集结成团，六位蜘蛛侠首次同框大银幕，对抗蜘蛛侠宇宙最强反派。 ​</p><img src=\"https://wx2.sinaimg.cn/wap720/61e7f4aaly1fyedcyfl15j20u0160npf.jpg\" alt=\"《天气预爆》\"/><div class=\"hl-img-desc\">《天气预爆》</div><p><b>《天气预爆》​</b></p><p>导演: 肖央</p><p>主演: 肖央 / 杜鹃 / 常远 / 小沈阳 / 岳云鹏 </p><p>类型: 喜剧 / 奇幻​</p><p>简介：号称“自杀干预大师”的心理医生马乐，专靠别人生活的不如意发财，一日天降“寿星”砸中了马乐，误吸仙气的马乐被告知世界正在崩溃边缘，只有找齐被贬入凡间的风雨雷电四神才能改变一切，于是众神与凡人一同踏上了一段爆笑奇幻又紧张刺激的旅程....​</p><img src=\"https://wx1.sinaimg.cn/wap720/61e7f4aaly1fyed34dn74j20u0160hdu.jpg\" alt=\"《叶问外传：张天志》\"/><div class=\"hl-img-desc\">《叶问外传：张天志》</div><p><b>《叶问外传：张天志》</b></p><p>导演: 袁和平</p><p>主演: 张晋 / 戴夫·巴蒂斯塔 / 柳岩 / 杨紫琼 / 托尼·贾 </p><p>类型: 动作<br/></p><p>简介：作为《叶问》系列影片，电影《叶问外传：张天志》延续了《叶问3》的故事，讲述了同为咏春传人的张天志在比武惜败叶问后，决意放下功夫、远离江湖纷争，但面对接踵而至的连番挑衅，面对家国大义遭受的恶意侵犯，决定重拾咏春惩戒毒贩、“以武之道”捍卫民族道义尊严的故事。</p><img src=\"https://wx4.sinaimg.cn/wap720/61e7f4aaly1fyed5yzckij20nr0xcb2a.jpg\" alt=\"《武林怪兽》\"/><div class=\"hl-img-desc\">《武林怪兽》</div><p><b>《武林怪兽》</b><br/></p><p>导演: 刘伟强</p><p>主演: 古天乐 / 陈学冬 / 郭碧婷 / 包贝尔 / 王太利 </p><p>类型: 喜剧 / 奇幻 / 武侠<br/></p><p>​简介：屈服？反转？逆套路？这是一个超乎你想象的武林爆笑故事！东厂悬赏价值三万两的奶凶怪兽，让各方异士垂涎不已。一波杂烩大侠们临时组队，做起了一夜暴富的白日梦，古天乐郭碧婷貌合神离、陈学冬欺软怕硬、周冬雨威逼利诱、潘斌龙孔连顺颜值狙击，各路大侠花样百出！到底谁能走向人生巅峰呢？</p><img src=\"https://wx2.sinaimg.cn/wap720/61e7f4aaly1fyecztn2clj20u0180qv7.jpg\" alt=\"《大路朝天》\"/><div class=\"hl-img-desc\">《大路朝天》</div><p>​<b>《大路朝天》</b></p><p>导演: 苗月</p><p>主演: 李保田 / 陈瑾 / 巴登西绕 / 张政勇 / 孙敏 </p><p>类型: 剧情​​</p><p>简介：在社会主义道路上，中国公路的发展和人民命运紧密相连的。《大路朝天》以四川公路建设为切口，以成雅高速、雅西高速、雅康高速建设为题材，通过讲述祖孙三代路桥工人伴随改革开放40年经历的命运和情感故事，折射出时代发展与变迁。 </p><h1>【演出】​</h1><img src=\"https://wx2.sinaimg.cn/wap720/61e7f4aaly1fyedirhagmj209g0cq44l.jpg\" alt=\"2018德云社北京相声大会——新街口德云社\"/><div class=\"hl-img-desc\">2018德云社北京相声大会——新街口德云社</div><p><br/></p><p>北京​</p><p><b>2018德云社北京相声大会——新街口德云社</b><br/></p><p>时间：常年</p><p>地点：德云社相声大会新街口剧场</p><p><br/></p><p><b>开心麻花2019爆笑贺岁舞台剧《谈判专家》</b><br/></p><p>时间：2018.12.05-12.31</p><p>地点：世纪剧院</p><p><br/></p><p><b>730匣子X开心麻花联合出品高糖音乐喜剧《恋爱吧！人类》</b><br/></p><p>时间：2018.12.21-12.31</p><p>地点：地质礼堂剧场</p><p><br/></p><p>上海</p><p><b>音乐剧《芝加哥》上海站</b><br/></p><p>时间：2018.12.20-2019.01.13</p><p>地点：美琪大戏院</p><p><br/></p><p><b>林肯爵士乐上海中心Dominick Farinacci Group week1</b><br/></p><p>时间：2018.12.18-12.25</p><p>地点：林肯爵士乐上海中心</p><p><br/></p><p><b>开心麻花爆笑舞台剧《乌龙山伯爵》</b><br/></p><p>时间：2018.12.11-2019.01.06</p><p>地点：虹桥艺术中心</p><p><br/></p><p>广州</p><p><b>话剧《我是月亮》</b><br/></p><p>时间：2018.12.20-12.22</p><p>地点：正佳演艺剧院</p><p><br/></p><p><b>黎星工作室：舞蹈剧场《大饭店》</b><br/></p><p>时间：2018.12.21-12.22</p><p>地点：广州友谊剧院</p><p><br/></p><p><b>俄罗斯莫斯科芭蕾舞团•新春贺岁 经典芭蕾舞剧《天鹅湖》</b><br/></p><p>时间：2018.12.23 19:30</p><p>地点：广东演艺中心大剧院</p><p><br/></p><h1>本周福利大放送！！！​</h1><img src=\"https://wx4.sinaimg.cn/wap720/61e7f4aaly1fyedyvnxy7j20u013ze84.jpg\" alt=\"《格林德沃之罪》电影周边\"/><div class=\"hl-img-desc\">《格林德沃之罪》电影周边</div><img src=\"https://wx2.sinaimg.cn/wap720/61e7f4aaly1fyedym0ugfj20u013zb2c.jpg\" alt=\"《蜘蛛侠：平行宇宙》电影周边\"/><div class=\"hl-img-desc\">《蜘蛛侠：平行宇宙》电影周边</div><img src=\"https://wx3.sinaimg.cn/wap720/61e7f4aaly1fyedyz0rlkj212w0t6b2a.jpg\" alt=\"海清2019台历、经超签名小浪公仔\"/><div class=\"hl-img-desc\">海清2019台历、经超签名小浪公仔</div><p>《格林德沃之罪》电影周边；《蜘蛛侠：平行宇宙》电影周边；海清2019台历、经超签名小浪公仔等你来拿！</p><p><b><b><b>​</b></b></b>​​​</p>",
    "use_new_readcount_v3": 1,
    "biz_exempt": 1,
    "read_count_num": 932851,
    "target_url": "https://media.weibo.cn/article?id=2309404319715983019118",
    "pic_map": {
        "https://wx3.sinaimg.cn/large/61e7f4aaly1fyecwviy5dj20hs0a0wlv.jpg": "61e7f4aaly1fyecwviy5dj20hs0a0wlv",
        "https://wx3.sinaimg.cn/large/61e7f4aaly1fyecwwqdf2j20hr0kr4mg.jpg": "61e7f4aaly1fyecwwqdf2j20hr0kr4mg",
        "https://wx1.sinaimg.cn/large/61e7f4aaly1fyeeihqgy0j20c80hd4f4.jpg": "61e7f4aaly1fyeeihqgy0j20c80hd4f4",
        "https://wx2.sinaimg.cn/large/61e7f4aaly1fyedcyfl15j20u0160npf.jpg": "61e7f4aaly1fyedcyfl15j20u0160npf",
        "https://wx1.sinaimg.cn/large/61e7f4aaly1fyed34dn74j20u0160hdu.jpg": "61e7f4aaly1fyed34dn74j20u0160hdu",
        "https://wx4.sinaimg.cn/large/61e7f4aaly1fyed5yzckij20nr0xcb2a.jpg": "61e7f4aaly1fyed5yzckij20nr0xcb2a",
        "https://wx2.sinaimg.cn/large/61e7f4aaly1fyecztn2clj20u0180qv7.jpg": "61e7f4aaly1fyecztn2clj20u0180qv7",
        "https://wx2.sinaimg.cn/large/61e7f4aaly1fyedirhagmj209g0cq44l.jpg": "61e7f4aaly1fyedirhagmj209g0cq44l",
        "https://wx4.sinaimg.cn/large/61e7f4aaly1fyedyvnxy7j20u013ze84.jpg": "61e7f4aaly1fyedyvnxy7j20u013ze84",
        "https://wx2.sinaimg.cn/large/61e7f4aaly1fyedym0ugfj20u013zb2c.jpg": "61e7f4aaly1fyedym0ugfj20u013zb2c",
        "https://wx3.sinaimg.cn/large/61e7f4aaly1fyedyz0rlkj212w0t6b2a.jpg": "61e7f4aaly1fyedyz0rlkj212w0t6b2a"
    },
    "scheme_url": "sinaweibo://article?object_id=1022:2309404319715983019118",
    "userinfo": {
        "id": 1642591402,
        "idstr": "1642591402",
        "screen_name": "新浪娱乐",
        "name": "新浪娱乐",
        "description": "新浪娱乐",
        "profile_image_url": "https://tva4.sinaimg.cn/crop.0.0.440.440.1024/61e7f4aajw8ev79nvbx40j20c80c875l.jpg",
        "cover_image_phone": "https://tva1.sinaimg.cn/crop.0.0.640.640.640/549d0121tw1egm1kjly3jj20hs0hsq4f.jpg",
        "gender": "f",
        "followers_count": "2613万",
        "friends_count": 3369,
        "following": false,
        "verified": true,
        "verified_type": 3,
        "avatar_large": "http://tva4.sinaimg.cn/crop.0.0.440.440.180/61e7f4aajw8ev79nvbx40j20c80c875l.jpg",
        "avatar_hd": "http://tva4.sinaimg.cn/crop.0.0.440.440.1024/61e7f4aajw8ev79nvbx40j20c80c875l.jpg",
        "verified_reason": "新浪娱乐为你带来最新鲜的娱乐资讯",
        "follow_me": false,
        "vicon": "bluev",
        "att": 0,
        "friendships_relation": 0
    },
    "created_at": "2018.12.21",
    "follow_button": {
        "skip_format": 1,
        "sub_type": 0,
        "type": "follow",
        "name": "加关注",
        "params": {
            "uid": 1642591402
        }
    },
    "flow": {
        "flow_type": 1,
        "flow_title": "推荐阅读"
    },
    "sharecontent": {
        "description": "",
        "pic_url": ""
    },
    "read_count": "93万+",
    "page_id": "2309404319715983019118",
    "article_version": 2,
    "scheme": "sinaweibo://article?object_id=1022:2309404319715983019118",
    "article_fingerprinting": "b8fd2e46ae5ff84c2f4264f162319496",
    "refresh_placeholder_pic": "https://h5.sinaimg.cn/upload/1000/48/2018/11/19/iPhone.png",
    "edit_scheme": "sinaweibo://articleedit?oid=1022:2309404319715983019118",
    "created_time": "2018-12-21T17:20:09Z",
    "mblog": {
        "id": "4319715981734631",
        "reposts_count": 380,
        "comments_count": 739,
        "attitudes_count": 464,
        "scheme_wb": "sinaweibo://detail?mblogid=4319715981734631&luicode=10000370"
    },
    "writers": {
        "screen_name": "新浪娱乐"
    },
    "isMyself": 0,
    "liked": 0,
    "reward_users": [],
    "ok": 1,
    "msg": "文章内容获取成功",
    "exp": {
        "uid": null,
        "isLogin": false,
        "loginUrl": "https://passport.weibo.cn/signin/welcome?entry=mweibo&r=https%3A%2F%2Fmedia.weibo.cn%2Farticle%3Fobject_id%3D1022%253A2309404319715983019118%26extparam%3Dlmid--4319715981734631%26luicode%3D10000011%26lfid%3D2303190002_445_1642591402_WEIBO_ARTICLE_LIST_DETAIL%26id%3D2309404319715983019118%26sudaref%3Dm.weibo.cn%26display%3D0%26retcode%3D6102",
        "wx_callback": "https://passport.weibo.com/othersitebind/authorize?entry=h53rdlanding&site=qq&callback=http%3A%2F%2Fmedia.weibo.cn%2Farticle%3Fobject_id%3D1022%253A2309404319715983019118%26extparam%3Dlmid--4319715981734631%26luicode%3D10000011%26lfid%3D2303190002_445_1642591402_WEIBO_ARTICLE_LIST_DETAIL%26id%3D2309404319715983019118%26sudaref%3Dm.weibo.cn%26display%3D0%26retcode%3D6102",
        "wx_authorize": "https://passport.weibo.com/othersitebind/authorize?site=weixin&entry=sinawap&type=normal&callback=http%3A%2F%2Fmedia.weibo.cn%2Farticle%3Fobject_id%3D1022%253A2309404319715983019118%26extparam%3Dlmid--4319715981734631%26luicode%3D10000011%26lfid%3D2303190002_445_1642591402_WEIBO_ARTICLE_LIST_DETAIL%26id%3D2309404319715983019118%26sudaref%3Dm.weibo.cn%26display%3D0%26retcode%3D6102",
        "passport_login_url": "https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fmedia.weibo.cn%2Farticle%3Fobject_id%3D1022%253A2309404319715983019118%26extparam%3Dlmid--4319715981734631%26luicode%3D10000011%26lfid%3D2303190002_445_1642591402_WEIBO_ARTICLE_LIST_DETAIL%26id%3D2309404319715983019118%26sudaref%3Dm.weibo.cn%26display%3D0%26retcode%3D6102",
        "deviceType": "Mac",
        "browserType": "Chrome",
        "online": true,
        "wm": null,
        "st": false,
        "isInClient": 0,
        "isWechat": 0,
        "hideHeaderBanner": 0,
        "request_key": "891e9c679086af405acc1e0d76387db7"
    },
    "rewards": {
        "version": "7ed12affaecce88a",
        "rewardComponent": "seller=1642591402&bid=1000207805&oid=1022:2309404319715983019118&share=1&access_type=mobileLayer&sign=aab125c16c22ecf7a8c68d2d394fb220",
        "extendParam": "type=layer&extparam=lmid--4319715981734631",
        "displayPayRead": 0,
        "isreward": 1
    },
    "wxConfig": "",
    "config": {
        "id": "1022:2309404319715983019118",
        "extparam": "lmid--4319715981734631",
        "cover_img": "https://wx4.sinaimg.cn/wap720/61e7f4aaly1fyeeq8jlcgj20m20cee3p.jpg"
    },
    "callUinversalLink": true,
    "callWeibo": true,
    "amphtml": "<link rel=\"amphtml\" href=\"https://media.weibo.cn/article/amp?id=2309404319715983019118\">",
    "scheme_user_profile": "sinaweibo://userinfo?uid=1642591402&luicode=10000370",
    "home_scheme": "sinaweibo://gotohome?luicode=10000370",
    "scheme_wb": "sinaweibo://detail?mblogid=4319715981734631&luicode=10000370",
    "article_scheme": "sinaweibo://article?object_id=1022:2309404319715983019118&luicode=10000370",
    "reward_scheme": "sinaweibo://article?object_id=1022:2309404319715983019118&pos=1&anchor=reward&luicode=10000370",
    "pay_scheme": "sinaweibo://article?object_id=1022:2309404319715983019118&pos=1&anchor=pay&luicode=10000370"
}][0] || {};
    </script>
    <script type="text/javascript">!function(e){function n(r){if(t[r])return t[r].exports;var o=t[r]={i:r,l:!1,exports:{}};return e[r].call(o.exports,o,o.exports,n),o.l=!0,o.exports}var r=window.webpackJsonp;window.webpackJsonp=function(t,c,a){for(var f,i,u,d=0,s=[];d<t.length;d++)i=t[d],o[i]&&s.push(o[i][0]),o[i]=0;for(f in c)Object.prototype.hasOwnProperty.call(c,f)&&(e[f]=c[f]);for(r&&r(t,c,a);s.length;)s.shift()();if(a)for(d=0;d<a.length;d++)u=n(n.s=a[d]);return u};var t={},o={46:0};n.e=function(e){function r(){f.onerror=f.onload=null,clearTimeout(i);var n=o[e];0!==n&&(n&&n[1](new Error("Loading chunk "+e+" failed.")),o[e]=void 0)}var t=o[e];if(0===t)return new Promise(function(e){e()});if(t)return t[2];var c=new Promise(function(n,r){t=o[e]=[n,r]});t[2]=c;var a=document.getElementsByTagName("head")[0],f=document.createElement("script");f.type="text/javascript",f.charset="utf-8",f.async=!0,f.timeout=12e4,n.nc&&f.setAttribute("nonce",n.nc),f.src=n.p+"js/"+e+"."+{0:"865dbff5",1:"c6339c72",2:"0c43d811",3:"483b104f",4:"51480cae",5:"2f2a9d37",6:"ece54313",7:"61d844af",8:"38ba9abf",9:"5e69a019",10:"497fc3f5",11:"1bd80c67",12:"46ba295a",13:"dca49150",14:"866926d7",15:"aa748a07",16:"8fa3379f",17:"c6cf5833",18:"94c85260",19:"379d999d",20:"199b5dbd",21:"ef925b97",22:"51d23086",25:"78ae6a9e",26:"0b92fdc5",27:"ce5f15fc",28:"d0a69e3c",29:"f0282e63",30:"e2b4e6f7",31:"a2226670",32:"47c67883",33:"d59412af",34:"2de5c489",35:"919d8986",36:"107de634",37:"173c53e4",38:"1371f37b",39:"ab970676",40:"87854b5b",41:"ca969307",42:"9fbaf223",43:"d384ef55",44:"c901849f",45:"96e60c8b"}[e]+".js";var i=setTimeout(r,12e4);return f.onerror=f.onload=r,a.appendChild(f),c},n.m=e,n.c=t,n.d=function(e,r,t){n.o(e,r)||Object.defineProperty(e,r,{configurable:!1,enumerable:!0,get:t})},n.n=function(e){var r=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(r,"a",r),r},n.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)},n.p="//h5.sinaimg.cn/m/v8/",n.oe=function(e){throw console.error(e),e}}([]);</script>
    <script type="text/javascript" src="//h5.sinaimg.cn/m/v8/js/vendor.c69866be.js"></script>
    <script type="text/javascript" src="//h5.sinaimg.cn/m/v8/js/app.722d375c.js"></script>
    <script>
        window.__wb_performance_data = {
            v: 'v8',
            m: 'mainsite',
            pwa: 0
        }
    </script>
        <script src="https://h5.sinaimg.cn/upload/1005/16/2017/11/30/wbp.js" id="__wb_performance_log"
            data-rate="0.1"></script>
</body>

</html>
"""


class Channel:
    BAIJIAHAO_BAIDU_COM = [('//*[@class="article-title"]/h2/text() |'
             ' //*[@class="author-name"]/text() |  '
#             '//*[@class="article-source"]/span[@class="source"]/text() | '
#             '//div[@class="article-desc clearfix"]/div[@class="author-txt"]/p[@class="author-name"]/text()|'
             '//*[@class="article-source"]/span[@class="date"]/text() |'
             '//*[@class="article-source"]/span[@class="time"]/text() |'
             '//*[@class="article-content"]| //*[@id="content-container"]/@data-extralog'), "baijiahao"]
    MP_WEIXIN_QQ_COM = [('//*[@id="js_profile_qrcode"]/div/p[1]/span/text() | //*[@id="activity-name"]/text() | //*[@id="js_profile_qrcode"]/div/strong/text() | //*[@id="js_profile_qrcode"]/div/p[1]/label/text() | //*[@id="publish_time"]/text() | //*[@id="js_content"]'), "weixin"]
    WEMEDIA_IFENG_COM = [('//*[@class="yc_tit"]/h1/text() | //*[@class="clearfix"]/a[2] |  //*[@class="clearfix"]/span/text() | //*[@class="yc_con_txt"]'), 'ifeng']
    WWW_TOUTIAO_COM = [('//*[@class="article-title"]/text() | //*[@class="user-card-name"]/a |  //*[@class="article-sub"]/span[2]/text() | //*[@class="article-content"]'), 'toutiao_detail']
    WWW_SOHU_COM = [('//div[@class="text"]/div[@class="text-title"]/h1/text() | //*[@id="news-time"]/@data-val | //*[@class="user-info"]/h4/a |  //*[@class="article"]'), "sohu_detail"]
    KUAIBAO_QQ_COM = [('//*[@class="title"]/text()|//*[@class="time"]/text()|//*[@class="author"]/text()|//*[@class="content-box"]') ,'news_qq']
    DY_163_COM = [('//*[@class="article_title"]/h2/text() | //*[@class="time"]/span[not(@class="point")]/text() |  //*[@id="content"]'), "dy_163_com"]
    WWW_YIDIANZIXUN_COM = [('//*[@class="left-wrapper"]/h2/text() | //*[@class="content-bd"]'), 'yidianzixun']
    WWW_SOHU_ACCOUNT = [
        ('//h3[@class="article-title"]/text() |  //*[@class="l time"]/text() | //*[@class="l clearfix"]/a[2]/text() | //*[@class="article-text"]'), "sohu_account"
    ]
    MEDIA_WEIBO_CN = ["", "weibo_news_detail"]

    @classmethod
    def get_channel_xpath(cls, channel: str):
        return cls.__dict__.get(channel, None)


replace_repattern = lambda pattern: pattern.replace('"', "").split(":", 1)[1]


class Saved:
    def __init__(self, elements):
        self.elements = elements
        self.replace = replace_repattern

    def sohu_account(self, html, pattern):
        self.elements = etree.HTML(html).xpath(pattern)
        return self.elements

    def weibo_news_detail(self):
        date = re.search("\"created_time\": \"(.*?)\"", self.html).group(1).replace("T", " ").replace("Z", "")
        uid = re.search("\"id\": \"(.*?)\"", self.html).group(1)
        publisher = re.search("\"name\": \"(.*?)\"", self.html).group(1)
        title = re.search("\"title\": \"(.*?)\"", self.html).group(1)
        content = re.search("\"content\": \"(.*?.*)", self.html).group(1)[0:-2]
        publish_info = "微博新闻"
        return title, publisher, publish_info, date, content, uid

    def yidianzixun(self):
        def get_publishtime(date_string):
            date = None
            now = int(time.time())
            if "刚刚" in date_string:
                date = now
            elif "小时前" in date_string:
                date_pattern = int(date_string.replace("小时前", ""))
                date = now - (date_pattern * 3600)
            elif "分钟前" in date_string:
                date_pattern = int(date_string.replace("分钟前", ""))
                date = now - (date_pattern * 60)
            elif "天前" in date_string:
                date_pattern = int(date_string.replace("天前", ""))
                date = now - (date_pattern * 86400)
            else:
                date = date_string.replace(".", "-") + " 00:00:00"
                if len(date.split("-")[1]) == 1:
                    date = (date_string.replace(".", "-") + " 00:00:00").split("-")
                    date[1] = "0" + date[1]
                    date = '-'.join(date)
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date)) if isinstance(date, int) else date
        date = self.replace(re.search("\"date\":\"(.*?)\"", self.html).group(0))
        uid = self.replace(re.search("\"fromId\":\"(.*?)\"", self.html).group(0))
        publisher = self.replace(re.search("\"source\":\"(.*?)\"", self.html).group(0))
        title, content = self.elements
        date = get_publishtime(date)
        for bad in content.xpath("//*[@class='yidian-wm-copyright-bottom']"):
            bad.getparent().remove(bad)

        content = self.tostring(content)
        return title, publisher, "一点资讯", date, content, uid

    def news_qq(self):
        uid = self.replace(re.search(r'chlid\":.*?\"(.*?)\"', self.html).group(0))
        title,publisher,publish_time,content = self.elements
        content = self.tostring(content)
        return title, publisher, "腾讯新闻", publish_time, content, uid

    def dy_163_com(self):
        title, publish_time, publisher, content = self.elements
        content = self.tostring(content)
        return title, publisher, "网易有料", publish_time, content, ""

    def sohu_detail(self):
        try:
            publisher, title, _, publish_time, content = self.elements
        except ValueError as err:
            title, publish_time, content, publisher = self.sohu_account(self.html, Channel.WWW_SOHU_ACCOUNT[0])
            publisher = str(publisher)
        publisher = publisher if type(publisher) == str else publisher.xpath("text()")[0]
        uid = re.search("weboUrl: \".*?\"", self.html).group(0).replace('"', "").split(":", 1)[1].strip()
        uid = uid.split("xpt=")[1]
        content = self.tostring(content)
        return title, publisher, "搜狐新闻", publish_time, content, uid

    def weixin(self):
        date = re.findall('publish_time = \".*\"', self.html)[0].split('"')[1]
        title, publisher, publish_info, uid, content = self.elements
        content = self.tostring(content)
        return title, publisher, publish_info, date, content, uid

    def baijiahao(self):
        uid, title, publisher, content, *_ = self.elements
        _time = self.elements[-1]
        date = self.elements[-2]
        content = self.tostring(content)
        return title, publisher, "百家号", date + " " + _time, content, uid

    def toutiao_detail(self):
        detail_info = self.extractor.extract()
        title = detail_info.get("title")
        publisher = detail_info.get("publisher")
        content = detail_info.get("body")
        publish_time = detail_info.get("publishtime")
        publish_info = "今日头条"
        uid = detail_info.get("uid")

        detail_info.clear()

        if not content:
            raise AttributeError("body is empty..")
        return title, publisher, publish_info, publish_time, content, uid

    def ifeng(self):
        pattern = "(20\d{2}([\.\-/|年月\s]{1,3}\d{1,2}){2}日?(\s?\d{2}:\d{2}(:\d{2})?)?)|(\d{1,2}\s?(分钟|小时|天)前)"
        publish_time = re.findall(pattern, self.html)[0][0]
        title, publish_info, content = self.elements
        uid, publisher = publish_info.xpath("@href")[0], publish_info.xpath("text()")[0]
        uid = uid.split("/")[-1]
        content = self.tostring(content)
        return title, publisher, "大风号", publish_time, content, uid

    def tostring(self, element):
        return tostring(element, encoding="utf-8", pretty_print=True).decode()


class Parser(Saved):
    slots = ("pattern", "result")

    def __init__(self, channel: str, html: str):
        """

        :type html: str
        """
        self.channel = channel.upper()
        self.html = html
        self.extractor = Extractor(self.html)
        patterns = Channel.get_channel_xpath(self.channel)
        if not patterns:
            raise AttributeError("Patterns that need to be resolved do not exist")
        self.pattern, self.save_method_name = patterns
        if not self.pattern:
            self.elements = []
        else:
            self.elements = etree.HTML(self.html).xpath(self.pattern)
        super(Parser, self).__init__(self.elements)
    
    @property
    def result(self):
        method = getattr(self, self.save_method_name)
        resp = [item.strip() for item in method()]
        save_info = dict()
        save_info['title'] = resp[0]
        save_info['publisher'] = resp[1]
        save_info['publish_info'] = resp[2]
        save_info['publish_time'] = resp[3]
        isvalid = get_text(resp[4])
        if not isvalid:
            raise AttributeError("content is empty..")
        zdetail = zcompress(isvalid)
        if zdetail:
            save_info['detail'] =zdetail
        else:
            save_info['detail'] = isvalid
            save_info['zcompress'] = 0
        save_info['newdetail'] = resp[4]
        save_info["uid"] = resp[5]
        save_info["ts"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resp.clear()
        return save_info


class Extractor(object):
    def __init__(self, html):
        self.html = html

    def extract(self):
        result = {}
        gallery_info = re.search('gallery: JSON.parse\("(.*?)"\),', self.html)
        if gallery_info:
            recommend_news = re.search('siblingList: (\[\{.*?\}\])', self.html)
            gallery_detail = self.extract_gallery(gallery_info.group(1))
            gallery_detail['recommand_news'] = recommend_news.group(1) if recommend_news else ''
            return gallery_detail

        base_data = re.search('BASE_DATA = (\{.*?\});', self.html, re.S)
        if base_data:
            base_json = base_data.group(1)
            content = re.search("content: '(.*?)groupId", base_json, re.S)
            title = re.search("title: '(.*?)',", base_json)
            tags = re.search('tags: (.*?\]),', base_json)
            uid = re.search("uid: '(.*?)'", base_json)
            recommend_news = re.search('initList: (\[\{.*?\}\])', self.html, re.S)
            if content:
                content = content.group(1)
                content = unescape(content[:-1])
                body_imgs = self.extract_img(content)
                publisher, publishtime = self.extract_publish_info(base_json)
                result['body'] = content.strip().rstrip("',\n")
                result['bodyImgs'] = body_imgs
                result['publisher'] = publisher
                result['publishtime'] = publishtime
                result['title'] = title.group(1) if title else ''
                result['tags'] = re.findall('"name":"(.*?)"', tags.group(1)) if tags else []
                result['recommand_news'] = recommend_news.group(1) if recommend_news else ''
                result['uid'] = uid.group(1)
                return result
        return result

    def extract_img(self, content):
        imgs = re.findall('img.*?src="(.*?)"', content)
        body_imgs = []
        for img in imgs:
            body_imgs.append({'url': img})
        return body_imgs

    def extract_gallery(self, gallery_json):
        gallery_json = gallery_json.replace('\\"', '"')
        gallery_json = gallery_json.replace('\\\\', '\\')
        gallery_dict = json.loads(gallery_json)
        sub_images = gallery_dict.get('sub_images', [])
        sub_abstracts = gallery_dict.get('sub_abstracts')
        gallery_list = []
        for img, abstracts in zip(sub_images, sub_abstracts):
            img['description'] = abstracts
            gallery_list.append(img)
        body_imgs = [{'url': x['url']} for x in gallery_list]
        publisher, publishtime, title = self.extract_gallery_publish_info()
        gallery_info = {'title': title,
                        'body': json.dumps(gallery_list, ensure_ascii=False),
                        'bodyImgs': body_imgs,
                        'publisher': publisher,
                        'publishtime': publishtime}
        return gallery_info

    def extract_publish_info(self, base_json):
        publisher = re.search("source: '(.*?)',", base_json)
        publishtime = re.search("time: '(.*?)'", base_json)
        publisher = publisher.group(1) if publisher else ''
        publishtime = publishtime.group(1) if publishtime else ''
        return publisher, publishtime

    def extract_gallery_publish_info(self):
        publishtime = re.search("publish_time: '(.*?)'", self.html)
        media_info = re.search("mediaInfo: \{(.*?)\}", self.html, re.S)
        title = re.search("title: '(.*?)',", self.html)
        publisher = ''
        if media_info:
            publisher = re.search("name: '(.*?)'", media_info.group(1), re.S)
        publishtime = publishtime.group(1) if publishtime else ''
        publisher = publisher.group(1) if publisher else ''
        title = title.group(1) if title else ''
        return publisher, publishtime, title


if __name__ == "__main__":
    parser = Parser("media_weibo_cn", _html)
    print(json.dumps(parser.result, ensure_ascii=False, indent=4))
