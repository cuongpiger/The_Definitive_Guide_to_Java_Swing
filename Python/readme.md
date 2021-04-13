# 1. 📁 misc
## 1.1. [utils.py](misc/utils.py) - [demo](misc/utils.ipynb)
* Class `CUtils`:
  * Method `seedir`: dùng để vẽ cây thư mục.

# 2. 📁 machine learning
## 2.1. [fp_growth.py](machine%20learning/fp_growth.py) - [demo](machine%20learning/fp_growth.ipynb)
* Class `MyFPGrowth`: khai thác luật kết hợp bằng thuật toán FP-Growth.
  * Method `genFpTree`: dùng để xây dựng ra cây FP-Growth.
  * Method `drawTree`: vẽ cây ra màn hình _(có thể lưu cây ra file ảnh ***.png**)_.
  * Method `associationRules`: dùng để phát sinh ra các mẫu mà thoả giá trị **minsup**.