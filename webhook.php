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
    
    echo $post;

    ?>


</body>
</html>

 