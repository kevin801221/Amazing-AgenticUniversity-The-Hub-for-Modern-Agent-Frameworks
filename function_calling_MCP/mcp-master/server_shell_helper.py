from mcp.server.fastmcp import FastMCP
import subprocess, platform

mcp = FastMCP("shell_helper")

@mcp.tool()
async def get_platform() -> str:
    """取得作業系統平台

    Returns:
        str: 作業系統平台，"Windows" 為 Windows, 
                            "*nix" 為 Linux 或 MacOS
    """
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Linux" or system == "Darwin":
        return "*nix"
    else:        
        return "Unknown"

@mcp.tool()
async def shell_helper(platform: str, 
                       shell_command: str
) -> str:
    """可以依據 platform 指定的平作業系統平台執行：
       Windows powershell 指令或是 Linux/MacOS  
       shell 指令的工具函式

    Args:
        platform (str): 作業系統平台，"Windows" 為 Windows， 
                                   "*nix" 為 Linux 或 MacOS
        shell_command (str): 要執行的指令，Windows 平台只接受 
                             powershell 指令
    """

    # 啟動子行程
    if platform == "Windows":
        args = ['powershell', '-Command', shell_command]
    elif platform == "*nix":
        args = shell_command
    else:
        return "不支援的作業系統平台"
    
    process = subprocess.Popen(
        args,
        shell=True,             # 在 shell 中執行
        stdout=subprocess.PIPE, # 擷取標準輸出
        stderr=subprocess.PIPE, # 擷取錯誤輸出
        text=True               # 以文字形式返回
    )

    result = '執行結果：\n\n```\n'

    # 即時讀取輸出
    while True:
        output = process.stdout.readline()
        # 如果沒有輸出且行程結束
        if output == '' and process.poll() is not None:
            break
        if output:
            result += output

    result += "```"

    # 檢查錯誤輸出
    error = process.stderr.read()
    if error:
        result += f"\n\n錯誤: {error}"

    # 等待行程結束並取得返回碼
    return_code = process.wait()
    result += f"\n\n命令執行完成，返回碼: {return_code}\n\n"

    return result

if __name__ == "__main__":
    # 執行 MCP 伺服器
    mcp.run(transport='stdio')