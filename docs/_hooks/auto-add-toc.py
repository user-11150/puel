def on_page_markdown(markdown, **kwargs):
    return f"<details markdown><summary>Table of contents</summary>\n<hr>[TOC]</details>\n{markdown}"