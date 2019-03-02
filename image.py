import numpy as np
import cv2
class OpenCVImageMatcher(object):   
    # 全图进行配对
    def match_sub_image(self, img_rgb ,imgfile):
        #加载原始RGB图像
        cv_img = np.array(img_rgb)
        img = cv2.cvtColor(cv_img, cv2.cv.CV_BGR2RGB)
        #创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #加载将要搜索的图像模板
        template = cv2.imread(imgfile, 0)
        #记录图像模板的尺寸
        w, h = template.shape[::-1]

        #使用matchTemplate对原始灰度图像和图像模板进行匹配
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        #设定阈值 
        threshold = 0.7 
        #res大于70% 
        loc = np.where( res >= threshold)
        locs = zip(*loc[::-1])# 列表
        if locs:
            return (locs[0],locs[1],locs[0]+w,locs[1]+h)
        else:
            return None

"""
图像识别的两套方案
1.截取全图
通过截取全图传递过来，然后使用识别返回对应的坐标，然后在坐标上进行点击
优点：
不用单独计算要识别的区域，可以进行全图的识别，可能对一些突然显示的界面有比较好的识别
缺点:
全图识别可能速度没有这么快，对于比如确定等按钮可能会造成错误点击
2.截取部分
首先要通过截取全图获取到每张图片在游戏界面的比例位置
然后再通过截取对应部分的区域进行识别

openVC图片
http://bluewhale.cc/2017-09-22/use-python-opencv-for-image-template-matching-match-template.html
截图
https://www.cnblogs.com/weiyinfu/p/8051280.html
openVC裁剪图像
https://codeday.me/bug/20170921/73527.html
"""
