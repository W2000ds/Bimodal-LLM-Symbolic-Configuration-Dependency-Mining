from DepClassifyer import DepClassifyer
from DepIdentifyer import DepIdentifyer
from CodeExtractor import CodeExtractor
import pandas as pd



if __name__ == "__main__":

    modellist = ['dpseek']
    software = 'hdfs' # Replace with your actual software name

    for model in modellist:

        Identifyerprompt_file = './prompt1.txt'
        Classifyerprompt_file = './prompt2.txt'
        # questionsfile = '/home/lhy/LLM-dependency/questions.csv'
        Identifyerresultfile = f'path/to/your/resultfolder/{model}Finderresult.csv'
        Classifyerresultfile = f'path/to/your/resultfolder/{model}Classifyersresult.csv'

        TA_resultcsv = f'TAresult/{software}.csv'
        project_root_dir = 'path/to/your/software/src/directory'  # Replace with your actual root directory
        Code_Basecsv = '/CodeDepBase.csv'

        extractor = CodeExtractor(TA_resultcsv, project_root_dir, Code_Basecsv)

        DepIdentifyer = DepIdentifyer(Code_Basecsv, Identifyerresultfile, Identifyerprompt_file,model)
        DepIdentifyer.Find()
        print("Identify Done!")

        # classifyer
        df = pd.read_csv(Identifyerresultfile)
        df = pd.read_csv(Identifyerresultfile, encoding='ISO-8859-1')
        current_yes_ids = df[df['ans'] == 'Yes']['id'].tolist()
        classifyer = DepClassifyer(current_yes_ids, Code_Basecsv, Classifyerresultfile, Classifyerprompt_file,model)
        classifyer.Find()
        print("Classifyer Done!")