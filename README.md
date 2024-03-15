The following software must be installed on your machine:
    - Docker and Docker-compose
    - Ngrok
    - JQ

1. **Start ngrok** from a new terminal running `ngrok http 8021`

2. **Register DID** on the BCLedger at `http://test.bcovrin.vonx.io/` using a 32bit wallet seed. Remember your seed, we need it to start the AcaPy agent.

3. **Start AcaPy Agent** from the auries-cloudagent-python root directory running the following command (Exchange <ngrok_endpoint> with the endpoint shown in the ngrok terminal (e.g.: `https://7f7c-34-16-203-117.ngrok-free.app`) and the <seed> with the 32bit-seed that you registered on the ledger):

    `PORTS="8020:8020 8021:8021" EVENTS=1 scripts/run_docker start --endpoint <ngrok_endpoint> --label authority.agent --auto-ping-connection --auto-respond-messages --inbound-transport http 0.0.0.0 8020 --outbound-transport http --admin 0.0.0.0 8021 --admin-insecure-mode --genesis-url http://test.bcovrin.vonx.io/genesis --wallet-type askar --wallet-name authority.agent744140 --wallet-key authority.agent744140 --preserve-exchange-record --auto-provision --public-invites --seed <seeed> --webhook-url http://172.17.0.1:8000/webhook --monitor-revocation-notification --trace-target log --trace-tag acapy.events --trace-label authority.agent.trace --auto-accept-invites --auto-accept-requests --auto-store-credential`

4. **Build and start Authority Controller** from the authority_controller root directory running `docker-compose up --build` on Mac or `docker compose up --build` on Linux

5. **Start Registration Process** by visiting `http://localhost:8000` in your browser.