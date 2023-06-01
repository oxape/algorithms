#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <cstdio>

using namespace std;

vector<vector<int>> compute_transition_function(string p) {
    vector<char> letters;
    for (int i=0; i<26; i++) {
         letters.push_back((char)((int)'a'+i));
    }
    int m = p.size();
    vector<vector<int>> transition(m+1);
    for (int q=0; q<p.size()+1; q++) {
        transition[q].reserve(26);
        for (int li=0; li<letters.size(); li++) {
            int k = min(m, q+1);
            string Pq_a = p.substr(q-k+1, k-1)+letters[li];
            int Pq_a_size = Pq_a.size();
            //比较P[0..k]是否是Pq_a的后缀，注意判断是不是Pq_a的后缀，而不是和Pq_a比较
            while (p.substr(0, k).compare(Pq_a.substr(Pq_a_size-k)) != 0 and k > 0) {
                k = k-1;
            }
            transition[q][(int)letters[li]-((int)'a')] = k;
        }
    }
    return transition;
}

int finite_automation_matcher(string s, string p) {
    vector<vector<int>> transition = compute_transition_function(p);
    int q = 0;
    int m = p.size();
    for (int i=0; i<s.size(); i++) {
        q = transition[q][(int)s.at(i)-((int)'a')];
        if (q == m) {
            return i-m+1;
        }
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
