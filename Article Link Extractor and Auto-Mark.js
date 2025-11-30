// ==UserScript==
// @name         Article Link Extractor and Auto-Mark
// @description  提取文章链接并自动标记非领域文献
// @match		 https://www.inoreader.com/all_articles
// ==/UserScript==

(function() {
    'use strict';

    // 创建按钮容器
    const buttonContainer = document.createElement('div');
    buttonContainer.style.position = 'fixed';
    buttonContainer.style.top = '20px';
    buttonContainer.style.right = '20px';
    buttonContainer.style.zIndex = '9999';
    buttonContainer.style.display = 'flex';
    buttonContainer.style.flexDirection = 'column';
    buttonContainer.style.gap = '10px';
    document.body.appendChild(buttonContainer);

    // 下载链接按钮
    const downloadBtn = document.createElement('button');
    downloadBtn.textContent = '下载文章链接';
    downloadBtn.style.padding = '10px 15px';
    downloadBtn.style.backgroundColor = '#4CAF50';
    downloadBtn.style.color = 'white';
    downloadBtn.style.border = 'none';
    downloadBtn.style.borderRadius = '5px';
    downloadBtn.style.cursor = 'pointer';
    buttonContainer.appendChild(downloadBtn);

    // 上传结果文件按钮
    const uploadBtn = document.createElement('button');
    uploadBtn.textContent = '上传分类结果';
    uploadBtn.style.padding = '10px 15px';
    uploadBtn.style.backgroundColor = '#2196F3';
    uploadBtn.style.color = 'white';
    uploadBtn.style.border = 'none';
    uploadBtn.style.borderRadius = '5px';
    uploadBtn.style.cursor = 'pointer';
    buttonContainer.appendChild(uploadBtn);

    // 下载链接功能
    downloadBtn.addEventListener('click', function() {
        const articles = document.querySelectorAll('.article_title_link');
        let outputContent = '';

        articles.forEach(article => {
            const title = article.textContent.trim();
            const href = article.getAttribute('href');
            outputContent += `${title}\t${href}\n`;
        });

        const blob = new Blob([outputContent], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'article_links.txt';
        document.body.appendChild(a);
        a.click();

        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
    });

    // 上传结果文件功能
    uploadBtn.addEventListener('click', function() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.txt';

        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const content = e.target.result;
                    processClassificationResults(content);
                };
                reader.readAsText(file);
            }
        });

        input.click();
    });

    // 处理分类结果并标记非领域文献
    function processClassificationResults(content) {
        const lines = content.split('\n');
        const articles = document.querySelectorAll('[id^="article_"]');

        lines.forEach(line => {
            if (line.trim()) {
                const [title, domain, model, isInDomain] = line.split('\t');
                if (isInDomain && isInDomain.trim().toLowerCase() === 'false') {
                    // 找到对应的文章并标记为已读
                    articles.forEach(article => {
                        const articleTitle = article.querySelector('.article_title_link');
                        if (articleTitle && articleTitle.textContent.trim() === title.trim()) {
                            const markAsReadBtn = article.querySelector('.icon-article_topbar_mark_as_read_full');
                            if (markAsReadBtn) {
                                markAsReadBtn.click();
                                console.log(`标记为非领域文献: ${title}`);
                            }
                        }
                    });
                }
            }
        });

        alert('非领域文献已自动标记为已读！');
    }
})();