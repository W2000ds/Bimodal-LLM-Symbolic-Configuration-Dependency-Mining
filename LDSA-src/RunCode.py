from DepClassifyer import DepClassifyer
from DepIdentifyer import DepIdentifyer
from CodeExtractor import CodeExtractor
import pandas as pd
# import threading
# import time
# import os

# def run_morph(code_base_csv, result_file, prompt_file):
#     """执行DepMorph处理的线程函数"""
#     # 等待Finderresult.csv文件创建
#     while not os.path.exists(Finderresultfile) or os.stat(Finderresultfile).st_size == 0:
#         print("等待Finderresult.csv文件创建或写入内容...")
#         time.sleep(5)  # 每5秒检查一次
    
#     while True:
#         try:
#             # 读取当前的Yes结果
#             df = pd.read_csv(Finderresultfile)
#             current_yes_ids = df[df['Answer'] == 'Yes']['ID'].tolist()
            
#             if current_yes_ids:  # 如果有Yes结果
#                 print(f"Morph线程找到 {len(current_yes_ids)} 条回答为'Yes'的记录")
#                 print("当前Yes ID列表:", current_yes_ids)
                
#                 # 检查是否有新的结果需要处理
#                 morph = DepMorph(current_yes_ids, code_base_csv, result_file, prompt_file)
#                 morph.Find()
            
#             # 定期检查是否有新结果
#             time.sleep(30)  # 每30秒检查一次新结果
#         except Exception as e:
#             print(f"Morph线程发生错误: {e}")
#             time.sleep(10)  # 出错后等待10秒再重试


if __name__ == "__main__":

    modellist = ['doubao']

    for model in modellist:

        Identifyerprompt_file = './Agent1prompt.txt'
        Classifyerprompt_file = './Agent2prompt.txt'
        # questionsfile = '/home/lhy/LLM-dependency/questions.csv'
        Identifyerresultfile = f'ldsa-result/python/glance/{model}Finderresult.csv'
        Classifyerresultfile = f'ldsa-result/python/glance/{model}Classifyersresult.csv'

        # TA_resultcsv = 'TAresult/cdepdataset/cdep2.0result/Cdep-result.csv'
        # project_root_dir = '/home/lhy/cDep/cdep2/cdep-fse-ae/app/hadoop-2.9.2-src/'
        Code_Basecsv = 'TAresult/pyta/glance_with_code.csv'

        # 处理污点分析结果，获取代码片段
        # extractor = CodeExtractor(TA_resultcsv, project_root_dir, Code_Basecsv)
        # 启动identifyer
        DepIdentifyer = DepIdentifyer(Code_Basecsv, Identifyerresultfile, Identifyerprompt_file,model)
        DepIdentifyer.Find()
        print("Identify Done!")

        # 启动classifyer
        df = pd.read_csv(Identifyerresultfile)
        df = pd.read_csv(Identifyerresultfile, encoding='ISO-8859-1')
        current_yes_ids = df[df['ans'] == 'Yes']['id'].tolist()
        classifyer = DepClassifyer(current_yes_ids, Code_Basecsv, Classifyerresultfile, Classifyerprompt_file,model)
        classifyer.Find()
        print("Classifyer Done!")

    # record "Yes" ID
    # 读取CSV文件并提取回答为"Yes"的ID
    # morph_thread = threading.Thread(
    #     target=run_morph,
    #     args=(Code_Basecsv, DepMorphresultfile, Mophprompt_file),
    #     daemon=True  # 设置为守护线程，主线程结束时自动结束
    # )
    # morph_thread.start()
    # print("Morph处理线程已启动，将在后台持续监控Yes答案并进行处理")

    # # 执行Finder处理
    # finder = DepFinder(Code_Basecsv, Finderresultfile, Finderprompt_file)
    # finder.Find()
    # print("Finder主处理完成!")
    
    # 等待Morph线程处理所有结果
    # print("等待Morph线程完成所有处理...")
    # morph_thread.join(timeout=60)  # 最多等待60秒
    # print("程序执行完毕!")
    # print("Finder Done!")

    # DepMorph.dpseek(Finderresultfile, DepMorphresultfile)

    # print("Done!")