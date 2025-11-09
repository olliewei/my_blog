$(function () {
    // 初始化 showdown 转换器（带优化配置）
    var converter = new showdown.Converter({
        smartIndentationFix: true,
        simpleLineBreaks: true,
        smoothLivePreview: true,
        ghCompatibleHeaderId: true,
    });

    // 定义渲染函数
    function renderPreview() {
        var markdownText = $('#article_content').val();
        var html = converter.makeHtml(markdownText);
        $('#article_preview').html(html);
    }

    // 页面加载完成时立即渲染一次
    renderPreview();

    // 监听输入框变化（实时更新）
    $('#article_content').on('input', function () {
        renderPreview();
    });
});
