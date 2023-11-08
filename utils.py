import re
class RandomChose:
    """用于给单词分配位置"""
    def __init__(self,left,right) -> None:
        self.left = left
        self.right = right
        self.range_ = [(left,right)]
    
    def divide(self,l,r):
        """挑选位置，range_为剩下位置"""
        for k,(o_l,o_r) in enumerate(self.range_):
            if o_l<l and r<o_r:
                self.range_[k]=(r,o_r)
                self.range_.insert(k,(o_l,l))
                break

    def giveback(self,l,r):
        """归还位置"""
        for k,(o_l,o_r) in enumerate(self.range_):
            if o_l==r:
                self.range_[k] = (l,o_r) #向右合并
                if k>0:
                    if self.range_[k-1][1]==l:  #判断左边能否合并
                        temp = self.range_[k-1][0]
                        self.range_[k] = (temp,o_r)
                        del self.range_[k-1]
                break
            elif o_l>r:
                self.range_.insert(k,(l,r))  
                break

class SpideWords:
    def __init__(self,path) -> None:
        self.file = open(path,'r',encoding='utf-8')
        self.context = self.file.read()

    def re_match(self):
        pattern = "\d?、\s*(\w*)\s*\n\n(.*)"
        result = re.findall(pattern,self.context)
        if result:
            result = [x for x in result if x[0].isascii()]
        self.close()
        return result
    def close(self):
        self.file.close()

    def isenglisth(self,s:str):
        return s.isascii()

if __name__=='__main__':
    spide = SpideWords(r"E:\code\2_tkinter\English-pyqt\words.txt")
    find_words = spide.re_match()
    print(find_words)

    # spide = SpideWords(r"E:\code\2_tkinter\English-pyqt\test.py")

    # cho = RandomChose(0,100)
    # cho.divide(12,15)
    # print(cho.range_)