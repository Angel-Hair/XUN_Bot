from lxml import etree
import requests

from datetime import datetime

# 这里是早期版本的地震报道，因为采用了不同的方法，所以留了下来，仅供参考。
# 
# def getinfostr(info: list):
#     if not info:
#         return ''
#     # [CQ:emoji,id=128677]
#     header = '[CQ:emoji,id=128677]地震通报[CQ:emoji,id=128677]'
#     for po in info:
#         header += '\n地点: {}\n震级(M): {}\n深度(km): {}'.format(po['point'], po['ms'], po['d'])
    
#     return header

# async def getceicinfo(em: float) -> str: # 只报道震级>=em
#     info = []
#     html_data = requests.get("http://www.ceic.ac.cn/speedsearch?time=1")
#     nowdate = datetime.now()
#     html = etree.HTML(html_data.text)
#     table = html.xpath('//table[@class="speed-table1"]/tr[2]')[0]
#     msg_time_str = table.xpath('./td[2]/text()')[0]
#     msg_time = datetime.strptime(msg_time_str,'%Y-%m-%d %H:%M:%S')
#     ms = float(table.xpath('./td[1]/text()')[0])
#     print(ms, (nowdate - msg_time).seconds)
#     if ((nowdate - msg_time).seconds < 120) and (ms > em):
#         po = dict()
#         d = int(table.xpath('./td[5]/text()')[0])
#         point = table.xpath('./td[6]/a/text()')[0]
#         po['ms'] = ms
#         po['d'] = d
#         po['point'] = point
#         info.append(po)

#     info = getinfostr(info)

#     return info

# add_list = ['上海', '京沪深', '北京', '东莞', '重庆', '乐山','内江','凉山','彝族','南充','成都','宜宾','遂宁','巴中','资阳','达州','绵阳','泸州','德阳','眉山','广安','自贡', '四川', '贵阳','六盘水','安顺','遵义', '贵州', '南京','苏州','南通','镇江','宿迁','连云港','常州','无锡','徐州','扬州','盐城','淮安','泰州','昆山', '江苏', '深圳','广州','珠海','佛山','惠州','中山','云浮','韶关','汕头','江门','湛江','肇庆','梅州','茂名','清远','揭阳','河源','阳江','潮州','汕尾', '广东', '广西北海','南宁','桂林','柳州','梧州','玉林', '广西', '三亚','海口', '海南', '三明','南平','厦门','泉州','龙岩','福州','漳州','莆田','宁德', '福建', '石家庄','保定','唐山','邯郸','邢台','廊坊','秦皇岛','沧州','承德','张家口', '河北', '三门峡','信阳','南阳','周口','商丘','安阳','郑州','驻马店','许昌','洛阳','新乡','濮阳','开封','焦作','平顶山','漯河','鹤壁', '河南', '济南','东营','临沂','青岛','威海','烟台','潍坊','济宁','淄博','德州','聊城','日照','菏泽','滨州','泰安','莱芜','枣庄', '山东', '临汾','大同','太原','长治','阳泉','运城','晋中','忻州', '山西', '杭州','丽水','台州','嘉兴','宁波','金华','衢州','温州','绍兴','湖州','舟山', '浙江', '昆明','丽江','大理','西双版纳', '云南', '九江','上饶','南昌','吉安','宜春','赣州','抚州','萍乡','新余','景德镇', '江西', '武汉','十堰','咸宁','黄冈','孝感','宜昌','鄂州','黄石','衡水','襄阳','荆州','恩施','荆门', '湖北', '长沙','邵阳','郴州','岳阳','常德','衡阳','株洲','湘潭','益阳','永州','怀化','娄底', '湖南', '咸阳','安康','宝鸡','西安','榆林','渭南','汉中', '陕西', '沈阳','丹东','大连','锦州','铁岭','盘锦','鞍山', '辽宁', '中卫','吴忠','固原','银川', '宁夏', '亳州','六安','合肥','安庆','阜阳','马鞍山','宿州','芜湖','蚌埠','滁州','淮南','铜陵', '安徽', '佳木斯','七台河','哈尔滨','齐齐哈尔','大庆','牡丹江', '黑龙江', '兰州', '甘肃', '西宁', '青海', '长春', '吉林', '香港', '包头','呼和浩特','呼伦贝尔','锡林郭勒盟','鄂尔多斯','赤峰','通辽', '内蒙古', '乌鲁木齐','伊犁','克拉玛依', '新疆','日本']

