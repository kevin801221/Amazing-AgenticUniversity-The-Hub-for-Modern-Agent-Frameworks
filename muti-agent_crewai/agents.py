# 匯入 Agent 類別，用於定義我們的 AI 代理
from crewai import Agent
# 匯入我們自定義的搜索工具
from tools.search import SearchTools

# 定義一個名為 AnalysisAgents 的類別，專門用來創建和管理所有分析相關的代理
class AnalysisAgents:
    
    # 類別的初始化方法，接收一個大型語言模型 (llm) 的實例
    def __init__(self, llm):
        # 將傳入的 llm 實例儲存起來，以便後續代理使用
        self.llm = llm

    # 定義一個方法來創建「市場研究分析師」代理
    def market_research_analyst(self):
        # 使用 Agent 類別來實例化一個新的代理
        return Agent(
            # 指定這個代理要使用的大型語言模型
            llm=self.llm,
            # 定義代理的角色，這裡是「市場研究分析師」
            role="市場研究分析師",
            # 設定代理的最終目標
            goal="搜索公司的市場和財務狀況，並按照找到的信息整理總結出公司各方面的表現和財務狀況",
            # 描述代理的背景故事，這有助於 LLM 更好地進行角色扮演
            backstory="最富經驗的市場研究分析師，善於捕捉和發掘公司內在的真相。請用中文思考和行動，並用中文回覆客戶問題或與其他同事交流。",
            # 指定這個代理可以使用的工具列表，這裡是我們定義的 searchInfo 工具
            tools=[SearchTools.searchInfo],
            # 設定為 False，表示這個代理不能將任務委派給其他代理
            allow_delegation=False,
            # 設定代理執行任務的最大迭代次數
            max_iter=3,
            # 設定為 True，會在執行過程中打印詳細的日誌，方便調試
            verbose=True
        )
    
    # 定義一個方法來創建「特許財務分析師」(CFA) 代理
    def cfa(self):
        # 同樣使用 Agent 類別來實例化
        return Agent(
            # 指定使用的大型語言模型
            llm=self.llm,
            # 定義角色為「特許財務分析師」
            role="特許財務分析師",
            # 設定其目標，即基於研究員的資料進行深度分析並提供投資建議
            goal="根據市場研究分析師搜索到的資料，重新整理並總結出公司的狀況，並且提供該公司的股份是否值得買入的建議",
            # 描述其背景故事，強調其專業性和經驗
            backstory="最富經驗的投資者，善於透過公司細微的變化，捕捉公司股價走向。現在你面對一生中最中的客戶。請用中文思考和行動，並用中文回覆客戶問題或與其他同事交流。",
            # 這個代理沒有配置任何工具，因為它的任務是純分析，不需額外搜索
            tools=[],
            # 同樣不允許委派任務
            allow_delegation=False,
            # 開啟詳細日誌
            verbose=True
        )
