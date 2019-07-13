
word2dict = dict()
with open('data/MSParS_train.txt', 'r') as fin, open('data/vocab_all.txt','w') as fout:
    for line in fin.readlines():
        line = line.strip()
        if '<question id' in line:
            question_text = line.split('>')[1][1:]
            question_text_list = question_text.split(' ')
            for q in question_text_list:
                if q in word2dict:
                    word2dict[q] += 1
                else:
                    word2dict[q] = 1
        if '<logical form id' in line:
            logical_text = line.split('>')[1][1:]
            logical_text_list = logical_text.split(' ')
            for q in logical_text_list:
                if q in word2dict:
                    word2dict[q] += 1
                else:
                    word2dict[q] = 1

    for k,v in word2dict.items():
        fout.write(k + ' ' + str(v)+'\n')