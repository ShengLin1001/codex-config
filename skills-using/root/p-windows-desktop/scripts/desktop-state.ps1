# Read-only: print the foreground window (pid / title / rect) and whether each
# top-level window is minimized. Run before takeover as a baseline, after bringing
# up the target to verify the foreground, and after restoring to compare.
# Keep this file ASCII: Windows PowerShell 5.1 reads a BOM-less .ps1 as ANSI.
# SetProcessDPIAware puts the rect in the same coordinate space as windows-mcp.

Add-Type @"
using System; using System.Runtime.InteropServices; using System.Text;
public class DesktopState {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern int GetWindowThreadProcessId(IntPtr h, out int pid);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
  public struct RECT { public int L, T, R, B; }
}
"@
[DesktopState]::SetProcessDPIAware() | Out-Null
# Without this, Chinese window titles print as ???? when the caller reads a pipe.
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$hwnd = [DesktopState]::GetForegroundWindow()
$title = New-Object Text.StringBuilder 512
[DesktopState]::GetWindowText($hwnd, $title, 512) | Out-Null
$fg_pid = 0
[DesktopState]::GetWindowThreadProcessId($hwnd, [ref]$fg_pid) | Out-Null
$rect = New-Object DesktopState+RECT
[DesktopState]::GetWindowRect($hwnd, [ref]$rect) | Out-Null
$fg_name = (Get-Process -Id $fg_pid -ErrorAction SilentlyContinue).ProcessName
"foreground: pid=$fg_pid ($fg_name) title='$title' rect=($($rect.L),$($rect.T),$($rect.R),$($rect.B))"

"================ windows: pid, minimized, process, title"
Get-Process | Where-Object { $_.MainWindowTitle } | ForEach-Object {
    "{0,7}  {1,-5}  {2,-20}  {3}" -f $_.Id, [DesktopState]::IsIconic($_.MainWindowHandle), $_.ProcessName, $_.MainWindowTitle
}
