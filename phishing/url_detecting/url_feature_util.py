#!/usr/bin/env python
# coding:utf-8

from url_features import FeatureClassify


class SetFeature(object):

    def __init__(self, url):
        self.fc_obj = FeatureClassify(url)
        self.features_lst_local = [
            'get_url_domain_symbol_1',
            'get_url_query_symbol_2',
            'get_url_path_symbol_3',
            'get_url_length',
            'get_url_domain_length',
            'get_url_domain_level_length',
            'get_url_path_level_length',
            'get_url_domain_is_ip_type',
            'get_url_domain_brand',
            'get_url_path_brand',
            'get_tiny_domain',
            'get_special_character'
        ]

    # 创建特征函数列表, 并且利用特征函数得到特征列表
    def set_feature(self):
        list_feature = []
        list_fc_func = map(lambda x: 'self.fc_obj.' + x + '()', self.features_lst_local)
        # return map(lambda x: eval(x), lst) 报错
        for fc_func in list_fc_func:
            list_feature.append(eval(fc_func))
        return list_feature






'''test
url1 = "http://www.luxinnerwear.com/javascript_gallery/alibaba/alibaba/login.alibaba.com.php?email=abuse@madecenter.com"
url2 = "http://www.Confirme-paypal.com/"
url3 = "http://www.mmch.co.in/font/index2.html?email=abuse@sfc-ksa.com"
url4 = "http://xxxxx/abc?name=admin&password=admin"
url5 = "http://docs.restala.com/LatestG/file/ServiceLoginAuth.php?cmd=?LOB=RBGLogon&amp;_pageLabel=page_logonform&amp;secured_buyer_page"
url6 = "http://www.legitimate.com//http://www.phishing.com"
url7 = "http://173.236.239.124/wp-content/themes/twentyfourteen/css/alibaba/index.php?email=abuse@houstonlinksmagazine.com"
url8 = "http://www.legitimate.com//http://www.phishing.com"
url9 = "http://www.cclpgms.com/js/?_Acess_Tooken&amp;Acirc;????????????????????????????????792e070ef1e2a9747e63dd241bb32a87792e070ef1e2a9747e63dd241bb32a"
url10 = "http://3designcenter.com/blog/wp-admin/network/other/index.html?.rand&amp;us.battle.net/login/en"
url11 = "http://shop.dominion.dn.ua/templates/redirect/smiles_motivo_para_sorrir_/?https://www.smiles.com.br/promocoes/redireciona/cadastrar/novapromocao/"

# test_func
def prefix_url():
    with open('test_urls.txt', 'rb') as f:
        urls = f.readlines()
        urls_strip = map(lambda x: x.strip(), urls)
    return urls_strip

obj = SetFeature('https://www.bai-du.com')
print obj.set_feature()
'''
