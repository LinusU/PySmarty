<?xml version="1.0" charset="utf-8" ?>
<!DOCTYPE html>
<html>
<head>
    <title>{$name}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
    
    <p>
        Hej jag heter {$name|lower|upper}!
    </p>
    
    <p>
        Tre citat-tecken: """
    </p>
    
    <p>
        Sju citat-tecken: """""""
    </p>
    
    {if $test == 4}
    <h1>Test är fyra</h1>
    {elseif $test == 5}
    <h1>Test är fem</h1>
    {else}
    <h1>Test är inte fyra</h1>
    {/if}
    
    <ul>
    {for $i=1 to $test}
        <li>Nummer {$i}</li>
    {/for}
    </ul>
    
    <ul>
    {for $i=$test to 38 step $test}
        <li>Nummer {$i}</li>
    {/for}
    </ul>
    
    <ul>
    {for $i=15 to $test step -2}
        <li>Nummer {$i}</li>
    {/for}
    </ul>
    
    <ul>
    {for $i=15 to -$test step -2}
        <li>Nummer {$i}</li>
    {/for}
    </ul>
    
    <ul>
    {for $i=-15 to -$test step 2}
        <li>Nummer {$i}</li>
    {/for}
    </ul>
    
    <ol>
    {foreach $colors as $key=>$val}
        <li>{$val} ({$key})</li>
    {/foreach}
    </ol>
    
    <ol>
    {foreach $colors as $val}
        <li>{$val|upper}</li>
    {/foreach}
    </ol>
    
    <script type="text/javascript">
        console.log({
            a: "hej",
            b: {ldelim}"då": "re"{rdelim} 
        });
    </script>
    
</body>
</html>