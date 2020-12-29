<script>
  import QRCode from "qrcode";
  import { createEventDispatcher, onMount } from "svelte";
  import { fly } from "svelte/transition";
  import Check from "./Done.svelte";

  const dispatch = createEventDispatcher();
  let modal;
  let paid = false;

  const interval = setInterval(async () => {
    const response = await fetch(`https://bitclouds.sh/status/${invoice.host}`);
    const res = await response.json();
    if (res.status === "unpaid") return interval;

    dispatch("paid", res);
    paid = true;
    setTimeout(() => {
      dispatch("close");
    }, 3000);
    return clearInterval(interval);
  }, 3000);

  const close = () => {
    clearInterval(interval);
    dispatch("close");
  };
  export let invoice;

  const makeQR = async (address) => {
    try {
      const QR = await QRCode.toDataURL(address, { margin: 0 });
      interval;
      return QR;
    } catch (err) {
      console.error(err);
    }
  };
</script>

<style>
  .modal-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.3);
    z-index: 998;
  }

  .modal {
    position: fixed;
    left: 50%;
    top: 50%;
    width: calc(100vw - 4em);
    max-width: 32em;
    max-height: calc(100vh - 4em);
    overflow-x: hidden;
    transform: translate(-50%, -50%);
    padding: 1em;
    border-radius: 0.2em;
    background: white;
    z-index: 999;
  }

  figure {
    display: flex;
    flex-flow: column;
    align-items: center;
    margin: 1em;
  }
  figcaption {
    word-break: break-all;
    font-size: 70%;
    margin-top: 1em;
  }
  footer {
    text-align: center;
  }
  footer > h2 {
    font-size: 1.333rem;
    margin-top: 1em;
    margin-bottom: 0.8em;
    color: #034c8f;
    text-transform: uppercase;
    font-family: "Roboto Condensed", sans-serif;
  }
  footer > a {
    font-size: 80%;
  }
</style>

<div class="modal-background" on:click={close} />

<div
  class="modal"
  role="dialog"
  aria-modal="true"
  bind:this={modal}
  in:fly={{ y: 200, duration: 500 }}
  out:fly={{ y: -200, duration: 500 }}>
  <header>
    <h3>
      {invoice ? `Pay invoice for your host: ${invoice.host}` : `Fetching your invoice`}
    </h3>
  </header>
  <div>
    {#if paid}
      <Check />
    {:else if invoice}
      {#await makeQR(invoice.paytostart)}
        <p>Wait...</p>
      {:then qr}
        <figure>
          <a href={`lightning:${invoice.paytostart}`}>
            <img src={qr} alt={invoice.paytostart} />
          </a>
          <figcaption>{invoice.paytostart}</figcaption>
        </figure>
      {:catch error}
        <p>Oh no! Something went wrong!</p>
      {/await}
    {/if}
  </div>
  <footer>
    {#if paid}
      <h2>Done</h2>
    {/if}
    <a href="https://support.bitclouds.sh">Support at support.bitclouds.sh</a>
  </footer>
</div>
