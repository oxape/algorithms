

class Solution(object):
    def strStr(self,  haystack,  needle):
        # dfa = self.dfa_construct(needle)
        dfa = self.kmp_construct(needle)
        M = len(needle)
        j = 0
        for i in range(len(haystack)):
            j = dfa[j][haystack[i]]
            if j == M:
                break
        if (j == M):
            return i - M + 1
        return -1

    def dfa_construct(self,  pattern: str):
        M = len(pattern)
        dfa = {}
        for j in range(M):
            dfa[j] = {}
            print(f'------{j}------')
            for li in range(26):
                # 对于每一个字符k最多为当前状态j+1, 状态机终止态为M
                k = min(M,  j+1)
                c = chr(ord('A')+li)
                # 状态等于j时已经匹配的字符为pattern[0:j]
                # 1、现在检查第j和字符是否匹配
                # 2、第j个字符不匹配时查找pattern[0:j]+c中即是前缀又是后缀的字串的最大长度
                # 也可以视作直接进行第2不查找最大长度的"前后缀", 第j字符匹配相当于pattern[0:j]+c == pattern[0:j+1], 自己是自己的最大长度的"前后缀"
                txt = pattern[:k-1]+c
                # print(f'{pattern[0:k]} {txt[len(txt)-k:]}') # 打印需要比较的前缀和后缀
                while pattern[0:k] != txt[len(txt)-k:] and k > 0:
                    k = k-1
                    # print(f'{pattern[0:k]} {txt[len(txt)-k:]}') # 打印需要比较的前缀和后缀
                dfa[j][c] = k
        return dfa

    def kmp_construct(self,  pattern: str):
        M = len(pattern)
        dfa = {}
        # 状态等于0时, 输入不匹配的字符下一个状态还是0
        j = 0
        dfa[j] = {}
        for i in range(26):
            dfa[j][chr(ord('A')+i)] = 0
        # 匹配的字符状态等于当前状态j+1
        dfa[j][pattern[j]] = j+1
        X = 0
        for j in range(1,  M):
            dfa[j] = {}
            for i in range(26):
                c = chr(ord('A')+i)
                # 失配时复制重启状态的dfa[X][...]到dfa[j][c]
                dfa[j][c] = dfa[X][c]
            # 匹配时等于当前状态j+1
            dfa[j][pattern[j]] = j+1
            '''
            下面一句代码是重点, 理解下面的代码时需要先理解search
            当前状态是j, 已经匹配的字符分别是pattern[0:j](不包括pattern[j]), txt中已经匹配的字符是txt[i:i+j](不包括txt[i+j])。
            失配后, 表明txt[i+j] != pattern[j]。
            按照暴力解法, 相当于要把j=0, 开始从i+1重新和pattern匹配。
            但是失配后, 我们已经知道了txt[i+1:i+j](不包括txt[i+j])其实就是pattern[1:j](不包括pattern[j])
            这时相当于把pattern[1:j](不包括pattern[j])输入状态机得到一个状态X, 然后从X状态继续输入txt[j], 便可以得到状态j中除了匹配(txt[i+j] == pattern[j])状态的其他状态。

            例如pattern = 'ABABAC'
            每次状态j的状态机计算完成后, 都要计算下一个状态的失配后的重启状态, 状态0时重启状态是0，状态1时由于pattern[1:j] = pattern[1:1] = ''，所以重启状态也是0。
            所以复制状态0的dfa[0][...]到状态1的dfa[1][...](除了匹配状态)
            当前状态是1，计算状态2时:如果失配相当于pattern[1:j] = pattern[1:2] = 'B'输入状态机，由于此时状态机[0:2](不包括2)都已经计算完毕，所以可以从重启状态0输入'B'得到状态2的重启状态
            计算得到状态2的重启状态还是0。记住此时的X等于从状态0开始输入了一个字符'B'
            当前状态是2，状态3时:如果失配相当于pattern[1:j] = pattern[1:3] = 'BA'输入状态机，而此时X保存的状态是已经输入了'B'的状态，此时从X状态继续输入'A'即可得到状态4的重启状态1
            当前状态是3，状态4时:如果失配相当于pattern[1:j] = pattern[1:4] = 'BAB'输入状态机，而此时X保存的状态是已经输入了'BA'的状态，此时从X状态继续输入'B'即可得到状态5的重启状态2
            当前状态是4，状态5时:如果失配相当于pattern[1:j] = pattern[1:5] = 'BABA'输入状态机，而此时X保存的状态是已经输入了'BAB'的状态，此时从X状态继续输入'A'即可得到状态5的重启状态3
            当前状态是5，状态6时:已经不需要计算状态6了，因为状态6了，因为状态6是终止态此时可以退出搜索了
            '''
            X = dfa[X][pattern[j]]
        return dfa

    def next_construct_minus_one(self, p: str):
        M = len(p)
        j = -1
        i = 0
        next = [-1] * (M+1)
        while i < M:
            if j == -1:
                i += 1
                next[i] = 0
                j = 0
            elif p[i] == p[j]:
                i += 1
                next[i] = j+1
                j += 1
            else:
                j = next[j]
        '''
        构造好的next数组表示当前模式中的第j(此处j仅代表索引和函数内的j变量没有关系)匹配失败时，
        1、pattern[1:j](不包括k)的最长前后缀是多少，例如为k，
        2、此时需要继续比较pattern[j]和txt[i]，
        3、如果相等，j++，i++
        4、如果不相等则另j=k，重新执行第1步
        '''
        return next
    
    def force_search(self, txt, pat):
        M = len(pat)
        N = len(txt)
        i = 0
        j = 0
        while i < N:
            if txt[i] == pat[j]:
                j += 1
            else:
                i -= j # 回退已经匹配的j个字符
                j = 0 # 重置为已经匹配了0个字符
            if j == M:
                return i - M + 1 # 找到匹配
            i += 1
        return -1
    
    def pmp_search(self, txt, pat):
        i = 0
        j = 0
        next = self.next_construct_minus_one(pat)
        while i<len(txt):
            if j == -1:
                j = 0
                i += 1
            elif pat[j] == txt[i]:
                j += 1
                i += 1
                if j == len(pat):
                    return i-j
            else:
                j = next[j]
        return -1

if __name__ == '__main__':
    # haystack = "BCBAABACAABABACAA"
    # needle = "ABABAC"
    haystack = "AAAAAABCDE"
    needle = "ABCDE"
    result = Solution().strStr(haystack,  needle)
    print(f'strStr = {result}')
    result = Solution().force_search(haystack,  needle)
    print(f'force_search = {result}')
    result = Solution().pmp_search(haystack, needle)
    print(f'pmp_search = {result}')