class ceicinfo():

    def __init__(self, em: float =4.5, only: bool = True):  # 只报道震级>=em
        self.em = em
        self.only = only
        self.add_list = ['香港','台湾','上海', '京沪深', '北京', '东莞', '重庆', '乐山','内江','凉山','彝族','南充','成都','宜宾','遂宁','巴中','资阳','达州','绵阳','泸州','德阳','眉山','广安','自贡', '四川', '贵阳','六盘水','安顺','遵义', '贵州', '南京','苏州','南通','镇江','宿迁','连云港','常州','无锡','徐州','扬州','盐城','淮安','泰州','昆山', '江苏', '深圳','广州','珠海','佛山','惠州','中山','云浮','韶关','汕头','江门','湛江','肇庆','梅州','茂名','清远','揭阳','河源','阳江','潮州','汕尾', '广东', '广西北海','南宁','桂林','柳州','梧州','玉林', '广西', '三亚','海口', '海南', '三明','南平','厦门','泉州','龙岩','福州','漳州','莆田','宁德', '福建', '石家庄','保定','唐山','邯郸','邢台','廊坊','秦皇岛','沧州','承德','张家口', '河北', '三门峡','信阳','南阳','周口','商丘','安阳','郑州','驻马店','许昌','洛阳','新乡','濮阳','开封','焦作','平顶山','漯河','鹤壁', '河南', '济南','东营','临沂','青岛','威海','烟台','潍坊','济宁','淄博','德州','聊城','日照','菏泽','滨州','泰安','莱芜','枣庄', '山东', '临汾','大同','太原','长治','阳泉','运城','晋中','忻州', '山西', '杭州','丽水','台州','嘉兴','宁波','金华','衢州','温州','绍兴','湖州','舟山', '浙江', '昆明','丽江','大理','西双版纳', '云南', '九江','上饶','南昌','吉安','宜春','赣州','抚州','萍乡','新余','景德镇', '江西', '武汉','十堰','咸宁','黄冈','孝感','宜昌','鄂州','黄石','衡水','襄阳','荆州','恩施','荆门', '湖北', '长沙','邵阳','郴州','岳阳','常德','衡阳','株洲','湘潭','益阳','永州','怀化','娄底', '湖南', '咸阳','安康','宝鸡','西安','榆林','渭南','汉中', '陕西', '沈阳','丹东','大连','锦州','铁岭','盘锦','鞍山', '辽宁', '中卫','吴忠','固原','银川', '宁夏', '亳州','六安','合肥','安庆','阜阳','马鞍山','宿州','芜湖','蚌埠','滁州','淮南','铜陵', '安徽', '佳木斯','七台河','哈尔滨','齐齐哈尔','大庆','牡丹江', '黑龙江', '兰州', '甘肃', '西宁', '青海', '长春', '吉林', '香港', '包头','呼和浩特','呼伦贝尔','锡林郭勒盟','鄂尔多斯','赤峰','通辽', '内蒙古', '乌鲁木齐','伊犁','克拉玛依', '新疆','日本']
        self.firsttime = self.getfirsttime()

    def getfirsttime(self):
        html_data = requests.get("http://news.ceic.ac.cn/index.html")
        html = etree.HTML(html_data.text)
        msg_time_str = html.xpath('//table[@class="news-table"]/tr[2]/td[2]/text()')[0]
        time = datetime.strptime(msg_time_str,'%Y-%m-%d %H:%M:%S')
        return time

    async def getceicinfo(self) -> str:
        info = []
        html_data = requests.get("http://news.ceic.ac.cn/index.html")
        html_data.encoding = 'utf-8'
        html = etree.HTML(html_data.text)
        table = html.xpath('//table[@class="news-table"]/tr[2]')[0]
        msg_time_str = table.xpath('./td[2]/text()')[0]
        msg_time = datetime.strptime(msg_time_str,'%Y-%m-%d %H:%M:%S')
        print("[info]loading newtime……\nFirsttime: {}\nNew: {}".format(self.firsttime, msg_time))
        if msg_time != self.firsttime:
            self.firsttime = msg_time
            point = table.xpath('./td[6]/a/text()')[0]
            for add in self.add_list:
                if (add in point) or (not self.only):
                    ms = float(table.xpath('./td[1]/text()')[0])
                    if (ms > self.em):
                        po = dict()
                        d = int(table.xpath('./td[5]/text()')[0])
                        po['ms'] = ms
                        po['d'] = d
                        po['point'] = point
                        info.append(po)

                        info = self.getinfostr(info)

                        return info

                    else: print("[info]ms not >=".format(self.em))
                # else: print("{} not in add_list……".format(add))
        else: print("[info]time not update……")
        if not info: print("[info]Not update info.")

        return info

    def getinfostr(self, info: list):
        if not info:
            return ''
        # [CQ:emoji,id=128677]
        header = '[CQ:emoji,id=128677]地震通报[CQ:emoji,id=128677]'
        for po in info:
            header += '\n地点: {}\n震级(M): {}\n深度(km): {}'.format(po['point'], po['ms'], po['d'])
        
        return header