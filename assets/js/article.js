$(function () {
    // 初始化 showdown 转换器（带优化配置）
    var converter = new showdown.Converter({
        tables: true,        // ✅ 开启表格解析
        strikethrough: true, // （可选）开启删除线
        tasklists: true,     // （可选）开启任务列表
        // simpleLineBreaks: true // （推荐）让单个换行生效
        smartIndentationFix: true,
        simpleLineBreaks: true,
        smoothLivePreview: true,
        ghCompatibleHeaderId: true,
        // 代码相关配置
        backslashEscapesHTMLTags: true,
        smoothLivePreview: true,
        extensions: [{
            type: 'output',
            filter: function(text) {
                // 确保代码块有正确的 Prism.js 语言类名
                return text.replace(
                    /```(\w+)?\n([\s\S]*?)```/g,
                    function(match, language, code) {
                        var lang = language || 'text';
                        var cleanedCode = code.trim();
                        // 生成 Prism.js 兼容的 HTML
                        return `<pre class="language-${lang}"><code class="language-${lang}">${cleanedCode}</code></pre>`;
                    }
                );
            }
        }]

    });

    // 定义渲染函数
    function renderPreview() {
        var markdownText = $('#article_content').val();
        var html = converter.makeHtml(markdownText);
        //将前段包含markdown内容的 id传进来
        $('#article_viewer').html(html);
        // 使用 Prism 进行语法高亮
        if (window.Prism) {
            Prism.highlightAll();
            console.log('Prism 语法高亮已应用');
        } else {
            console.log('Prism.js 未加载');
        }

    }

    // 页面加载完成时立即渲染一次
    renderPreview();

});