# -*- coding: utf-8 -*-
'''
将小于一百万亿元的小写金额转换为大写
（中国2011年GDP为47.3104万亿元）
by Haisheng HU <hanson@sdf.org>

version 0.1
 * basic functions
'''

from decimal import Decimal

def num2cap(num = Decimal('0')):
    # 1995年3月18日第八届全国人民代表大会第三次会议通过的《中华人民共和国中国人民
    # 银行法》以法律的形式明确规定了“人民币的单位为元”
    NUMERIC = (u'零', u'壹', u'贰', u'叁', u'肆', u'伍', u'陆', u'柒', u'捌', u'玖')
    PLACE = (u'拾', u'佰', u'仟', u'万', u'拾', u'佰', u'仟', u'亿')
    UNIT = (u'分', u'角', u'元')
    ADDENDUM = (u'负', u'整')
    chn = ''
    s = '%d' % (num * 100)
    l = len(s)
    # 零
    if num == 0:
        return NUMERIC[0] + UNIT[2] + ADDENDUM[1]
    # 负数
    if num < 0:
        chn += ADDENDUM[0]
        s = s[1:]
        l -= 1
    # 100 0000 0000 0000 00
    #  99 9999 9999 9999 99
    if l > 16:
        return u'不支持达到或超过一百万亿的金额'
    # 计算共遇到连续0的个数
    count = 0
    for i in range(l):
        digit = int(s[i])
        # 当前数字所在位数（zero-based，含小数部分）
        # 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0
        place = l - i - 1
        if digit != 0:
            # 清算连续的0
            if (place == 0) and (count > 0) and (l > 1) or \
(place >= 2) and (place not in [5, 9, 13]) and (count > 0) or \
(place >= 2) and (count >= 4):
                chn += NUMERIC[0]
            chn += NUMERIC[digit]
            if place >= 3:
                chn += PLACE[(place - 3) % 8]
            else:
                chn += UNIT[place % 3]
            count = 0
        else:
            # 当前遇到0，某些情况也需输出“万、亿、万亿”
            if (place == 6 and count < 4) or (place in [10, 14]):
                chn += PLACE[(place - 3) % 8]
            if place == 2:
                chn += UNIT[place % 3]
            count += 1
    if s[l-1] == '0':
        chn += ADDENDUM[1]
    return chn

if __name__ == '__main__':
    for num in [0,
            1,
            2.02,
            0.24,
            1234.56,
            100010,
            1000001011.1,
            12300100112340,
            -5,
            -23000.7,
        ]:
        print u'%0.2f: %s' % (num, num2cap(num))
