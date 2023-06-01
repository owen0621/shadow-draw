import random


def minhash(data, permutation):
    # 生成随机置换
    # permutation = list(range(len(data)))
    # random.shuffle(permutation)

    # 对输入数据进行置换
    permuted_data = [data[i] for i in permutation]

    # 找到第一个值为1的位置
    minhash_value = len(data)
    for i in range(len(permuted_data)):
        if permuted_data[i] == 1.0:
            # minhash_value = permutation[i]
            minhash_value = i
            break

    return minhash_value
