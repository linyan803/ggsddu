# ggsddu 好好学习天天向上
蓁蓁的错题本. 主要特点：智能排序，常错优先

## 目录和文件:

> |-database                                                         # 存放数据库的目录

> > |-ggsddu.db                                                 # 答题记录数据库
> >
> > |-english.db                                                  # 英语题库记
> >
> > |-biology.db                                                  # 生物题库
>
> |-raw                                                                   # 试题素材
>
> > |-english                                                        # 英语试题素材目录
> >
> > |-biology                                                        # 生物试题素材目录
> >
> > |-math                                                           # 数学试题素材目录
>
> |-resource                                                          # 存放UI界面图片
>
> |-source                                                             # 代码：Python脚本
>
> > |-app.py                                                        # 主程序
> >
> > |-single_choice                                            # 单个选择题
>
> > ​    |-single_choice.py                                   # 单个选题代码
> >
> > |-single_blank                                             # 单个填空题
>
> > ​    |-single_blank.py                                    # 单个选择题
> >
> > |-exercise                                                     # 练习题相关代码
> >
> > ​    |-exercise_list.py                                     # 练习题列表
> >
> > ​    |-exercise.py                                            # 练习题类
> >
> > |-misc                                                           # 杂项
> >
> > ​    |-constants.py                                         # 常量代码
>
> |-script                                                              # 非app脚本存放目录
>
> |-update                                                            # 升级文件目录
>
> > |-update_desc.json                                     # 升级描述文件
> >
> > |-update.py                                                  # 升级脚本



## 数据库设计

1. PRESONAL.db 是用户自身存放练习信息数据库. 这个数据库git下载时应该避免下载，存储用户个性化信息

   **exercise_info 表:** 存放用户答题信息

   SUBJECT INT8 NOT NULL,                           # 科目ID 
   ID INT NOT NULL,                                        # 题干ID
   ITEM_NUM INT8,                                          # 小题数目
   TIMES INT,                                                      # 答题次数
   CORRECT INT,                                                # 答对次数
   STATUS INT8,                                                 # 题目状态
   NOTE VARCHAR(255),                                   # 答题备注 255个字符
   WEIGHT REAL                                                 # 题目权重

   SUBJECT表示科目, 03代表英语. 题干ID, 每个科目独立编号, 总共可以有99999道错题.  ITEM_NUM 是题干对应的小问数量, 适用于一个题干多个空或多个选择题的场景

   NOTE是用户答题备注. STATUS 是题目状态, 当前没有用. WEIGHT是根据答题情况计算出的权重.

   **update_info表**: 存放用户更新信息

   ID INT PRIMARY KEY NOT NULL,                  # 更新ID
   UPDATE_DATE DATETIME,                             # 用户更新时间
   NOTE VARCHAR(255)                                     # 更新备注 255个字符

   

2. ENGLISH.db BIOLOGY.db 是分科目的错题库. 分不同科目的错题库使得下载更新变得容易

   **stem表**: 存放题干信息

   ID INT PRIMARY KEY NOT NULL,                  # 题干ID
   MODEL INT8,                                                   # 题目类型
   DES_STYLE INT8,                                             # 题干描述方式
   DES TEXT                                                          # 题干

   DES_STYLE是题干描述方式, TEXT_IN_DB = 0, IMG_FILE = 1, MD_IN_DB=2. 如果是TEXT_IN_DB, 则题干是按照DES中存储的文本来描述, MD_IN_DB则DES存储的是Markdown文本方式, 对于需要格式化显示的文本采用这种方式. MODEL是题目类型

   **key表**: 存放填空题的答案

   ID INT PRIMARY KEY NOT NULL,                  # 题干ID
   SUB_ID INT8,                                                   # 小题编号 
   KEY  VARCHAR(255)                                        # 填空答案

   **answer表**: 存放选择题的答案

   ID INT PRIMARY KEY NOT NULL,                  # 题干ID
   SUB_ID INT8,                                                   # 小题编号 
   ANSWER  VARCHAR(8)                                   # 选择题答案

   

   

   

   
   
   