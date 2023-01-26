<script>
	import "bootstrap/dist/css/bootstrap.min.css";
	import Nested from './Nested.svelte';

	let name = 'world!';
	let src = 'imgs/minju.jpg';
	let string = 'this string contains some <strong>HTML!!!</strong>'
</script>

<main>
	<h1>Hello {name.toUpperCase()}!</h1>
	<p>{@html string}</p>
	<img src={src} alt="Svelte">
</main>

<style>
	h1 {
		color: purple;
		font-family: 'Comic Sans MS', cursive;
		font-size: 2em;
	}
</style>