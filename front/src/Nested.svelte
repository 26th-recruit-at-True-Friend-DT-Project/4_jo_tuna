<script>
    let count = 0;

    function incrementCount() {
        cnt += 1;
    }
</script>

<button on:click={incrementCount}>
    Clicked {cnt} {cnt === 1 ? 'time' : 'times'}
</button>