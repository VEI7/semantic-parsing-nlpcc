This repository contains code for  *[Open Domain Semantic Parsing task of NLPCC2019](http://tcci.ccf.org.cn/conference/2019/cfpt.php)*. 


## About this code
This code was developed with Python 3.6.

This code is based on the [TextSum code](https://github.com/tensorflow/models/tree/master/textsum) from Google Brain.

This code was developed for Tensorflow 0.12, but has been updated to run with Tensorflow 1.0.
In particular, the code in attention_decoder.py is based on [tf.contrib.legacy_seq2seq_attention_decoder](https://www.tensorflow.org/api_docs/python/tf/contrib/legacy_seq2seq/attention_decoder), which is now outdated.
Tensorflow 1.0's [new seq2seq library](https://www.tensorflow.org/api_guides/python/contrib.seq2seq#Attention) probably provides a way to do this (as well as beam search) more elegantly and efficiently in the future.

## How to run

### Get the dataset
The dataset of this task can be found [here](https://github.com/msra-nlc/MSParS).

### Run training
To train your model, run:

```
python run_model.py --mode=train --data_path=/path/to/train_data --vocab_path=/path/to/vocab --log_root=/path/to/a/log/directory --exp_name=myexperiment
```

This will create a subdirectory of your specified `log_root` called `myexperiment` where all checkpoints and other data will be saved. Then the model will start training using the `train_*.bin` files as training data.

### Run (concurrent) eval
You may want to run a concurrent evaluation job, that runs your model on the validation set and logs the loss. To do this, run:

```
python run_model.py --mode=eval --data_path=/path/to/val_data --vocab_path=/path/to/vocab --log_root=/path/to/a/log/directory --exp_name=myexperiment
```

Note: you want to run the above command using the same settings you entered for your training job.


### Run beam search decoding
To run beam search decoding:

```
python run_model.py --mode=decode --data_path=/path/to/test_data --vocab_path=/path/to/vocab --log_root=/path/to/a/log/directory --exp_name=myexperiment
```

Note: you want to run the above command using the same settings you entered for your training job (plus any decode mode specific flags like `beam_size`).

This will repeatedly load random examples from your specified datafile and generate a result using beam search. The results will be printed to screen.

