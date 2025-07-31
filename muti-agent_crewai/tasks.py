# 匯入 Task 類別，用於定義代理需要執行的具體任務
from crewai import Task
# 匯入 textwrap 的 dedent 功能，用於處理多行字符串的縮排，讓程式碼更美觀
from textwrap import dedent

# 定義一個名為 AnalysisTasks 的類別，專門用來創建和管理所有分析相關的任務
class AnalysisTasks:
    
    # 定義一個方法來創建「市場研究」任務
    # 這個方法接收兩個參數：
    # agent: 將要執行此任務的代理實例
    # company: 需要研究的公司名稱
    def research(self, agent, company):
        # 使用 Task 類別來實例化一個新的任務
        return Task(
            # 'description' 是任務的核心，詳細描述了代理需要做什麼
            # 使用 f-string 將公司名稱動態地插入到描述中
            # dedent 函數會自動移除多行字串中每一行開頭的共同空白，使描述文本在程式碼中能保持對齊，同時在執行時又是正常的字串
            description=dedent(
                f"""
                正在搜索並總結最新的 {company} ���司動態和新聞。
                特別關注最近發生的重大事件。
                """
            ),
            # 'async_execution' 設置為 True，表示這個任務可以異步執行。
            # 在 crewAI 中，如果任務之間沒有嚴格的順序依賴，異步執行可以提升效率。
            async_execution=True,
            # 'agent' 參數指定了負責執行此任務的代理
            agent=agent,
            # 'expected_output' 明確告知代理，我們期望它完成任務後產出什麼樣格式的結果
            # 這有助於 LLM 更精準地生成符合我們需求的輸出
            expected_output="用列表的形式總結頭5項最重要的公司新聞。"
        )
    
    # 定義一個方法來創建「財務分析」任務
    # 這個方法接收兩個參數：
    # agent: 將要執行此任務的代理實例
    # context: 此任務的上下文信息，通常是前一個任務的執行結果
    def analysis(self, agent, context):
        # 實例化一個新的分析任務
        return Task(
            # 任務描述，指示代理需要對已有的信息進行分析和總結
            description=dedent(
                """
                將搜索到的信息進行分析，並且總結。
                """
            ),
            # 'agent' 參數指定了負責此分析任務的代理
            agent=agent,
            # 'context' 參數是 crewAI 的一個重要特性，它允許我們將其他任務的結果作為當前任務的輸入
            # 這裡我們傳入一個列表，包含了 research 任務的結果 (context)，這樣分析師代理就能基於研究員的發現來工作
            context=[context],
            # 同樣，定義期望的輸出格式，這裡要求是一份包含市場總結、走向分析和投資建議的綜合報告
            expected_output="用報告的形式總結該公司的市場和走向，最終得出是否應該買入該公司股票的建議。"
        )
