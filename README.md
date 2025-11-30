**This software is released under MIT license.**
**本软件在MIT许可下发行**

This project provides a set of programs that helps address the dillema where one wants to look top papers in their field on general journals like Nature but is afraid of being overwhelmed by unrelated literature.

该项目提供一系列程序，帮助解决研究人员希望阅读所在领域在Nature等综合期刊的顶尖论文，但是担心被过多无关文献搞懵的困境。

Usage用法
=========

1. Install [Ollama](https://ollama.com/download) and an Ollama chat [model](https://ollama.com/search)
2. Install provided `requirements.txt` packages to your python environment
3. Install [Tampermonkey](https://www.tampermonkey.net/) plugin on your browser and copy the contents in provided `Article Data Extractor.js` and `Article Link Extractor and Auto-Mark.js` file to new file (`⊞` button) at the extension options page. Press Ctrl+S to save.
4. Create `domain_definition.txt` in the same folder and write in your interested field.
5. The workflow is to download all your unread feeds in https://www.inoreader.com/all_articles by the green added button at top right to the same folder as the `process_articles.py` file and run `process_articles.py`. After it finishes, upload the result by the blue added button. Read the articles and make research notes as comments, and download them in https://www.inoreader.com/all_articles by the added button at top right. For the automation to work, you need to change the coordinates to fit your browser and screen. You may use the provided [AutoHotKey](https://www.autohotkey.com/) script `MouseLocationIdentifier.ahk` to determine the appropriate coordinates.
6. If there is bug, please report to me: [zsc_chris@outlook.com](mailto:zsc_chris@outlook.com). I'll try to solve it with you.
<!-- -->
1. 安装`Ollama(https://ollama.com/download)`和Ollama聊天[模型](https://ollama.com/search)。
2. 将提供的`requirements.txt`文件中的软件包安装到您的Python环境中。
3. 在浏览器中安装[`Tampermonkey`](https://www.tampermonkey.net/)插件，并将提供的`Article Data Extractor.js`和 `Article Link Extractor and Auto-Mark.js`文件中的内容复制到扩展程序选项页面中的新文件（`⊞`按钮）中。按Ctrl+S保存。
4. 在同一文件夹中创建`domain_definition.txt`文件，并在其中写入您感兴趣的领域。
5. 操作流程：点击右上角的绿色按钮，将 https://www.inoreader.com/all_articles 中所有未读的文章下载到与`process_articles.py`文件相同的文件夹中，然后运行​​`process_articles.py`。完成后，点击蓝色按钮上传结果。阅读文章并以评论的形式做研究笔记，然后通过右上角新增的按钮在 https://www.inoreader.com/all_articles 下载它们。为了使自动化功能正常工作，您需要更改坐标以适应您的浏览器和屏幕。您可以使用提供的[AutoHotKey](https://www.autohotkey.com/)脚本 `MouseLocationIdentifier.ahk` 来确定合适的坐标。
6. 如果有bug，请联系我：[zsc_chris@outlook.com](mailto:zsc_chris@outlook.com)。我会尝试和您一起解决。

Requirements依赖
================

`Ollama`*, `Tampermonkey`, `requirements.txt`

*A NVIDIA GPU is preferred最好有英伟达GPU