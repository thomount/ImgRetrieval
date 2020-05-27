# 使用方法

	pip install -r requirements.txt
	cd src
	python main.py [-a/-q] [-L2/-HI/-Bh/-CE] -v=[16/128/160/192/256/320/512/1024] [-l=128 -a=<alpha>]

## 其中
	-a/-q  全体测试/查询指定集合
	-L2/-HI/-Bh/-CE  距离函数选择
	-v=<vector_length>  选择不同长度的向量，其中大小在128~512的长度均为在128基础上继续改进
	-l=128 -a=<alpha>  选择向量分段点，实际距离=前半段的距离*a+后半段距离，alpha部分为实数，用"_"代替"."，例如 0.5 应写作 0_5
