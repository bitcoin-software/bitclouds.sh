<script>
  import Git from "./Git.svelte";
  import Telegram from "./Telegram.svelte";
  import Twitter from "./Twitter.svelte";
</script>

<style>
  .social {
    display: flex;
    position: relative;
    padding: 0.5rem 0;
    height: 1.5rem;
  }

  .social > a {
    height: 100%;
    margin-right: 1rem;
    opacity: 0.7;
  }

  .social > a:hover {
    opacity: 1;
    transition: all 0.25s ease;
  }
</style>

<div class="social">
  <a
    href="https://github.com/bitcoin-software/bitclouds.sh/tree/master/how-tos">
    <Git height="100%" width="auto" />
  </a>
  <a href="https://t.me/s/BitClouds">
    <Telegram height="100%" width="auto" />
  </a>
  <a href="https://twitter.com/bitcoinsoftwar1">
    <Twitter height="100%" width="auto" />
  </a>
</div>
