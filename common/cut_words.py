#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.cut_words
# @Calendar: 2025-06-24 18:34
# @Time: 18:34
# @Author: mammon, kiramario
import datetime
import jieba


def run():
    # 精确模式
    text = "猫女茜莉"
    words = jieba.cut(text, cut_all=False)
    print("精确模式:", "/ ".join(words))

    # 全模式
    words_all = jieba.cut(text, cut_all=True)
    print("全模式:", "/ ".join(words_all))

    # 搜索引擎模式
    words_search = jieba.cut_for_search(text)
    print("搜索引擎模式:", "/ ".join(words_search))


if __name__ == "__main__":
    start = datetime.datetime.now()
    run()
    exec_time = (datetime.datetime.now() - start).total_seconds()
    print(f"run total spend: {exec_time:.3f}s\n")
