import sys
import math
import pdb
state_M = 4
word_N = 0

A_dic = {}
B_dic = {}
Count_dic = {}
Pi_dic = {}
word_set = set()
state_list = ['B','M','E','S']
line_num = -1

INPUT_DATA = "RenMinData.txt"
PROB_START = "prob_start.txt"
PROB_EMIT = "prob_emit.txt"
PROB_TRANS = "prob_trans.py"

def Output():
    #start_fp = file(PROB_START,'w')
    #emit_fp = file(PROB_EMIT,'w')
    #trans_fp = file(PROB_TRANS,'w')

    #print("len(word_set) = %s " % (len(word_set)))
    for key in Pi_dic:
        '''
        if Pi_dic[key] != 0:
            Pi_dic[key] = -1*math.log(Pi_dic[key] * 1.0 / line_num)
        else:
            Pi_dic[key] = 0
        '''
        Pi_dic[key] = Pi_dic[key] * 1.0 / line_num
    f = open(PROB_START, 'w')
    f.write(str(Pi_dic))
    #with open(PROB_START, 'w') as fw:
    #   fw.write('%s' % '\n'.join(Pi_dic))
    #print >>start_fp,Pi_dic

    for key in A_dic:
        for key1 in A_dic[key]:
            '''
            if A_dic[key][key1] != 0:
                A_dic[key][key1] = -1*math.log(A_dic[key][key1] / Count_dic[key])
            else:
                A_dic[key][key1] = 0
            '''
            A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
    f = open(PROB_TRANS, 'w')
    f.write(str(A_dic))
    #with open(PROB_TRANS, 'w') as fw:
    #    fw.write('%s' % '\n'.join(A_dic))
    #print >>trans_fp,A_dic

    for key in B_dic:
        for word in B_dic[key]:
            '''
            if B_dic[key][word] != 0:
                B_dic[key][word] = -1*math.log(B_dic[key][word] / Count_dic[key])
            else:
                B_dic[key][word] = 0
            '''
            B_dic[key][word] = B_dic[key][word] / Count_dic[key]

    #print >> emit_fp,B_dic
    with open(PROB_EMIT, 'w') as fw:
        fw.write('%s' % '\n'.join(B_dic))
    #start_fp.close()
    #emit_fp.close()
    #trans_fp.close()


def getList(input_str):
    outpout_str = []
    if len(input_str) == 1:
        outpout_str.append('S')
    elif len(input_str) == 2:
        outpout_str = ['B','E']
    else:
        M_num = len(input_str) -2
        M_list = ['M'] * M_num
        outpout_str.append('B')
        outpout_str.extend(M_list)
        outpout_str.append('S')
    return outpout_str

def init():
    global state_M
    global word_N
    for state in state_list:
        A_dic[state] = {}
        for state1 in state_list:
            A_dic[state][state1] = 0.0
    for state in state_list:
        Pi_dic[state] = 0.0
        B_dic[state] = {}
        Count_dic[state] = 0

def readtrnfile():
    init()
    global word_setB
    global line_num

    with open('RenMinData.txt', encoding='utf-8') as f:
        line = f.readline()
        while line:
            line_num += 1
            line = line.strip()
            if not line:continue
            #line = line.decode("utf-8","ignore")

            word_list = []
            for i in range(len(line)):
                if line[i] == " ":continue
                word_list.append(line[i])
            #word_set = word_set | set(word_list)

            lineArr = line.split(" ")
            line_state = []
            for item in lineArr:
                line_state.extend(getList(item))

            if len(word_list) != len(line_state):
                print >> sys.stderr,"[line_num = %d][line = %s]" % (line_num, line.endoce("utf-8",'ignore'))
            else:
                for i in range(len(line_state)):
                    if i == 0:
                        Pi_dic[line_state[0]] += 1
                        Count_dic[line_state[0]] += 1
                    else:
                        A_dic[line_state[i-1]][line_state[i]] += 1
                        Count_dic[line_state[i]] += 1
                        if word_list[i] not in B_dic[line_state[i]]:
                            B_dic[line_state[i]][word_list[i]] = 0.0
                        else:
                            B_dic[line_state[i]][word_list[i]] += 1
            line = f.readline()
    Output()
    print(Pi_dic)
    print(A_dic)
    print(B_dic)



def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}] #tabular
    path = {}
    for y in states: #init
        V[0][y] = start_p[y] * emit_p[y].get(obs[0],0)
        path[y] = [y]
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            (prob,state ) = max([(V[t-1][y0] * trans_p[y0].get(y,0) * emit_p[y].get(obs[t],0) ,y0) for y0 in states if V[t-1][y0]>0])
            V[t][y] =prob
            newpath[y] = path[state] + [y]
        path = newpath
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def cut(sentence):
    #pdb.set_trace()
    prob, pos_list =  viterbi(sentence,('B','M','E','S'), Pi_dic, A_dic, B_dic)
    return (prob,pos_list)


if __name__ == "__main__":
    readtrnfile()

    test_str = u"长春市长春节讲话。"
    prob,pos_list = cut(test_str)
    print(test_str)
    print(prob)
    print(pos_list)
    test_str = u"他说的确实在理."
    prob,pos_list = cut(test_str)
    print(test_str)
    print(prob)
    print(pos_list)

    test_str = u"对于正在走向伟大复兴的中华民族而言，是一个值得纪念的日子"
    prob,pos_list = cut(test_str)
    print(test_str)
    print(pos_list)

    test_str = u"我有一台电脑。"
    prob,pos_list = cut(test_str)
    print(test_str)
    print(pos_list)