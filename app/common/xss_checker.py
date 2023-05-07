def safe_xss(html: str):
    return (
        html.replace("<script", "begin script")
        .replace("</script>", "end script")
        .replace("<iframe", "begin iframe")
        .replace("</iframe>", "end iframe")
        .replace("<frame", "begin frame")
        .replace("</frame>", "end frame")
    )
