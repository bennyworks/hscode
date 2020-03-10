"""
    @author zhy
    @since 1.0
"""
from functools import reduce


class HsRecord():
    """
        海关编码记录
    """

    def __init__(self, base_info, tax, declarations, supervisions, quarantines,  ciq):
        """
            构造函数
        """
        # 商品编码
        self.code = base_info.code
        # 商品名称
        self.name = base_info.name
        # 是否过期
        self.outdated = base_info.outdated
        # 更新时间
        self.update_time = base_info.update_time
        # 税率信息
        self.tax = tax
        # 申报要素【有序列表】
        self.declarations = declarations
        # 监管条件
        self.supervisions = supervisions
        # 检疫类别
        self.quarantines = quarantines
        # CIQ代码
        self.ciq_code = ciq

    def __str__(self):
        name = self.name.replace('"', '\\"')

        return '{ "code": ' + str(self.code) + ', "name": "' + name + '", "outdated": ' + \
            ('true'if self.outdated else 'false') + ', "update_time": "' + self.update_time + \
            '", "tax_info": ' + str(self.tax) + ', "declarations": ' + \
            self.arr2json(self.declarations) + ', "supervisions": ' + \
            self.arr2json(self.supervisions) + ', "quarantines": ' + \
            self.arr2json(self.quarantines) + ', "ciq_codes": ' + \
            self.arr2json(self.ciq_code) + ' }'

    def arr2json(self, arr):
        """
            数组转换成json
        """
        if len(arr) == 0:
            return "[]"
        double_quote = list(map(lambda a: '"' + str(a) + '"', arr))
        linked = reduce(lambda a, b: str(a)+', '+str(b), double_quote)
        return '[' + linked + ']'


class BaseInfo():
    """
        海关编码基本信息
    """

    def __init__(self, code, name="", outdated=False, update_time=""):
        self.code = code
        self.name = name
        self.outdated = outdated
        self.update_time = update_time

    def __str__(self):
        return '{ "code": ' + str(self.code) + ', "name": "' + self.name + '", "outdated": ' + \
            ('true' if self.outdated else 'false') + \
            ', "update_time": "' + self.update_time + '" }'


class TaxInfo():
    """
      税率信息
    """

    # 出口税率、出口退税税率、出口暂定税率、增值税率、进口优惠税率、进口暂定税率、进口普通税率、消费税率
    def __init__(self, unit, export, ex_rebate, ex_provisional, vat, preferential, im_provisional,
                 import_, consumption):
        self.unit = unit
        self.export = export
        self.ex_rebate = ex_rebate
        self.ex_provisional = ex_provisional
        self.vat = vat
        self.preferential = preferential
        self.im_provisional = im_provisional
        self.import_ = import_
        self.consumption = consumption

    def __str__(self):
        return '{ "unit": "' + self.unit + '", "export": "' + self.export + '", "ex_rebate": "' +  \
            self.ex_rebate + '", "ex_provisional": "' + self.ex_provisional + '", ' + '"vat": "' + \
            self.vat + '", "preferential": "' + self.preferential + '", "im_provisional": "' + \
            self.im_provisional + '", "import": "' + self.import_ + '", "consumption": "' + \
            self.consumption + '" }'
