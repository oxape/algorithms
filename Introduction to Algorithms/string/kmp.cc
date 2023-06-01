#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <cstdio>

using namespace std;

void compute_transition_function(vector<vector<int>> &dfa, string p) {
    vector<char> letters;
    int M = p.size();
    dfa.push_back({});
    for (int i=0; i<26; i++) {
        letters.push_back((char)((int)'a'+i));
        dfa[0].push_back(0);
    }
    dfa[0][(int)p.at(0)-((int)'a')] = 1;
    for (int X=0, j=1; j < M; j++) {
        
        dfa.push_back({});
        for (int li=0; li<letters.size(); li++) {
            int index = (int)letters[li]-((int)'a');
            dfa[j].push_back(dfa[X][index]);
        }
        dfa[j][(int)p.at(j)-((int)'a')] = j+1;
        printf("j = %d c = %c X = %d [%d][%c]=%d\n", j, p.at(j), X, X, p.at(j), dfa[X][(int)p.at(j)-((int)'a')]);
        X = dfa[X][(int)p.at(j)-((int)'a')];
    }
}

int finite_automation_matcher(string s, string p) {
    vector<vector<int>> dfa;
    compute_transition_function(dfa, p);
    int i;
    int q;
    int M = p.size();
    for (i=0, q=0; i<s.size() && q < M; i++) {
        q = dfa[q][(int)s.at(i)-((int)'a')];
    }
    if (q == M) {
        return i-M;
    }
    return -1;
}

int main(int argc, char *argv[]) {
    // string haystack = "sadbutsad", needle = "sad";
    // string haystack = "abababacaba", needle = "ababaca";
    string haystack = "mississippi", needle = "issip";
    int result = finite_automation_matcher(haystack, needle);
    printf("result = %d\n", result);
    return 0;
}
