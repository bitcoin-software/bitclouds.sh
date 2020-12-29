<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();
  let selected;
  export let images;

  const handleCreate = async () => {
    console.log("create");
    if (!selected) return;
    dispatch("openModal");
    try {
      const req = await fetch(`https://bitclouds.sh/create/${selected}`);
      const res = await req.json();
      dispatch("invoice", { ...res });
    } catch (e) {
      console.error(e);
      dispatch("close");
    }
  };
</script>

<style>
  button {
    background: #034c8f;
    border: 0.05rem solid #034c8f;
    border-radius: 0.25rem;
    cursor: pointer;
    display: inline-block;
    line-height: 1.2rem;
    outline: 0;
    padding: 0.25rem 0.4rem;
    text-align: center;
    text-decoration: none;
    transition: background 0.2s, border 0.2s, box-shadow 0.2s, color 0.2s;
    vertical-align: middle;
    white-space: nowrap;
    color: #fff;
    margin: 0;
    margin-left: 0.5rem;
  }

  button:hover {
    background: #00a8e3;
  }

  button:disabled {
    cursor: initial;
    background: #3c5f80;
    color: #999;
  }
</style>

<div class="form">
  <select bind:value={selected}>
    <option value="" default>Choose image</option>
    {#each images as image}
      <option value={image}>{image}</option>
    {/each}
  </select>
  <button disabled={!selected} on:click={handleCreate}>CREATE</button>
</div>
