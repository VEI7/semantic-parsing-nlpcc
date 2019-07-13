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

**Warning**: Using default settings as in the above command, both initializing the model and running training iterations will probably be quite slow. To make things faster, try setting the following flags (especially `max_enc_steps` and `max_dec_steps`) to something smaller than the defaults specified in `run_model.py`: `hidden_dim`, `emb_dim`, `batch_size`, `max_enc_steps`, `max_dec_steps`, `vocab_size`. 

**Increasing sequence length during training**: Note that to obtain the results described in the paper, we increase the values of `max_enc_steps` and `max_dec_steps` in stages throughout training (mostly so we can perform quicker iterations during early stages of training). If you wish to do the same, start with small values of `max_enc_steps` and `max_dec_steps`, then interrupt and restart the job with larger values when you want to increase them.

### Run (concurrent) eval
You may want to run a concurrent evaluation job, that runs your model on the validation set and logs the loss. To do this, run:

```
python run_model.py --mode=eval --data_path=/path/to/val_data --vocab_path=/path/to/vocab --log_root=/path/to/a/log/directory --exp_name=myexperiment
```

Note: you want to run the above command using the same settings you entered for your training job.

**Restoring snapshots**: The eval job saves a snapshot of the model that scored the lowest loss on the validation data so far. You may want to restore one of these "best models", e.g. if your training job has overfit, or if the training checkpoint has become corrupted by NaN values. To do this, run your train command plus the `--restore_best_model=1` flag. This will copy the best model in the eval directory to the train directory. Then run the usual train command again.

### Run beam search decoding
To run beam search decoding:

```
python run_model.py --mode=decode --data_path=/path/to/test_data --vocab_path=/path/to/vocab --log_root=/path/to/a/log/directory --exp_name=myexperiment
```

Note: you want to run the above command using the same settings you entered for your training job (plus any decode mode specific flags like `beam_size`).

This will repeatedly load random examples from your specified datafile and generate a result using beam search. The results will be printed to screen.



### Help, I've got NaNs!
For reasons that are [difficult to diagnose](https://github.com/abisee/pointer-generator/issues/4), NaNs sometimes occur during training, making the loss=NaN and sometimes also corrupting the model checkpoint with NaN values, making it unusable. Here are some suggestions:

* If training stopped with the `Loss is not finite. Stopping.` exception, you can just try restarting. It may be that the checkpoint is not corrupted.
* You can check if your checkpoint is corrupted by using the `inspect_checkpoint.py` script. If it says that all values are finite, then your checkpoint is OK and you can try resuming training with it.
* The training job is set to keep 3 checkpoints at any one time (see the `max_to_keep` variable in `run_model.py`). If your newer checkpoint is corrupted, it may be that one of the older ones is not. You can switch to that checkpoint by editing the `checkpoint` file inside the `train` directory.
* Alternatively, you can restore a "best model" from the `eval` directory. See the note **Restoring snapshots** above.
* If you want to try to diagnose the cause of the NaNs, you can run with the `--debug=1` flag turned on. This will run [Tensorflow Debugger](https://www.tensorflow.org/versions/master/programmers_guide/debugger), which checks for NaNs and diagnoses their causes during training.
