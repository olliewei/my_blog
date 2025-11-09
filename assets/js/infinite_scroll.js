$(document).ready(function() {
    console.log("✅ infinite_scroll.js 调试版启动");
    let loading = false;
    let searchKeyword = "{{ search if search else '' }}"; // ✅ 当前搜索关键字

    function loadMoreArticles() {
        if (!window.nextPage || loading) return;
        loading = true;

        // 显示加载指示器
        let loadingIndicator = $('#loading-indicator');
        if (loadingIndicator.length === 0) {
            $('body').append('<div id="loading-indicator" style="text-align:center;padding:1rem;color:#555;">加载中...</div>');
            loadingIndicator = $('#loading-indicator');
        }
        loadingIndicator.show();

        console.log("⬇️ 正在加载第", nextPage, "页...");

        $.get(window.loadUrl, { page: window.nextPage, ajax: 1, search:window.searchKeyword ||"" }, function(data) {
            console.log("✅ 收到响应:", data);
            loadingIndicator.hide();

            if (!data.articles || data.articles.length === 0) {
                console.warn("⚠️ 没有更多文章返回");
                $('#end-indicator').show();
                $('#loading-indicator').hide();
                loading = false;
                nextPage = null;
                return;
            }
            if (data.articles && data.articles.length > 0) {
                data.articles.forEach(article => {
                    console.log("📄 渲染文章:", article.title);
                    const card = `
                        <div class="card article-card mt-4">
                            <div class="card-header">
                                <a class="btn fs-5 fw-bold" href="article/${article.id}.html">${article.title}</a>
                            </div>
                            <div class="card-body">
                                <p class="card-text card-text-truncate">
                                    <a class="btn fs-6" href="article/${article.id}.html">${article.content}</a>
                                </p>
                                <ul class="nav">
                                    <li class="nav-item me-auto">
                                        <small class="text-body-secondary">${article.author}</small>
                                    </li>
                                    <li class="nav-item me-auto">
                                        <small class="text-body-secondary">${article.create_time}</small>
                                    </li>
                                </ul>
                            </div>
                        </div>`;
                    $('#articles-container').append(card);
                });
            }

            if (data.has_next) {
                window.nextPage = data.next_page;
            } else {
                window.nextPage = null;
                if ($('#end-indicator').length === 0) {
                    $('body').append('<div id="end-indicator" style="text-align:center;padding:1rem;color:#aaa;">No more articles 🎉</div>');
                }
            }

            loading = false;
        }).fail(function() {
            loadingIndicator.hide();
            loading = false;
        });
    }
    // ✅ 关键：暴露给全局，否则index中无法调用
    window.loadMoreArticles = loadMoreArticles;

    // ✅ 滚动触发
    $(window).on('scroll', function() {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
            loadMoreArticles();
        }
    });
    // ✅ 初次载入时主动检查一次（解决大屏无滚动问题）
    setTimeout(() => {
        if ($(document).height() <= $(window).height() + 200) {
            loadMoreArticles();
        }
    }, 300);
});
