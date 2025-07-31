"""
LangGraph 條款比對工作流
每個節點專精單一任務，可視化檢驗過程
"""

from typing import Dict, List, Optional, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime

# 定義工作流狀態
class ClauseWorkflowState(TypedDict):
    # 輸入文件
    new_case_document: str
    historical_documents: List[str]
    
    # 處理結果 (每個節點的輸出)
    extracted_clauses: Optional[List[Dict]]
    historical_clauses: Optional[List[Dict]]
    matched_pairs: Optional[List[Dict]]
    difference_analysis: Optional[List[Dict]]
    recommendations: Optional[List[Dict]]
    final_report: Optional[str]
    
    # 控制流程
    current_step: str
    errors: List[str]
    human_feedback: Optional[Dict]
    
    # 聊天歷史 (用於可視化)
    messages: Annotated[List[BaseMessage], operator.add]

@dataclass
class ClauseDatabase:
    """簡單的條款資料庫"""
    db_path: str = "clauses.db"
    
    def __post_init__(self):
        self.init_database()
    
    def init_database(self):
        """初始化資料庫結構"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 案件表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY,
                case_name TEXT NOT NULL,
                case_type TEXT NOT NULL,
                client_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 條款表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clauses (
                id INTEGER PRIMARY KEY,
                case_id INTEGER,
                category TEXT NOT NULL,
                original_text TEXT NOT NULL,
                standardized_text TEXT,
                parameters JSON,
                risk_level TEXT,
                FOREIGN KEY (case_id) REFERENCES cases (id)
            )
        """)
        
        # 比對歷史表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comparisons (
                id INTEGER PRIMARY KEY,
                new_case_id INTEGER,
                reference_case_id INTEGER,
                clause_category TEXT,
                similarity_score REAL,
                difference_type TEXT,
                action_taken TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (new_case_id) REFERENCES cases (id),
                FOREIGN KEY (reference_case_id) REFERENCES cases (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_case(self, case_name: str, case_type: str, client_name: str) -> int:
        """儲存案件基本資訊"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO cases (case_name, case_type, client_name)
            VALUES (?, ?, ?)
        """, (case_name, case_type, client_name))
        
        case_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return case_id
    
    def save_clauses(self, case_id: int, clauses: List[Dict]):
        """儲存條款"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for clause in clauses:
            cursor.execute("""
                INSERT INTO clauses 
                (case_id, category, original_text, standardized_text, parameters, risk_level)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                case_id,
                clause.get('category'),
                clause.get('original_text'),
                clause.get('standardized_text'),
                json.dumps(clause.get('parameters', {})),
                clause.get('risk_level')
            ))
        
        conn.commit()
        conn.close()
    
    def get_historical_cases(self, case_type: str = None) -> List[Dict]:
        """取得歷史案件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if case_type:
            cursor.execute("""
                SELECT c.*, cl.category, cl.original_text, cl.standardized_text, 
                       cl.parameters, cl.risk_level
                FROM cases c
                LEFT JOIN clauses cl ON c.id = cl.case_id
                WHERE c.case_type = ?
                ORDER BY c.created_at DESC
            """, (case_type,))
        else:
            cursor.execute("""
                SELECT c.*, cl.category, cl.original_text, cl.standardized_text,
                       cl.parameters, cl.risk_level  
                FROM cases c
                LEFT JOIN clauses cl ON c.id = cl.case_id
                ORDER BY c.created_at DESC
            """)
        
        results = cursor.fetchall()
        conn.close()
        
        # 組織數據結構
        cases = {}
        for row in results:
            case_id = row[0]
            if case_id not in cases:
                cases[case_id] = {
                    'id': case_id,
                    'case_name': row[1],
                    'case_type': row[2], 
                    'client_name': row[3],
                    'created_at': row[4],
                    'clauses': []
                }
            
            if row[5]:  # 如果有條款
                cases[case_id]['clauses'].append({
                    'category': row[5],
                    'original_text': row[6],
                    'standardized_text': row[7],
                    'parameters': json.loads(row[8]) if row[8] else {},
                    'risk_level': row[9]
                })
        
        return list(cases.values())

class ClauseWorkflow:
    def __init__(self, gemini_api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=gemini_api_key,
            temperature=0.1
        )
        self.db = ClauseDatabase()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """建構 LangGraph 工作流"""
        workflow = StateGraph(ClauseWorkflowState)
        
        # 添加節點
        workflow.add_node("extract_new_clauses", self.extract_new_clauses)
        workflow.add_node("load_historical_clauses", self.load_historical_clauses)
        workflow.add_node("match_similar_clauses", self.match_similar_clauses)
        workflow.add_node("analyze_differences", self.analyze_differences)
        workflow.add_node("generate_recommendations", self.generate_recommendations)
        workflow.add_node("human_review", self.human_review)
        workflow.add_node("generate_final_report", self.generate_final_report)
        workflow.add_node("save_results", self.save_results)
        
        # 定義流程
        workflow.set_entry_point("extract_new_clauses")
        
        workflow.add_edge("extract_new_clauses", "load_historical_clauses")
        workflow.add_edge("load_historical_clauses", "match_similar_clauses")  
        workflow.add_edge("match_similar_clauses", "analyze_differences")
        workflow.add_edge("analyze_differences", "generate_recommendations")
        workflow.add_edge("generate_recommendations", "human_review")
        
        # 條件分支：是否需要人工介入
        workflow.add_conditional_edges(
            "human_review",
            self.should_continue_or_revise,
            {
                "continue": "generate_final_report",
                "revise": "analyze_differences",  # 回到差異分析
                "end": END
            }
        )
        
        workflow.add_edge("generate_final_report", "save_results")
        workflow.add_edge("save_results", END)
        
        return workflow.compile()
    
    def extract_new_clauses(self, state: ClauseWorkflowState) -> ClauseWorkflowState:
        """節點1：提取新案件條款"""
        print("🔍 執行節點：提取新案件條款")
        
        prompt = f"""
        你是銀行法務條款提取專家。請從以下文件中提取所有標準化條款。
        
        文件內容：
        {state['new_case_document']}
        
        請以JSON格式回傳，包含：
        - category: 條款類別 (授信種類及額度/利費率/期限/還本付息/連帶保證人/擔保品/特約條件)
        - original_text: 原始條款文字
        - standardized_text: 標準化後的條款文字
        - parameters: 提取的參數 (金額、利率、期限等)
        - risk_level: 風險等級 (low/medium/high)
        
        範例格式：
        {{
          "clauses": [
            {{
              "category": "授信種類及額度",
              "original_text": "短期貸款額度新臺幣500,000仟元整，得循環動用",
              "standardized_text": "短期貸款額度新臺幣{{amount}}仟元整，{{circulation}}",
              "parameters": {{"amount": "500,000", "circulation": "得循環動用"}},
              "risk_level": "medium"
            }}
          ]
        }}
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            # 解析JSON回應
            content = response.content
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            
            result = json.loads(json_str)
            extracted_clauses = result.get('clauses', [])
            
            print(f"✅ 提取了 {len(extracted_clauses)} 個條款")
            
        except Exception as e:
            print(f"❌ 提取失敗：{e}")
            extracted_clauses = []
            state['errors'].append(f"條款提取失敗：{e}")
        
        state['extracted_clauses'] = extracted_clauses
        state['current_step'] = "extract_new_clauses"
        state['messages'].append(AIMessage(content=f"提取了 {len(extracted_clauses)} 個新條款"))
        
        return state
    
    def load_historical_clauses(self, state: ClauseWorkflowState) -> ClauseWorkflowState:
        """節點2：載入歷史案件條款"""
        print("📚 執行節點：載入歷史案件條款")
        
        # 從資料庫載入歷史案件
        historical_cases = self.db.get_historical_cases()
        
        # 扁平化所有歷史條款
        historical_clauses = []
        for case in historical_cases:
            for clause in case['clauses']:
                clause['source_case'] = case['case_name']
                clause['source_client'] = case['client_name']
                historical_clauses.append(clause)
        
        print(f"✅ 載入了 {len(historical_clauses)} 個歷史條款")
        
        state['historical_clauses'] = historical_clauses
        state['current_step'] = "load_historical_clauses"
        state['messages'].append(AIMessage(content=f"載入了 {len(historical_clauses)} 個歷史條款"))
        
        return state
    
    def match_similar_clauses(self, state: ClauseWorkflowState) -> ClauseWorkflowState:
        """節點3：配對相似條款"""
        print("🔗 執行節點：配對相似條款")
        
        new_clauses = state['extracted_clauses']
        historical_clauses = state['historical_clauses']
        
        matched_pairs = []
        
        for new_clause in new_clauses:
            # 找出同類別的歷史條款
            same_category_clauses = [
                hc for hc in historical_clauses 
                if hc['category'] == new_clause['category']
            ]
            
            if same_category_clauses:
                # 使用LLM判斷最相似的條款
                best_match = self._find_best_match(new_clause, same_category_clauses)
                
                matched_pairs.append({
                    'new_clause': new_clause,
                    'historical_clause': best_match,
                    'category': new_clause['category']
                })
            else:
                # 沒有歷史對應條款
                matched_pairs.append({
                    'new_clause': new_clause,
                    'historical_clause': None,
                    'category': new_clause['category']
                })
        
        # 檢查歷史條款中新案件缺少的
        new_categories = {clause['category'] for clause in new_clauses}
        historical_categories = {clause['category'] for clause in historical_clauses}
        
        missing_categories = historical_categories - new_categories
        for category in missing_categories:
            # 找到該類別最常見的歷史條款
            category_clauses = [hc for hc in historical_clauses if hc['category'] == category]
            if category_clauses:
                most_common = category_clauses[0]  # 簡化：取第一個
                matched_pairs.append({
                    'new_clause': None,
                    'historical_clause': most_common,
                    'category': category
                })
        
        print(f"✅ 配對了 {len(matched_pairs)} 組條款")
        
        state['matched_pairs'] = matched_pairs
        state['current_step'] = "match_similar_clauses"
        state['messages'].append(AIMessage(content=f"配對了 {len(matched_pairs)} 組條款"))
        
        return state
    
    def analyze_differences(self, state: ClauseWorkflowState) -> ClauseWorkflowState:
        """節點4：分析差異"""
        print("🔍 執行節點：分析差異")
        
        matched_pairs = state['matched_pairs']
        difference_analysis = []
        
        for pair in matched_pairs:
            analysis = self._analyze_clause_difference(pair)
            difference_analysis.append(analysis)
        
        print(f"✅ 分析了 {len(difference_analysis)} 組差異")
        
        state['difference_analysis'] = difference_analysis
        state['current_step'] = "analyze_differences"
        state['messages'].append(AIMessage(content=f"完成 {len(difference_analysis)} 組差異分析"))
        
        return state
    
    def generate_recommendations(self, state: ClauseWorkflowState) -> ClauseWorkflowState:
        """節點5：生成建議"""
        print("💡 執行節點：生成建議")
        
        difference_analysis = state['difference_analysis']
        recommendations = []
        
        for analysis in difference_analysis:
            recommendation = self._generate_recommendation(analysis)
            recommendations.append(recommendation)
        
        print(f"✅ 生成了 {len(recommendations)} 個建議")
        
        state['recommendations'] = recommendations
        state['current_step'] = "generate_recommendations"
        state['messages'].append(AIMessage(content=f"生成了 {len(recommendations)} 個建議"))
        
        return state
    
    def human_review(self, state: ClauseWorkflowState) -> ClauseWorkflowState:
        """節點6：人工審核點"""
        print("👤 執行節點：人工審核")
        
        # 檢查是否有高風險或需要人工審核的項目
        recommendations = state['recommendations']
        
        high_risk_items = [
            rec for rec in recommendations 
            if rec.get('requires_human_review', False) or rec.get('risk_level') == 'high'
        ]
        
        if high_risk_items:
            print(f"⚠️ 發現 {len(high_risk_items)} 個需要人工審核的項目")
            
            # 生成人工審核摘要
            review_summary = self._generate_review_summary(high_risk_items)
            
            state['human_feedback'] = {
                'requires_review': True,
                'high_risk_items': high_risk_items,
                'review_summary': review_summary
            }
        else:
            print("✅ 所有項目通過自動審核")
            state['human_feedback'] = {'requires_review': False}
        
        state['current_step'] = "human_review"
        state['messages'].append(AIMessage(content="人工審核檢查完成"))
        
        return state
    
    def should_continue_or_revise(self, state: ClauseWorkflowState) -> str:
        """條件分支：決定是否繼續或需要修正"""
        human_feedback = state.get('human_feedback', {})
        
        if human_feedback.get('requires_review', False):
            return "continue"  # 有風險項目，但繼續到報告生成
        else:
            return "continue"  # 沒有問題，繼續
    
    def generate_final_report(self, state: ClauseWorkflowState) -> ClauseWorkflowState:
        """節點7：生成最終報告"""
        print("📊 執行節點：生成最終報告")
        
        # 整合所有分析結果生成報告
        report = self._generate_comprehensive_report(state)
        
        state['final_report'] = report
        state['current_step'] = "generate_final_report"
        state['messages'].append(AIMessage(content="最終報告生成完成"))
        
        return state
    
    def save_results(self, state: ClauseWorkflowState) -> ClauseWorkflowState:
        """節點8：儲存結果"""
        print("💾 執行節點：儲存結果")
        
        # 儲存新案件到資料庫
        case_id = self.db.save_case(
            case_name=f"新案件_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            case_type="待分類",
            client_name="待填入"
        )
        
        # 儲存提取的條款
        if state['extracted_clauses']:
            self.db.save_clauses(case_id, state['extracted_clauses'])
        
        print(f"✅ 結果已儲存，案件ID：{case_id}")
        
        state['current_step'] = "save_results"
        state['messages'].append(AIMessage(content=f"結果已儲存，案件ID：{case_id}"))
        
        return state
    
    # 輔助方法
    def _find_best_match(self, new_clause: Dict, candidates: List[Dict]) -> Dict:
        """找出最相似的歷史條款"""
        # 簡化版：使用文字長度相似度
        new_text = new_clause['original_text']
        
        best_match = candidates[0]
        best_score = 0
        
        for candidate in candidates:
            # 簡單的相似度計算（實際可以用更複雜的NLP方法）
            candidate_text = candidate['original_text']
            score = len(set(new_text.split()) & set(candidate_text.split())) / max(len(new_text.split()), len(candidate_text.split()))
            
            if score > best_score:
                best_score = score
                best_match = candidate
        
        return best_match
    
    def _analyze_clause_difference(self, pair: Dict) -> Dict:
        """分析單組條款差異"""
        new_clause = pair['new_clause']
        historical_clause = pair['historical_clause']
        category = pair['category']
        
        if new_clause is None:
            return {
                'category': category,
                'status': 'missing_in_new',
                'analysis': '新案件缺少此類條款',
                'risk_level': 'medium',
                'differences': [],
                'possible_reasons': ['業務簡化', '風險降低', '遺漏']
            }
        
        if historical_clause is None:
            return {
                'category': category,
                'status': 'new_addition',
                'analysis': '新案件新增此類條款',
                'risk_level': 'medium',
                'differences': [],
                'possible_reasons': ['業務擴展', '風險控制', '法規要求']
            }
        
        # 比較參數差異
        new_params = new_clause.get('parameters', {})
        hist_params = historical_clause.get('parameters', {})
        
        differences = []
        for key in set(new_params.keys()) | set(hist_params.keys()):
            if new_params.get(key) != hist_params.get(key):
                differences.append({
                    'parameter': key,
                    'old_value': hist_params.get(key),
                    'new_value': new_params.get(key)
                })
        
        if not differences:
            status = 'identical'
            risk_level = 'low'
        elif len(differences) <= 2:
            status = 'minor_differences'
            risk_level = 'medium'
        else:
            status = 'major_differences'
            risk_level = 'high'
        
        return {
            'category': category,
            'status': status,
            'analysis': f'發現 {len(differences)} 個參數差異',
            'risk_level': risk_level,
            'differences': differences,
            'possible_reasons': self._infer_change_reasons(differences)
        }
    
    def _infer_change_reasons(self, differences: List[Dict]) -> List[str]:
        """推斷變化原因"""
        reasons = []
        
        for diff in differences:
            param = diff['parameter']
            if param == 'amount':
                reasons.append('授信額度調整')
            elif param == 'rate':
                reasons.append('利率政策變化')
            elif param == 'period':
                reasons.append('期限要求變化')
            else:
                reasons.append('業務條件調整')
        
        return list(set(reasons))
    
    def _generate_recommendation(self, analysis: Dict) -> Dict:
        """為單個分析生成建議"""
        category = analysis['category']
        status = analysis['status']
        risk_level = analysis['risk_level']
        
        if status == 'identical':
            return {
                'category': category,
                'action': 'keep_current',
                'reasoning': '條款與歷史案件相同，建議保持',
                'requires_human_review': False,
                'risk_level': risk_level
            }
        
        elif status == 'missing_in_new':
            return {
                'category': category,
                'action': 'consider_adding',
                'reasoning': '新案件缺少此條款，建議評估是否需要添加',
                'requires_human_review': True,
                'risk_level': 'medium'
            }
        
        elif status == 'new_addition':
            return {
                'category': category,
                'action': 'review_necessity',
                'reasoning': '新增條款，建議確認其必要性和合規性',
                'requires_human_review': True,
                'risk_level': 'medium'
            }
        
        else:  # minor_differences or major_differences
            return {
                'category': category,
                'action': 'review_changes',
                'reasoning': f'發現條款差異（{status}），建議檢討變更原因',
                'requires_human_review': risk_level in ['high', 'medium'],
                'risk_level': risk_level
            }
    
    def _generate_review_summary(self, high_risk_items: List[Dict]) -> str:
        """生成人工審核摘要"""
        summary = "需要人工審核的項目：\n\n"
        
        for i, item in enumerate(high_risk_items, 1):
            summary += f"{i}. {item['category']}\n"
            summary += f"   建議行動：{item['action']}\n"
            summary += f"   原因：{item['reasoning']}\n"
            summary += f"   風險等級：{item['risk_level']}\n\n"
        
        return summary
    
    def _generate_comprehensive_report(self, state: ClauseWorkflowState) -> str:
        """生成綜合報告"""
        extracted_clauses = state.get('extracted_clauses', [])
        recommendations = state.get('recommendations', [])
        
        report = f"""
# 條款比對分析報告

## 執行摘要
- 分析時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 提取條款數：{len(extracted_clauses)}
- 生成建議數：{len(recommendations)}

## 條款分析結果

### 可直接使用的條款
{self._format_recommendations_by_action(recommendations, 'keep_current')}

### 需要檢討的條款  
{self._format_recommendations_by_action(recommendations, 'review_changes')}

### 建議新增的條款
{self._format_recommendations_by_action(recommendations, 'consider_adding')}

### 需要確認的新增條款
{self._format_recommendations_by_action(recommendations, 'review_necessity')}

## 總結建議
基於以上分析，建議法務人員重點關注需要檢討和確認的條款，其餘條款可按建議處理。
"""
        return report
    
    def _format_recommendations_by_action(self, recommendations: List[Dict], action: str) -> str:
        """按行動類型格式化建議"""
        filtered = [rec for rec in recommendations if rec.get('action') == action]
        
        if not filtered:
            return "- 無\n"
        
        result = ""
        for rec in filtered:
            result += f"- {rec['category']}: {rec['reasoning']}\n"
        
        return result
    
    def run_workflow(self, new_document: str, historical_documents: List[str] = None) -> Dict:
        """執行完整工作流"""
        initial_state = {
            'new_case_document': new_document,
            'historical_documents': historical_documents or [],
            'extracted_clauses': None,
            'historical_clauses': None,
            'matched_pairs': None,
            'difference_analysis': None,
            'recommendations': None,
            'final_report': None,
            'current_step': '',
            'errors': [],
            'human_feedback': None,
            'messages': []
        }
        
        print("🚀 開始執行條款比對工作流...")
        
        try:
            final_state = self.graph.invoke(initial_state)
            print("✅ 工作流執行完成！")
            return final_state
        except Exception as e:
            print(f"❌ 工作流執行失敗：{e}")
            return {'error': str(e)}

# 使用範例
def main():
    # 初始化工作流
    workflow = ClauseWorkflow(gemini_api_key="YOUR_API_KEY")
    
    # 測試文件
    new_document = """
    凱基商業銀行批覆書
    
    一、核准條件
    (二)授信種類及額度：短期貸款額度新臺幣300,000仟元整，得循環動用。
    (三)利(費)率：按參考利率或本行資金成本加年利率0.80％計息。稅內含。
    (四)期限：自簽約日起算1年。
    (五)還本付息辦法：本金屆期清償，利息按月計收。
    (六)連帶保證人：張三。
    (七)擔保品：無。
    """
    
    # 執行工作流
    result = workflow.run_workflow(new_document)
    
    if 'error' not in result:
        print("\n" + "="*50)
        print("最終報告：")
        print(result.get('final_report', '無報告'))
        print("="*50)
    
    return result

if __name__ == "__main__":
    main()