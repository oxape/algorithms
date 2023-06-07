

class Solution:
    def strStr(self,  haystack,  needle):
        # dfa = self.dfa_construct(needle)
        dfa = self.kmp_construct(needle)
        M = len(needle)
        j = 0
        i = 0
        while i < len(haystack) and j < M:
            j = dfa[j][haystack[i]]
            i += 1
        if (j == M):
            return i - M
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
        return next
    
    def force_search(self, txt, pat):
        M = len(pat)
        N = len(txt)
        i = 0
        j = 0
        while i < N:
            if txt[i] == pat[j]:
                j += 1
                i += 1
            else:
                '''
                回退已经匹配的j-1个字符，即是当txt[i]=pattern[0]，但是txt[i+j]!=pattern[j]时，从i+1位置从新和pattern[0]匹配
                '''
                i -= j-1
                j = 0 # 重置为已经匹配了0个字符
            if j == M:
                return i - M # 找到匹配
        return -1
    
    def ptm_search(self, txt, pat):
        i = 0
        j = 0
        '''
        构造好的next数组表示当前模式中的第j(此处j仅代表索引和函数内的j变量没有关系)匹配失败时，
        1、pattern[1:j](不包括k)的最长前后缀是多少，例如为k，
        2、此时需要继续比较pattern[j]和txt[i]，
        3、如果相等，j++，i++
        4、如果不相等则另j=k，重新执行第1步
        '''
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


class KMP:
    shift = False
    # shift = True
    '''
    这个可以找出所有匹配的字符，而不仅仅是第一个
    '''
    def KMP_MATCHER(self, T, P):
        n = len(T)
        m = len(P)
        '''
        pi数组包含对于某个q
        pattern[0:q](不包含q)
        pattern[0:q]
        pi[q] = pattern[0:q](不包含q)的最大前后缀
        '''
        pi = self.COMPUTE_PREFIX_FUNCTION(P)
        print(f'pi = {pi}')
        '''
        以下算法的本质是在patter[s:s+q]==T[s:s+i]成立时，patter[q]!=T[i]的情况下
        尝试下一个s'>s时，利用已有的patter[s:s+q]==T[s:s+i]，跳过所有不可能匹配的s'
        分别尝试pi[q]、pi[pi[q]]、pi[pi[pi[q]]]...
        另:
        pi^0(q) = pi[q]
        pi^1(q) = pi[pi[q]]
        pi^2(q) = pi[pi[pi[q]]]
        依次尝试pi^0(q)、pi^1(q)....直到pi^i(q)=0
        根据算法导论32.4节，引理32.5:
        pi^*(q) = {k: k<q 且P[0:k]是P[1:q]的后缀}
        这里引理说明pi^*(q)列出了所有P[0:k]是P[1:q]后缀的k
        根据算法导论32.4节，引理32.6:
        COMPUTE_PREFIX_FUNCTION可以正确的计算出pi(q)
        

        next数组不右移
                 0   1   2   3   4   5   6
        pattern: A   B   A   B   A   C   A
                 0   0   1   2   3   0   1

                pi(4) = 3
                pattern[0:4] = ABABA
                ABABA
                  ABABA
        next数组右移
                 0   1   2   3   4   5   6   7
        pattern: A   B   A   B   A   C   A   
                 0   0   0   1   2   3   0   1
        '''
        q = 0 # number of characters matched
        if self.shift:
            for i in range(0, n): # scan the text from left to right
                while q > 0 and P[q] != T[i]:
                    print(f'patter[{q}] != txt[{i}]')
                    q = pi[q] # next character does not match
                if P[q] == T[i]:
                    q = q + 1 # next character matches
                if q == m: # is all of P matched?
                    q = pi[q] # look for the next match
                    print(f'Pattern occurs with shift {i - m + 1} next match position at {q}') # 打印出所有匹配的字符
        else:
            for i in range(0, n): # scan the text from left to right
                while q > 0 and P[q] != T[i]:
                    q = pi[q-1] # next character does not match
                if P[q] == T[i]:
                    q = q + 1 # next character matches
                if q == m: # is all of P matched?
                    q = pi[q-1] # look for the next match
                    print(f'Pattern occurs with shift {i - m + 1} next match position at {q}') # 打印出所有匹配的字符
    
    def COMPUTE_PREFIX_FUNCTION(self, P):
        m = len(P)
        pi = [0]*(m)
        if self.shift:
            pi.append(0)
        pi[0] = 0
        k = 0
        if self.shift:
            for q in range(2, m):
                while k > 0 and P[k] != P[q]:
                    k = pi[k]
                if P[k] == P[q]:
                    k = k + 1
                pi[q+1] = k
        else:
            for q in range(1, m):
                while k > 0 and P[k] != P[q]:
                    k = pi[k]
                if P[k] == P[q]:
                    k = k + 1
                pi[q] = k
        return pi

if __name__ == '__main__':
    # haystack = "BCBAABACAABABACAA"
    # needle = "ABABAC"
    # haystack = "AAAAAABCDE"
    # needle = "ABCDE"
    haystack = "ABABABACAABABACA"
    needle = "ABABACA"
    result = Solution().strStr(haystack,  needle)
    print(f'strStr = {result}')
    result = Solution().force_search(haystack,  needle)
    print(f'force_search = {result}')
    result = Solution().ptm_search(haystack, needle)
    print(f'ptm_search = {result}')

    KMP().KMP_MATCHER(haystack, needle)