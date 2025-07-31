# 從 crewai 庫中匯入 Crew、Process 和 LLM 類別
# Crew: 用於組合代理和任務，並啟動整個工作流程
# Process: 定義了任務的執行方式，例如 sequential (順序執行) 或 hierarchical (層級執行)
# LLM: 用於配置要使用的大型語言模型
from crewai import Crew, Process, LLM

# 從我們自定義的模組中匯入代理和任務的定義類別
from agents import AnalysisAgents
from tasks import AnalysisTasks

# --- LLM 配置 ---
# 實例化 LLM 類別，來設定我們要使用的語言模型
# 這裡我們使用的是本地運行的 Ollama 服務
llm = LLM(
    # 'model' 參數指定了要使用的具體模型名稱，格式為 "ollama/模型名稱:版本"
    # 'llama3.1:latest' 表示使用最新版的 llama3.1 模型
    model="ollama/deepseek-r1:8b",
    # 'base_url' 指向 Ollama 服務的 API 端點
    base_url="http://localhost:11434",
)

# --- 主流程控制 ---
# 定義一個名為 FinancialCrew 的類別，用於封裝整個金融分析團隊的設置和執行邏輯
class FinancialCrew:

    # 初始化方法，接收一個公司名稱 (company) 作為參數
    def __init__(self, company: str):
        self.company = company

    # 'run' 方法是啟動整個分析流程的入口
    def run(self):
        # 實例化我們定義的代理和任務類別
        # 傳入配置好的 llm 實例給 AnalysisAgents
        agents = AnalysisAgents(llm)
        tasks = AnalysisTasks()

        # --- 創建代理實例 ---
        # 調用 agents 類別中的方法，創建具體的代理
        mr_analyst = agents.market_research_analyst()  # 市場研究分析師
        cfa = agents.cfa()  # 特許財務分析師

        # --- 創建任務實例 ---
        # 調用 tasks 類別中的方法，創建具體的任務，並將代理分配給它們
        # 創建研究任務，並將其分配給市場研究分析師 (mr_analyst)
        research = tasks.research(mr_analyst, self.company)
        # 創建分析任務，分配給財務分析師 (cfa)，並將研究任務 (research) 的結果作為其上下文
        analysis = tasks.analysis(cfa, research)

        # --- 組建 Crew ---
        # 實例化 Crew 類別，將代理和任務組合在一起
        crew = Crew(
            # 'agents' 參數是一個列表，包含了所有參與工作的代理
            agents=[mr_analyst, cfa],
            # 'tasks' 參數也是一個列表，包含了所有需要執行的任務
            tasks=[research, analysis],
            # 'process' 參數定義了任務的執行流程，這裡為 Process.sequential，表示任務將按列表順序依次執行
            process=Process.sequential,
            # 'verbose' 設為 True，會在執行時打印詳細的思考過程和日誌
            verbose=True
        )

        # --- 啟動 Crew ---
        # 調用 crew 的 kickoff 方法，開始執行所有任務
        result = crew.kickoff()

        # 返回最終的執行結果
        return result

# --- 程式主入口 ---
# 這是一個 Python 的標準寫法，確保只有當這個文件被直接執行時，下面的程式碼才會運行
if __name__ == "__main__":
    # 打印歡迎訊息
    print("\n\n## 歡迎來到投資顧問團隊")
    print("-------------------------")
    # 使用 input() 函數提示用戶輸入想分析的公司名稱
    company = input("請輸入您想分析的公司名稱\n")

    # 實例化我們的 FinancialCrew 類別，並傳入用戶輸入的公司名稱
    financial_crew = FinancialCrew(company)
    # 調用 run 方法來啟動分析流程
    result = financial_crew.run()
    
    # --- 打印最終結果 ---
    # 打印分隔線和標題，使輸出更清晰
    print("\n\n####################")
    print("## 如下是分析結果")
    print("####################\n")
    # 打印 crew 執行完成後返回的最終報告
    print(result)
