// agent 接管标签页的视觉提示：橙色呼吸边框 + 带光晕的动画光标 + 目标元素高亮。
//
// 用法：MCP 配置 args 加 `--init-page <本文件绝对路径>`，Playwright MCP 每接管一个
// 标签页就调用一次。靠 Playwright 自带的 page.screencast.showActions / showOverlay，
// 画在页面里（不需要录屏），翻页后自动重画；只有接管的标签页有，用户自己的页不受影响。
//
// 代价：每次点击 / 悬停前停 duration 毫秒播光标动画。
//
// 失败一律吞掉：init-page 抛错会让标签页初始化失败，整个浏览器工具跟着不可用。
const kOrange = '255,140,40';

// 用户浮层和光标在同一个 shadow root 里，所以这里的 <style> 能管到光标。
// shortcut: 依赖 Playwright 内部元素名 x-pw-action-cursor，改名后只丢光晕（光标还在），届时改选择器
const kOverlay = `<style>
  @keyframes pw-agent-glow {
    0%, 100% { box-shadow: inset 0 0 18px 4px rgba(${kOrange}, .5); }
    50% { box-shadow: inset 0 0 34px 10px rgba(${kOrange}, .85); }
  }
  .pw-agent-glow { position: fixed; inset: 0; pointer-events: none; animation: pw-agent-glow 2.4s ease-in-out infinite; }
  x-pw-action-cursor { filter: drop-shadow(0 0 3px rgba(${kOrange}, 1)) drop-shadow(0 0 8px rgba(${kOrange}, .8)); }
  x-pw-action-cursor::before {
    content: ''; position: absolute; left: -16px; top: -16px; width: 32px; height: 32px; border-radius: 50%;
    background: radial-gradient(rgba(${kOrange}, .55), transparent 70%);
  }
</style><div class="pw-agent-glow"></div>`;

exports.default = async ({ page }) => {
  try {
    await page.screencast.showActions({
      duration: 500,
      style: {
        highlight: `outline: 2px solid rgba(${kOrange}, .9); border-radius: 4px; box-shadow: 0 0 12px rgba(${kOrange}, .6)`,
        title: 'display: none',
      },
    });
    await page.screencast.showOverlay(kOverlay);
  } catch {}
};
