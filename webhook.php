<html>

<head>
    <title>Receive Trades</title>

</head>

<body>
    <h1>Receive Webhooks</h1>

    <div id="$data"></div>
    <?php
    
    $json = file_get_contents('php://input');
    // decode json
    $object = json_decode($json);
    // expecting valid json
    if (json_last_error() !== JSON_ERROR_NONE) {
        die(header('HTTP/1.0 415 Unsupported Media Type'));
    }
    echo $post;

    ?>


</body>
</html>

 