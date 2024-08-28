# 基于大模型 agent（智能体）生成 flask rest API

目的：基于 flask, flask-sqlalchemy, flask-restx, flask-migration，通过大模型 agent，相对低代码和自动的给出可以生成 CRUD api 的代码。


## 尝试的大模型
agent1. doubao- 是基于豆包的智能体
agent2. zhipu- 是基于智谱清言的智能体

## 小结
- 豆包的智能体，默认是在一个文件夹生成，出的 app.py 和 test.py 成功率都较高，但是需要自己改文件夹结构。
- 智谱清言的智能体，默认是按照文件夹结构给出文件，但是如果通过交互去修改代码，经常是只改一处，其他不改，总的用起来成功率低，需要大量调试。


