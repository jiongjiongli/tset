



```
cd /root/exp_tset_cn/tset-main

# 放置标注数据
# lc_quad_pre_cn/sparql_cn_train.json
# lc_quad_pre_cn/sparql_cn_test.json

# 随机翻转一些Question部分作为模型输入, Question本身是模型输出
python lc_quad_pre_cn/get_flip_data.py

# 结合实体字典，关系字典，sparql字典，进行预处理，生成训练和测试语料
python lc_quad_pre_cn/preprocess.py

# 模型训练
CUDA_VISIBLE_DEVICES=0 python seq2seq/run_seq2seq.py configs/train_1_cn.json

```

