import pickle
import numpy as np

emb_path = '/home/weijiaqi/pointer-generator/glove.840B.300d.txt'
vocab = '/home/weijiaqi/pointer-generator/data/vocab_all.txt'
out = '/home/weijiaqi/pointer-generator/data/embedding_all.pkl'

def gen_embedding_pkl(ori_emb_path, vocab_path, out_path):
    with open(ori_emb_path, 'r') as ori_emb_file, open(vocab_path,'r') as vocab_file, open(out_path, 'wb') as fout:
        embedding_list = []
        token2embedding = dict()
        count = 0
        for line in ori_emb_file.readlines():
            if count % 10000 == 0:
                print(count)
            count += 1
            info = line.strip().split(' ')
            token2embedding[info[0]] = [float(i) for i in info[1:]]
        for line in vocab_file.readlines():
            info = line.strip().split(' ')
            if info[0] in token2embedding:
                embedding_list.append(token2embedding[info[0]])
            else:
                embedding_list.append(np.random.randn(300).tolist())
        pickle.dump(embedding_list, fout, -1)


gen_embedding_pkl(emb_path, vocab, out)