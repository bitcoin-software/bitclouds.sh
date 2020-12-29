<script>
  import { onMount } from "svelte";
  import Social from "./components/Social.svelte";
  import Create from "./components/Create.svelte";
  import Invoice from "./components/Invoice.svelte";
  let showModal = false;
  let invoice = false;
  let images = [];
  let subscribed = false;
  hljs.initHighlightingOnLoad();

  onMount(async () => {
    try {
      const req = await fetch(`https://bitclouds.sh/images`);
      const res = await req.json();
      images = res.images;
    } catch (e) {
      console.error(e);
    }
  });

  function handleInvoice(event) {
    invoice = event.detail;
  }

  function handlePaid(e) {
    subscribed = e.detail;
  }
</script>

<style>
  .break {
    word-break: break-all;
  }
</style>

<main>
  {#if showModal}
    <Invoice
      on:close={() => (showModal = false)}
      on:paid={handlePaid}
      {invoice} />
  {/if}
  <div class="content-page">
    <div class="content-code" />
    <div class="content">
      <div class="overflow-hidden content-section" id="content-get-started">
        <h2 id="get-started">BITCLOUDS</h2>
        <pre>
          <code class="bash">
            {`# Get a list of available images\n# curl example\ncurl https://bitclouds.sh/images`}
          </code>
        </pre>
        <div>
          <p>
            <a href="bitclouds.sh">bitclouds.sh</a>
            is a programmable VPS platform where you can have any instance for
            66 sats per hour.
          </p>
          <p>
            <Social />
          </p>
        </div>

      </div>
      <div class="overflow-hidden content-section" id="content-get-characters">
        <h2 id="get-characters">create an image</h2>
        <pre>
          <code class="bash">
            {`# curl example\ncurl https://bitclouds.sh/create/'IMAGE'`}
          </code>
          <code class="json">
            {JSON.stringify({ disclaimer: 'If you pay the LN invoice, you agree...', host: 'hassaleh', paytostart: 'lnbc990n1p0ak494m...', performance: '1xXeon-2GB-40GB', price: '<1 sat/min', support: 'https://support.bitclouds.sh' }, null, 2)}
          </code>

        </pre>
        <p>
          Create an instance from the available images:
          <br />
          <code class="higlighted break">{images.toString()}</code>
        </p>
        <p>
          <Create
            {images}
            on:openModal={() => (showModal = true)}
            on:invoice={handleInvoice}
            on:close={() => (showModal = false)} />
        </p>
        <p>
          {#if subscribed}
            Details:
            <ul class="break">
              <li>HOST: {invoice.host}</li>
              <li>Status: {subscribed.status}</li>
              <li>IP: {subscribed.ip4}</li>
              <li>Key: {subscribed.key}</li>
            </ul>
          {/if}
        </p>
      </div>
      <div class="overflow-hidden content-section" id="content-get-characters">
        <h2 id="get-characters">ssh access</h2>
        <pre>
          <code class="bash">
            {`# get access key\ncurl https://bitclouds.sh/key/'HOST_NAME' > ssh.key\n\n#connect to instance\nssh -i ssh.key debian@87.85.113.253`}
          </code>
        </pre>
        <p>Get your ssh key and connect to your instance</p>
      </div>
      <div class="overflow-hidden content-section" id="content-get-characters">
        <h2 id="get-characters">Check status of your VPS</h2>
        <pre>
          <code class="bash">
            {`# curl example\ncurl https://bitclouds.sh/status/'HOST_NAME'`}
          </code>
          <code class="json">
            {JSON.stringify({ balance: 96, ip4: '87.85.113.253', key: 'https://bitclouds.sh/key/hassaleh', status: 'subscribed', tip: 'was your recent backup restore succesfull?', user: 'debian' }, null, 2)}
          </code>
        </pre>
        <p>Check status of your instance</p>
      </div>
      <div class="overflow-hidden content-section" id="content-get-characters">
        <h2 id="get-characters">Top up your VPS</h2>
        <pre>
          <code class="bash">
            {`# curl example\ncurl https://bitclouds.sh/topup/'HOST_NAME'/'AMOUNT'`}
          </code>
        </pre>
        <p>
          To top up send some sats to your VPS, using the
          <code class="higlighted">'HOST_NAME</code>
          and specifying the
          <code class="higlighted">AMOUNT</code>
        </p>
        <p>
          You can also use
          <code class="higlighted">
            curl https://bitclouds.sh/topup/'HOST_NAME'
          </code>
          to add 99 sats by default
        </p>
      </div>
      <div class="overflow-hidden content-section" id="content-get-characters">
        <h2 id="get-characters">For support or send some kind words</h2>
        <pre>
          <code class="bash">
            {`# curl example\nhttps://bitclouds.sh/support/'HOST_NAME'/'YOUR_EMAIL_OR_TELEGRAM_OR_PHONE_OR_WHATEVER'/'MESSAGE'/urgent`}
          </code>
        </pre>
        <p>
          Use this endpoint to ask for support or if just want to say something
          nice...
        </p>
      </div>
      <!-- <div class="overflow-hidden content-section" id="content-errors">
        <h2 id="errors">Errors</h2>
        <p>The Westeros API uses the following error codes:</p>
        <table>
          <thead>
            <tr>
              <th>Error Code</th>
              <th>Meaning</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>X000</td>
              <td>
                Some parameters are missing. This error appears when you don't
                pass every mandatory parameters.
              </td>
            </tr>
            <tr>
              <td>X001</td>
              <td>
                Unknown or unvalid
                <code class="higlighted">secret_key</code>
                . This error appears if you use an unknow API key or if your API
                key expired.
              </td>
            </tr>
            <tr>
              <td>X002</td>
              <td>
                Unvalid
                <code class="higlighted">secret_key</code>
                for this domain. This error appears if you use an API key non
                specified for your domain. Developper or Universal API keys
                doesn't have domain checker.
              </td>
            </tr>
            <tr>
              <td>X003</td>
              <td>
                Unknown or unvalid user
                <code class="higlighted">token</code>
                . This error appears if you use an unknow user
                <code class="higlighted">token</code>
                or if the user
                <code class="higlighted">token</code>
                expired.
              </td>
            </tr>
          </tbody>
        </table>
      </div> -->
    </div>
  </div>
</main>
