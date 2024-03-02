<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta http-equiv="x-ua-compatible" content="ie=edge, chrome=1" />
    <title>{{title}}</title>
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
    <link rel="stylesheet" href="/static/normalize.css">
    <link rel="stylesheet" href="/static/index.css">
    <script src="//cdn.jsdelivr.net/npm/hls.js@1"></script>
</head>

<body>
    {{!body}}
    <video style="max-width: 100%; max-height: 100%;" id="video" controls=""></video>
    <script>
        const video = document.getElementById('video');
        if (!video) {
            alert("Couldn't select video element.")
            throw new Error("Couldn't select video element.")
        }
        if (!Hls.isSupported()) {
            alert("HLS is not supported.")
            throw new Error("HLS is not supported.")
        }

        const hls = new Hls();
        hls.attachMedia(video);
        hls.loadSource("{{video_url}}");
        hls.on(Hls.Events.MEDIA_ATTACHED, () => {
            console.log("video tag bound successfully.");
        });
        hls.on(Hls.Events.MANIFEST_PARSED, (_, data) => {
            console.log("manifest loaded, found", data.levels.length, "quality level");
        });
    </script>
</body>

</html>
