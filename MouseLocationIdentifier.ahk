#Requires AutoHotkey v2.0

; 全局变量声明
global DisplayActive := false
global Color := 0xFFFFFF

; NUMPAD2: 启动/停止显示鼠标位置
NUMPAD2::
{
	global DisplayActive
	DisplayActive := !DisplayActive
	
	if (DisplayActive) {
		ToolTip("鼠标位置显示已启动")
		SetTimer(ShowMousePosition, 100)
	} else {
		ToolTip("鼠标位置显示已停止")
		SetTimer(ShowMousePosition, 0)
		SetTimer(() => ToolTip(), -1000)
	}
}

; 主检查与滚动函数
ShowMousePosition()
{
	global DisplayActive, Color
	
	; 获取当前鼠标位置
	MouseGetPos(&MouseX, &MouseY)

	; 获取当前位置的颜色
	Color := PixelGetColor(MouseX, MouseY)

	; 显示鼠标位置和颜色信息
	ToolTip("X: " . MouseX . " Y: " . MouseY . "`nColor: " . Color)
}

; 安全退出
#Esc::ExitApp