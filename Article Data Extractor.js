// ==UserScript==
// @name		Article Data Extractor
// @description	提取文章标题和注释并导出为TXT文件
// @match		https://www.inoreader.com/annotated
// ==/UserScript==
(function(){
	'use strict';
	// 创建导出按钮
	const exportBtn=document.createElement('button');
	exportBtn.textContent='导出数据';
	exportBtn.style.position='fixed';
	exportBtn.style.top='20px';
	exportBtn.style.right='20px';
	exportBtn.style.zIndex='9999';
	exportBtn.style.padding='10px 15px';
	exportBtn.style.backgroundColor='#4CAF50';
	exportBtn.style.color='white';
	exportBtn.style.border='none';
	exportBtn.style.borderRadius='5px';
	exportBtn.style.cursor='pointer';
	document.body.appendChild(exportBtn);
	// 按钮点击事件
	exportBtn.addEventListener('click',function(){
		// 获取所有文章容器
		const articles=document.querySelectorAll('.article_tile_content_wraper');
		let outputContent='';
		articles.forEach(article=>{
			// 提取标题
			const titleElement=article.querySelector('.article_tile_title .article_title_link');
			const title=titleElement?titleElement.textContent.trim():'无标题';
			// 提取注释
			const noteElement=article.querySelector('.annotations_preview_text');
			const note=noteElement?noteElement.textContent.trim():'无注释';
			// 构建输出行
			outputContent+=`${title}: ${note}\n\n`;
		});
		// 创建并下载文件
		const blob=new Blob([outputContent],{type:'text/plain;charset=utf-8'});
		const url=URL.createObjectURL(blob);
		const a=document.createElement('a');
		a.href=url;
		a.download='文章数据.txt';
		document.body.appendChild(a);
		a.click();
		// 清理
		setTimeout(()=>{
			document.body.removeChild(a);
			URL.revokeObjectURL(url);
		},100);
	});
})();